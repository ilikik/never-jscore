use anyhow::{anyhow, Result};
use deno_core::{JsRuntime, RuntimeOptions};
use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use pyo3::types::PyList;
use serde_json::Value as JsonValue;
use std::cell::RefCell;
use std::rc::Rc;

use crate::convert::{json_to_python, python_to_json};
use crate::ops;
use crate::runtime::get_tokio_runtime;
use crate::storage::ResultStorage;

/// JavaScript 执行上下文
///
/// 每个 Context 包含一个独立的 V8 isolate 和 JavaScript 运行时环境。
/// 支持 Promise 和 async/await，默认自动等待 Promise 结果。
#[pyclass(unsendable)]
pub struct Context {
    runtime: RefCell<JsRuntime>,
    result_storage: Rc<ResultStorage>,
    init_code: String,
    compiled: RefCell<bool>,
    exec_count: RefCell<usize>,
}

impl Context {
    /// 创建新的 Context
    pub fn new(code: String) -> PyResult<Self> {
        let storage = Rc::new(ResultStorage::new());

        let runtime = JsRuntime::new(RuntimeOptions {
            extensions: vec![ops::pyexecjs_ext::init(storage.clone())],
            ..Default::default()
        });

        Ok(Context {
            runtime: RefCell::new(runtime),
            result_storage: storage,
            init_code: code,
            compiled: RefCell::new(false),
            exec_count: RefCell::new(0),
        })
    }

    /// 确保初始化代码已编译
    fn ensure_compiled(&self) -> Result<()> {
        if !*self.compiled.borrow() && !self.init_code.is_empty() {
            let mut runtime = self.runtime.borrow_mut();
            runtime
                .execute_script("<compile>", self.init_code.clone())
                .map_err(|e| anyhow!("Compile error: {:?}", e))?;
            *self.compiled.borrow_mut() = true;
        }
        Ok(())
    }

    /// 执行 JavaScript 代码
    ///
    /// 根据 auto_await 参数决定是否自动等待 Promise。
    fn execute_js(&self, code: &str, auto_await: bool) -> Result<String> {
        self.ensure_compiled()?;
        self.result_storage.clear();

        if auto_await {
            // 异步模式：自动等待 Promise
            let tokio_rt = get_tokio_runtime();

            tokio_rt.block_on(async {
                let mut runtime = self.runtime.borrow_mut();

                // 使用 JSON 序列化来安全转义代码字符串（处理所有特殊字符）
                let code_json = serde_json::to_string(code)
                    .map_err(|e| anyhow!("Failed to serialize code: {}", e))?;

                // 包装代码以自动等待 Promise
                let wrapped_code = format!(
                    r#"
                    (async function() {{
                        try {{
                            const code = {};
                            const __result = await Promise.resolve(eval(code));
                            if (__result === undefined) {{
                                Deno.core.ops.op_store_result("null");
                                return null;
                            }}
                            try {{
                                const json = JSON.stringify(__result);
                                Deno.core.ops.op_store_result(json);
                                return __result;
                            }} catch(e) {{
                                const str = JSON.stringify(String(__result));
                                Deno.core.ops.op_store_result(str);
                                return __result;
                            }}
                        }} catch(err) {{
                            throw err;
                        }}
                    }})()
                    "#,
                    code_json
                );

                runtime
                    .execute_script("<eval_async>", wrapped_code)
                    .map_err(|e| anyhow!("Execution failed: {:?}", e))?;

                // 运行 event loop 等待 Promise 完成
                runtime
                    .run_event_loop(Default::default())
                    .await
                    .map_err(|e| anyhow!("Event loop error: {:?}", e))?;

                let result = self
                    .result_storage
                    .take()
                    .ok_or_else(|| anyhow!("No result stored"))?;

                // 更新执行计数
                let mut count = self.exec_count.borrow_mut();
                *count += 1;

                // 每 100 次执行后提示 GC
                if *count % 100 == 0 {
                    drop(runtime);
                    std::hint::black_box(());
                }

                Ok(result)
            })
        } else {
            // 同步模式：不等待 Promise
            let mut runtime = self.runtime.borrow_mut();

            // 使用 JSON 序列化来安全转义代码字符串（处理所有特殊字符）
            let code_json = serde_json::to_string(code)
                .map_err(|e| anyhow!("Failed to serialize code: {}", e))?;

            let wrapped_code = format!(
                r#"
                (function() {{
                    const code = {};
                    const __result = eval(code);
                    if (__result === undefined) {{
                        Deno.core.ops.op_store_result("null");
                        return null;
                    }}
                    try {{
                        const json = JSON.stringify(__result);
                        Deno.core.ops.op_store_result(json);
                        return __result;
                    }} catch(e) {{
                        const str = JSON.stringify(String(__result));
                        Deno.core.ops.op_store_result(str);
                        return __result;
                    }}
                }})()
                "#,
                code_json
            );

            runtime
                .execute_script("<eval_sync>", wrapped_code)
                .map_err(|e| anyhow!("Execution failed: {:?}", e))?;

            let result = self
                .result_storage
                .take()
                .ok_or_else(|| anyhow!("No result stored"))?;

            let mut count = self.exec_count.borrow_mut();
            *count += 1;

            if *count % 100 == 0 {
                drop(runtime);
                std::hint::black_box(());
            }

            Ok(result)
        }
    }

