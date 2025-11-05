# 方案3: 自定义Ops实现关键API

这个方案通过deno_core的ops机制，从Rust侧实现关键的Web API。

## 优点
- 完全可控，可以根据需求定制
- 不依赖额外的crate
- 编译体积小
- 可以针对JS逆向场景优化

## 缺点
- 需要手写Rust代码
- 需要理解deno_core的ops机制
- 对于复杂API（如fetch）实现工作量大

## 适用场景
- 只需要几个关键API（如console.log, setTimeout）
- 需要特殊的实现逻辑（如记录所有console.log用于调试）
- 希望保持最小依赖

## 实现示例

### 1. 创建新文件 src/web_apis.rs

```rust
use deno_core::{extension, op2, OpState};
use std::time::Duration;

/// Op: console.log 实现
///
/// 将JavaScript的console.log输出到Python侧
#[op2(fast)]
pub fn op_console_log(#[string] msg: String) {
    // 简单实现：输出到stderr
    eprintln!("[JS] {}", msg);

    // 高级实现：可以通过ResultStorage传递给Python
    // 这样Python可以捕获所有console.log输出
}

/// Op: 简化的setTimeout实现
///
/// 注意：这是一个简化版本，实际的setTimeout需要更复杂的实现
#[op2(async)]
pub async fn op_set_timeout(delay: f64) {
    tokio::time::sleep(Duration::from_millis(delay as u64)).await;
}

/// Op: atob实现 (Base64解码)
#[op2]
#[string]
pub fn op_atob(#[string] input: String) -> Result<String, anyhow::Error> {
    use base64::Engine;
    let bytes = base64::engine::general_purpose::STANDARD
        .decode(input)
        .map_err(|e| anyhow::anyhow!("atob error: {}", e))?;

    String::from_utf8(bytes)
        .map_err(|e| anyhow::anyhow!("atob error: {}", e))
}

/// Op: btoa实现 (Base64编码)
#[op2]
#[string]
pub fn op_btoa(#[string] input: String) -> String {
    use base64::Engine;
    base64::engine::general_purpose::STANDARD.encode(input.as_bytes())
}

/// Op: 获取当前时间戳
#[op2(fast)]
pub fn op_date_now() -> f64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_millis() as f64
}

// 定义扩展
extension!(
    web_apis,
    ops = [
        op_console_log,
        op_set_timeout,
        op_atob,
        op_btoa,
        op_date_now,
    ],
    esm_entry_point = "ext:web_apis/webapis.js",
    esm = [
        dir "src/js",
        "webapis.js"
    ],
);
```

### 2. 创建JavaScript胶水代码 src/js/webapis.js

```javascript
// 将Rust ops封装成标准Web API

// Console API
if (typeof console === 'undefined') {
    globalThis.console = {
        log: (...args) => {
            const msg = args.map(arg => {
                if (typeof arg === 'object') {
                    try {
                        return JSON.stringify(arg);
                    } catch {
                        return String(arg);
                    }
                }
                return String(arg);
            }).join(' ');

            Deno.core.ops.op_console_log(msg);
        },
        warn: (...args) => {
            globalThis.console.log('[WARN]', ...args);
        },
        error: (...args) => {
            globalThis.console.log('[ERROR]', ...args);
        },
        info: (...args) => {
            globalThis.console.log('[INFO]', ...args);
        },
        debug: (...args) => {
            globalThis.console.log('[DEBUG]', ...args);
        }
    };
}

// Base64 API
if (typeof atob === 'undefined') {
    globalThis.atob = (input) => {
        return Deno.core.ops.op_atob(input);
    };
}

if (typeof btoa === 'undefined') {
    globalThis.btoa = (input) => {
        return Deno.core.ops.op_btoa(input);
    };
}

// setTimeout实现（真正的异步）
if (typeof setTimeout === 'undefined') {
    let nextTimerId = 1;
    const activeTimers = new Map();

    globalThis.setTimeout = (callback, delay, ...args) => {
        const timerId = nextTimerId++;

        // 启动异步延迟
        (async () => {
            await Deno.core.ops.op_set_timeout(delay || 0);
            if (activeTimers.has(timerId)) {
                activeTimers.delete(timerId);
                callback(...args);
            }
        })();

        activeTimers.set(timerId, true);
        return timerId;
    };

    globalThis.clearTimeout = (timerId) => {
        activeTimers.delete(timerId);
    };
}

// Date.now优化（从Rust侧获取，更快）
const originalDateNow = Date.now;
Date.now = () => {
    return Deno.core.ops.op_date_now();
};

// 导出标记
globalThis.__WEB_APIS_LOADED__ = true;
```

### 3. 修改 src/lib.rs

```rust
mod context;
mod convert;
mod ops;
mod runtime;
mod storage;
mod web_apis;  // 新增

use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use std::cell::RefCell;

use context::Context;
use runtime::ensure_v8_initialized;

// ... 其他代码保持不变
```

### 4. 修改 src/context.rs

