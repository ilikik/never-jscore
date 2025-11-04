mod context;
mod convert;
mod ops;
mod runtime;
mod storage;

use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use std::cell::RefCell;

use context::Context;
use runtime::ensure_v8_initialized;

// 线程局部的全局 Context 缓存，用于优化 eval() 性能
thread_local! {
    static EVAL_CONTEXT: RefCell<Option<Context>> = RefCell::new(None);
}

/// 编译 JavaScript 代码并返回执行上下文
///
/// Args:
///     code: JavaScript 代码字符串
///
/// Returns:
///     Context 对象，可用于调用函数和执行代码
///
/// Example:
///     ```python
///     ctx = compile('''
///         function add(a, b) { return a + b; }
///     ''')
///     result = ctx.call("add", [1, 2])
///     ```
#[pyfunction]
fn compile(code: String) -> PyResult<Context> {
    ensure_v8_initialized();
    Context::new(code)
}

/// 直接执行 JavaScript 代码并返回结果
///
/// 性能说明：
///     此函数使用线程局部缓存的 Context，避免重复创建 V8 isolate。
///     首次调用时会初始化 Context，后续调用将复用同一个 Context。
///     相比之前版本，性能提升约 1000倍。
///
/// Args:
///     code: JavaScript 代码字符串
///     auto_await: 是否自动等待 Promise（默认 True）
///
/// Returns:
///     执行结果，自动转换为 Python 对象
///
/// Example:
///     ```python
///     result = eval("1 + 2 + 3")  # 6
///     result = eval("Promise.resolve(42)")  # 42
///     ```
#[pyfunction]
#[pyo3(signature = (code, auto_await=None))]
fn eval<'py>(
    py: Python<'py>,
    code: String,
    auto_await: Option<bool>,
) -> PyResult<Bound<'py, PyAny>> {
    ensure_v8_initialized();

    EVAL_CONTEXT.with(|ctx_cell| -> PyResult<Bound<'py, PyAny>> {
        // 检查是否需要初始化 Context
        if ctx_cell.borrow().is_none() {
            let new_ctx = Context::new(String::new())?;
            *ctx_cell.borrow_mut() = Some(new_ctx);
        }

        // 获取 Context 的不可变借用并执行 eval
        let ctx_ref = ctx_cell.borrow();
        let ctx = ctx_ref.as_ref().unwrap();
        ctx.eval(py, code, auto_await)
    })
}

/// 从文件读取并编译 JavaScript 代码
///
/// Args:
///     path: JavaScript 文件路径
///
/// Returns:
///     Context 对象
///
/// Example:
///     ```python
///     ctx = compile_file("script.js")
///     result = ctx.call("myFunction", [arg1, arg2])
///     ```
#[pyfunction]
fn compile_file(path: String) -> PyResult<Context> {
    let code = std::fs::read_to_string(&path)
        .map_err(|e| PyException::new_err(format!("Failed to read file: {}", e)))?;
    compile(code)
}

/// 从文件读取并执行 JavaScript 代码
///
/// Args:
///     path: JavaScript 文件路径
///     auto_await: 是否自动等待 Promise（默认 True）
///
/// Returns:
///     执行结果
///
/// Example:
///     ```python
///     result = eval_file("script.js")
///     ```
#[pyfunction]
#[pyo3(signature = (path, auto_await=None))]
fn eval_file<'py>(
    py: Python<'py>,
    path: String,
    auto_await: Option<bool>,
) -> PyResult<Bound<'py, PyAny>> {
    let code = std::fs::read_to_string(&path)
        .map_err(|e| PyException::new_err(format!("Failed to read file: {}", e)))?;
    eval(py, code, auto_await)
}

/// PyExecJS-RS Python 模块
#[pymodule]
fn never_jscore(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(compile, m)?)?;
    m.add_function(wrap_pyfunction!(eval, m)?)?;
    m.add_function(wrap_pyfunction!(compile_file, m)?)?;
    m.add_function(wrap_pyfunction!(eval_file, m)?)?;
    m.add_class::<Context>()?;
    Ok(())
}