    /// 请求垃圾回收
    fn request_gc(&self) -> Result<()> {
        let mut runtime = self.runtime.borrow_mut();
        let _ = runtime.execute_script(
            "<gc_hint>",
            "if (typeof gc === 'function') { gc(); } null;",
        );
        Ok(())
    }
}

impl Drop for Context {
    fn drop(&mut self) {
        // 清理资源
        self.result_storage.clear();
        *self.compiled.borrow_mut() = false;
    }
}

// ============================================
// Python Methods
// ============================================

#[pymethods]
impl Context {
    /// 调用 JavaScript 函数
    ///
    /// Args:
    ///     name: 函数名称
    ///     args: 参数列表
    ///     auto_await: 是否自动等待 Promise（默认 True）
    ///
    /// Returns:
    ///     函数返回值，自动转换为 Python 对象
    #[pyo3(signature = (name, args, auto_await=None))]
    pub fn call<'py>(
        &self,
        py: Python<'py>,
        name: String,
        args: &Bound<'_, PyAny>,
        auto_await: Option<bool>,
    ) -> PyResult<Bound<'py, PyAny>> {
        let json_args = if args.is_instance_of::<PyList>() {
            let list = args.downcast::<PyList>()?;
            let mut vec_args = Vec::with_capacity(list.len());
            for item in list.iter() {
                vec_args.push(python_to_json(&item)?);
            }
            vec_args
        } else {
            vec![python_to_json(args)?]
        };

        let args_json: Vec<String> = json_args
            .iter()
            .map(|arg| serde_json::to_string(arg).unwrap())
            .collect();
        let args_str = args_json.join(", ");
        let call_code = format!("{}({})", name, args_str);

        let result_json = self
            .execute_js(&call_code, auto_await.unwrap_or(true))
            .map_err(|e| PyException::new_err(format!("Call error: {}", e)))?;

        let result: JsonValue = serde_json::from_str(&result_json)
            .map_err(|e| PyException::new_err(format!("JSON parse error: {}", e)))?;

        json_to_python(py, &result)
    }

    /// 在当前上下文执行代码
    ///
    /// Args:
    ///     code: JavaScript 代码
    ///     auto_await: 是否自动等待 Promise（默认 True）
    ///
    /// Returns:
    ///     执行结果，自动转换为 Python 对象
    #[pyo3(signature = (code, auto_await=None))]
    pub fn eval<'py>(
        &self,
        py: Python<'py>,
        code: String,
        auto_await: Option<bool>,
    ) -> PyResult<Bound<'py, PyAny>> {
        let result_json = self
            .execute_js(&code, auto_await.unwrap_or(true))
            .map_err(|e| PyException::new_err(format!("Eval error: {}", e)))?;

        let result: JsonValue = serde_json::from_str(&result_json)
            .map_err(|e| PyException::new_err(format!("JSON parse error: {}", e)))?;

        json_to_python(py, &result)
    }

    /// 请求垃圾回收
    ///
    /// 注意：这只是向 V8 发送 GC 请求，V8 会根据自己的策略决定是否执行。
    fn gc(&self) -> PyResult<()> {
        self.request_gc()
            .map_err(|e| PyException::new_err(format!("GC error: {}", e)))
    }

    /// 获取执行统计信息
    ///
    /// Returns:
    ///     (exec_count,) 执行次数
    fn get_stats(&self) -> PyResult<(usize,)> {
        Ok((*self.exec_count.borrow(),))
    }

    /// 重置统计信息
    fn reset_stats(&self) -> PyResult<()> {
        *self.exec_count.borrow_mut() = 0;
        Ok(())
    }
}