```rust
impl Context {
    pub fn new(code: String) -> PyResult<Self> {
        let storage = Rc::new(ResultStorage::new());

        let runtime = JsRuntime::new(RuntimeOptions {
            extensions: vec![
                ops::pyexecjs_ext::init(storage.clone()),
                crate::web_apis::web_apis::init(),  // 添加自定义Web API扩展
            ],
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
}
```

### 5. 更新 Cargo.toml（添加base64依赖）

```toml
[dependencies]
deno_core = "0.365.0"
anyhow = "1.0.100"
tokio = { version = "1.48", features = ["rt", "time", "macros"] }
serde_json = "1.0"
pyo3 = { version = "0.27.1", features = ["extension-module", "abi3-py38"] }
base64 = "0.22"  # 用于atob/btoa实现
```

## 使用效果

```python
import never_jscore as execjs

ctx = execjs.compile("""
    function testCustomAPIs() {
        // 使用console.log（会输出到Python的stderr）
        console.log('Hello from JavaScript!');

        // 使用atob/btoa
        const encoded = btoa('Hello');
        console.log('Encoded:', encoded);

        const decoded = atob(encoded);
        console.log('Decoded:', decoded);

        // 使用setTimeout（真正的异步！）
        return new Promise((resolve) => {
            setTimeout(() => {
                console.log('Timeout executed!');
                resolve('Done');
            }, 1000);
        });
    }
""")

# 自动等待Promise完成
result = ctx.call("testCustomAPIs", [])
print(f"Result: {result}")
```

输出：
```
[JS] Hello from JavaScript!
[JS] Encoded: SGVsbG8=
[JS] Decoded: Hello
[JS] Timeout executed!
Result: Done
```

## 进阶：捕获console.log到Python

如果你想在Python侧捕获所有console.log输出：

### 修改 src/storage.rs

```rust
pub struct ResultStorage {
    pub value: RefCell<Option<String>>,
    pub console_logs: RefCell<Vec<String>>,  // 新增
}

impl ResultStorage {
    pub fn new() -> Self {
        Self {
            value: RefCell::new(None),
            console_logs: RefCell::new(Vec::new()),
        }
    }

    pub fn add_log(&self, msg: String) {
        self.console_logs.borrow_mut().push(msg);
    }

    pub fn get_logs(&self) -> Vec<String> {
        self.console_logs.borrow().clone()
    }

    pub fn clear_logs(&self) {
        self.console_logs.borrow_mut().clear();
    }
}
```

### 修改 src/web_apis.rs

```rust
#[op2(fast)]
pub fn op_console_log(state: &mut OpState, #[string] msg: String) {
    // 输出到stderr
    eprintln!("[JS] {}", msg);

    // 同时保存到storage
    if let Some(storage) = state.try_borrow_mut::<Rc<ResultStorage>>() {
        storage.add_log(msg);
    }
}
```

### 添加Python方法到Context

```rust
#[pymethods]
impl Context {
    // ... 现有方法 ...

    /// 获取所有console.log输出
    fn get_console_logs(&self) -> PyResult<Vec<String>> {
        Ok(self.result_storage.get_logs())
    }

    /// 清除console.log缓存
    fn clear_console_logs(&self) -> PyResult<()> {
        self.result_storage.clear_logs();
        Ok(())
    }
}
```

### Python使用

```python
ctx = execjs.compile("""
    function test() {
        console.log('Log 1');
        console.log('Log 2');
        console.error('Error message');
        return 'done';
    }
""")

result = ctx.call("test", [])
logs = ctx.get_console_logs()

print("Result:", result)
print("Logs captured:")
for log in logs:
    print("  -", log)
```

## 方案对比总结

| 特性 | 方案1 Polyfill | 方案2 Deno扩展 | 方案3 自定义Ops |
|------|---------------|---------------|----------------|
| 实现难度 | ⭐ 简单 | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐ 复杂 |
| 性能 | ⭐⭐⭐ 好 | ⭐⭐⭐⭐ 很好 | ⭐⭐⭐⭐⭐ 最好 |
| 真异步支持 | ❌ 假的 | ✅ 真的 | ✅ 真的 |
| 编译大小 | ⭐⭐⭐⭐⭐ 最小 | ⭐⭐ 大 | ⭐⭐⭐⭐ 小 |
| 可定制性 | ⭐⭐ 低 | ⭐⭐⭐ 中 | ⭐⭐⭐⭐⭐ 高 |
| 维护成本 | ⭐⭐⭐⭐⭐ 低 | ⭐⭐⭐ 中 | ⭐⭐ 高 |

## 推荐策略

1. **初期/大多数场景**: 使用方案1（Polyfill）
2. **需要真异步**: 先尝试方案2（Deno扩展），如果编译有问题再考虑方案3
3. **特殊需求**（如捕获console.log，特殊的setTimeout行为）: 使用方案3
4. **混合方案**: Polyfill处理大部分API + 自定义Ops处理关键API

例如：
```rust
extensions: vec![
    ops::pyexecjs_ext::init(storage.clone()),
    web_apis::web_apis::init(),  // 只实现console和atob/btoa
    // 其他API用polyfill处理
]
```
