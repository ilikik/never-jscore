# 方案2: 使用Deno官方扩展添加Web API支持

这个方案需要修改Rust代码，添加Deno官方提供的扩展crate。

## 优点
- 官方实现，质量有保证
- 真正的异步支持（setTimeout等）
- API完整且符合Web标准

## 缺点
- 需要修改Cargo.toml添加依赖
- 增加编译后的体积
- 某些扩展有复杂的依赖关系

## 实现步骤

### 1. 修改 Cargo.toml

```toml
[dependencies]
deno_core = "0.365.0"
anyhow = "1.0.100"
tokio = { version = "1.48", features = ["rt", "time", "macros"] }
serde_json = "1.0"
pyo3 = { version = "0.27.1", features = ["extension-module", "abi3-py38"] }

# 添加Deno扩展
deno_console = "0.192"  # Console API
deno_url = "0.192"      # URL和URLSearchParams
deno_web = "0.223"      # TextEncoder, TextDecoder, atob, btoa, setTimeout等
deno_webidl = "0.192"   # WebIDL支持（某些扩展需要）
deno_crypto = "0.206"   # Crypto API
```

### 2. 修改 src/context.rs

在创建JsRuntime时添加扩展：

```rust
use deno_core::{JsRuntime, RuntimeOptions};
use deno_console::deno_console;
use deno_url::deno_url;
use deno_web::deno_web;
use deno_crypto::deno_crypto;

impl Context {
    pub fn new(code: String) -> PyResult<Self> {
        let storage = Rc::new(ResultStorage::new());

        // 创建带Web API支持的runtime
        let runtime = JsRuntime::new(RuntimeOptions {
            extensions: vec![
                // 自定义ops
                ops::pyexecjs_ext::init(storage.clone()),

                // Deno官方扩展
                deno_webidl::deno_webidl::init_ops_and_esm(),
                deno_console::deno_console::init_ops_and_esm(),
                deno_url::deno_url::init_ops_and_esm(),
                deno_web::deno_web::init_ops_and_esm::<PermissionsContainer>(
                    Default::default(), // BlobStore
                    None,               // Location
                ),
                deno_crypto::deno_crypto::init_ops_and_esm(None),
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

// 权限容器（Web扩展需要）
struct PermissionsContainer;

impl deno_web::TimersPermission for PermissionsContainer {
    fn allow_hrtime(&mut self) -> bool {
        true
    }
}
```

### 3. 可能需要的额外设置

某些扩展可能需要额外的初始化代码。例如，deno_web需要在JavaScript侧引导：

```rust
// 在Context初始化后执行
runtime.execute_script(
    "<init>",
    r#"
    // 导入Web API到全局作用域
    import * as console from "ext:deno_console/01_console.js";
    import * as timers from "ext:deno_web/02_timers.js";

    globalThis.console = console;
    globalThis.setTimeout = timers.setTimeout;
    globalThis.setInterval = timers.setInterval;
    globalThis.clearTimeout = timers.clearTimeout;
    globalThis.clearInterval = timers.clearInterval;
    "#
)?;
```

## 使用效果

添加扩展后，JS代码可以直接使用Web API：

```python
import never_jscore as execjs

ctx = execjs.compile("""
    function testWebAPIs() {
        // 真正的setTimeout支持
        let result = 'start';
        setTimeout(() => {
            result = 'timeout called';
        }, 100);

        // Console API
        console.log('This is a real console.log');

        // Crypto API
        const array = new Uint8Array(10);
        crypto.getRandomValues(array);

        // URL API
        const url = new URL('https://example.com/path?foo=bar');

        return {
            urlHost: url.host,
            cryptoWorks: array[0] !== undefined
        };
    }
""")

result = ctx.call("testWebAPIs", [])
print(result)
```

## 注意事项

1. **版本兼容性**: 确保所有deno_*扩展的版本互相兼容
2. **编译体积**: 每个扩展都会增加编译后的大小
3. **复杂度**: deno_web等扩展有复杂的依赖，可能引入编译问题
4. **按需选择**: 只添加你需要的扩展，不要全部添加

## 推荐的扩展组合

### 最小集合（适合JS逆向）
```toml
deno_console = "0.192"
deno_url = "0.192"
```

### 中等集合
```toml
deno_console = "0.192"
deno_url = "0.192"
deno_web = "0.223"  # 包含 atob, btoa, TextEncoder等
```

### 完整集合（类似浏览器）
```toml
deno_console = "0.192"
deno_url = "0.192"
deno_web = "0.223"
deno_crypto = "0.206"
deno_fetch = "0.214"  # fetch API
```

## 与方案1对比

| 特性 | 方案1 (Polyfill) | 方案2 (Deno扩展) |
|------|------------------|------------------|
| 实现难度 | 简单 | 中等 |
| 异步支持 | 假的 | 真的 |
| API完整性 | 基础 | 完整 |
| 性能 | 好 | 更好 |
| 编译大小 | 小 | 大 |
| 适用场景 | 大多数JS逆向 | 需要真异步的场景 |

## 建议

对于JS逆向工程：
- **优先使用方案1（Polyfill）**：因为大多数加密JS不需要真正的异步
- 如果遇到真正需要异步的情况（例如使用了WebAssembly.instantiate等），再考虑方案2
