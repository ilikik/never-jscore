use std::sync::{Arc, OnceLock};

/// 全局 Tokio Runtime 实例
///
/// 使用 OnceLock 确保只初始化一次，所有 Context 共享同一个 tokio runtime。
static TOKIO_RUNTIME: OnceLock<Arc<tokio::runtime::Runtime>> = OnceLock::new();

/// 确保 V8 平台和 Tokio Runtime 已初始化
///
/// 这个函数是幂等的，可以多次调用，但只会初始化一次。
/// 必须在创建任何 JsRuntime 之前调用。
pub fn ensure_v8_initialized() {
    TOKIO_RUNTIME.get_or_init(|| {
        // 初始化 V8 平台
        deno_core::JsRuntime::init_platform(None, false);

        // 创建全局共享的 tokio runtime
        // 必须使用单线程 runtime，因为 V8 isolate 不是线程安全的
        let rt = tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .expect("Failed to create tokio runtime");

        Arc::new(rt)
    });
}

/// 获取全局 Tokio Runtime
///
/// 如果还未初始化，会 panic。
/// 应该先调用 ensure_v8_initialized()。
pub fn get_tokio_runtime() -> Arc<tokio::runtime::Runtime> {
    TOKIO_RUNTIME
        .get()
        .expect("Tokio runtime not initialized")
        .clone()
}
