use deno_core::{OpState, extension, op2};
use std::rc::Rc;

use crate::storage::ResultStorage;

/// Op: 存储 JavaScript 执行结果
///
/// 这个 op 允许 JavaScript 代码将执行结果存储到 Rust 端。
/// 使用 #[op2(fast)] 优化性能。
#[op2(fast)]
pub fn op_store_result(state: &mut OpState, #[string] value: String) {
    if let Some(storage) = state.try_borrow_mut::<Rc<ResultStorage>>() {
        storage.store(value);
    }
}

// 扩展
// 注册自定义 ops 到 Deno Core runtime。
// storage 通过 options 传入，并在 state 初始化时设置。
extension!(
    pyexecjs_ext,
    ops = [op_store_result],
    options = {
        storage: Rc<ResultStorage>,
    },
    state = |state, options| {
        state.put(options.storage);
    }
);
