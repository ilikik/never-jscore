// src/lib.rs - Main library entry point
// Refactored for better module organization

mod context;
mod convert;
mod runtime;
mod storage;

// Organized ops modules
mod ops;

// Legacy individual modules (for backward compatibility during migration)
mod crypto_ops;
mod encoding_ops;
mod timer_ops;
mod worker_ops;
mod fs_ops;
mod fetch_ops;

use pyo3::prelude::*;
use context::Context;

/// never_jscore Python 模块
///
/// 高性能 Python JavaScript 执行引擎，基于 Deno Core (V8)
/// 支持 Promise/async, fetch(), require(), WebAssembly 等现代 JS 特性
///
/// # 重构说明 (v2.2.0)
/// - 模块化 ops 组织结构
/// - 新增 localStorage/sessionStorage 支持
/// - 新增 window/navigator/location/document 浏览器环境对象
/// - 改进测试框架
///
/// # 使用示例
/// ```python
/// import never_jscore
///
/// # 创建 JS 执行环境
/// ctx = never_jscore.Context()
///
/// # 执行 JavaScript 代码
/// ctx.eval("function add(a, b) { return a + b; }")
/// result = ctx.call("add", [1, 2])
/// print(result)  # 3
///
/// # 使用浏览器 API
/// result = ctx.evaluate("localStorage.setItem('key', 'value')")
/// value = ctx.evaluate("localStorage.getItem('key')")
///
/// # 使用 fetch API
/// result = ctx.evaluate("""
///     (async () => {
///         const res = await fetch('https://api.github.com');
///         return res.status;
///     })()
/// """)
/// ```
#[pymodule]
fn never_jscore(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // 只导出 Context 类
    m.add_class::<Context>()?;

    // 添加版本信息
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("__doc__", "High-performance JavaScript execution engine for Python")?;

    Ok(())
}
