// 简化版异步示例 - 专注于演示功能
use anyhow::Result;
use deno_core::{extension, op2, JsRuntime, RuntimeOptions, OpState};
use std::cell::RefCell;
use std::rc::Rc;

// ============================================
// 结果存储
// ============================================

struct ResultStorage {
    value: RefCell<Option<String>>,
}

// ============================================
// 自定义 Ops
// ============================================

#[op2(fast)]
fn op_store_result(state: &mut OpState, #[string] value: String) {
    if let Some(storage) = state.try_borrow_mut::<Rc<ResultStorage>>() {
        *storage.value.borrow_mut() = Some(value);
    }
}

// 异步 op 示例
#[op2(async)]
#[string]
async fn op_async_add(a: i32, b: i32) -> String {
    // 模拟异步操作
    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
    format!("{} + {} = {}", a, b, a + b)
}

#[op2(async)]
#[string]
async fn op_decrypt(#[string] encrypted: String) -> String {
    // 模拟解密操作（适合 JS 逆向）
    tokio::time::sleep(tokio::time::Duration::from_millis(30)).await;
    encrypted.chars().rev().collect()
}

extension!(
    demo_ext,
    ops = [op_store_result, op_async_add, op_decrypt],
    options = {
        storage: Rc<ResultStorage>,
    },
    state = |state, options| {
        state.put(options.storage);
    }
);

// ============================================
// 主函数
// ============================================

fn main() -> Result<()> {
    let runtime = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()?;

    runtime.block_on(async { run_examples().await })
}

async fn run_examples() -> Result<()> {
    println!("╔═══════════════════════════════════════╗");
    println!("║   异步 Promise 支持示例 (JS逆向)    ║");
    println!("╚═══════════════════════════════════════╝\n");

    let storage = Rc::new(ResultStorage {
        value: RefCell::new(None),
    });

    let mut runtime = JsRuntime::new(RuntimeOptions {
        extensions: vec![demo_ext::init(storage.clone())],
        ..Default::default()
    });

    // ============================================
    // 示例 1: 基本 Promise 支持
    // ============================================
    println!("📝 示例 1: 基本 Promise 支持");
    println!("─────────────────────────────────────");

    runtime.execute_script(
        "<promise_basic>",
        r#"
        (async () => {
            console.log("✓ 开始异步操作");

            // 基本 Promise
            const result1 = await Promise.resolve(42);
            console.log("✓ Promise.resolve(42) =", result1);

            // Promise 链
            const result2 = await Promise.resolve(10)
                .then(x => x * 2)
                .then(x => x + 5);
            console.log("✓ Promise 链式调用 =", result2);

            // 多个 Promise 并发
            const results = await Promise.all([
                Promise.resolve("A"),
                Promise.resolve("B"),
                Promise.resolve("C")
            ]);
            console.log("✓ Promise.all =", results);

            console.log("✓ 基本 Promise 测试完成");
        })();
        "#,
    )?;

    runtime.run_event_loop(Default::default()).await?;
    println!();

    // ============================================
    // 示例 2: 调用异步 Rust 函数
    // ============================================
    println!("🔧 示例 2: 调用异步 Rust 函数");
    println!("─────────────────────────────────────");

    runtime.execute_script(
        "<async_rust_ops>",
        r#"
        (async () => {
            // 调用异步 op
            const result1 = await Deno.core.ops.op_async_add(5, 3);
            console.log("✓", result1);

            const result2 = await Deno.core.ops.op_async_add(100, 200);
            console.log("✓", result2);

            // 并发执行多个异步操作
            const results = await Promise.all([
                Deno.core.ops.op_async_add(1, 2),
                Deno.core.ops.op_async_add(3, 4),
                Deno.core.ops.op_async_add(5, 6),
            ]);

            results.forEach(r => console.log("✓", r));
        })();
        "#,
    )?;

    runtime.run_event_loop(Default::default()).await?;
    println!();

    // ============================================
    // 示例 3: JS 逆向场景 - 解密操作
    // ============================================
    println!("🎯 示例 3: JS 逆向场景 - 异步解密");
    println!("─────────────────────────────────────");

    runtime.execute_script(
        "<reverse_engineering>",
        r#"
        (async () => {
            console.log("模拟 JS 逆向解密流程...");

            // 模拟加密的数据
            const encrypted1 = "olleh";  // "hello" 反转
            const encrypted2 = "dlrow";  // "world" 反转

            // 调用异步解密函数
            const decrypted1 = await Deno.core.ops.op_decrypt(encrypted1);
            console.log(`✓ 解密 "${encrypted1}" => "${decrypted1}"`);

            const decrypted2 = await Deno.core.ops.op_decrypt(encrypted2);
            console.log(`✓ 解密 "${encrypted2}" => "${decrypted2}"`);

            // 批量解密
            const encryptedData = ['cba', 'fed', 'ihg'];
            console.log("✓ 批量解密开始...");

            const decryptedData = await Promise.all(
                encryptedData.map(data => Deno.core.ops.op_decrypt(data))
            );

            encryptedData.forEach((enc, i) => {
                console.log(`  "${enc}" => "${decryptedData[i]}"`);
            });

            console.log("✓ 所有解密操作完成");
        })();
        "#,
    )?;

    runtime.run_event_loop(Default::default()).await?;
    println!();

    // ============================================
    // 示例 4: 复杂异步流程
    // ============================================
    println!("⚡ 示例 4: 复杂异步流程（链式+并发）");
    println!("─────────────────────────────────────");

    runtime.execute_script(
        "<complex_async>",
        r#"
        (async () => {
            // 模拟完整的逆向分析流程
            async function analyzeEncryptedData(data) {
                // 步骤1: 解密
                const decrypted = await Deno.core.ops.op_decrypt(data);

                // 步骤2: 处理
                const processed = decrypted.toUpperCase();

                // 步骤3: 计算
                const result = await Deno.core.ops.op_async_add(
                    processed.length,
                    10
                );

                return {
                    original: data,
                    decrypted: decrypted,
                    processed: processed,
                    result: result
                };
            }

            // 处理多个加密数据
            const dataList = ['elpmas', 'atad', 'tset'];

            const results = await Promise.all(
                dataList.map(d => analyzeEncryptedData(d))
            );

            results.forEach(r => {
                console.log(`✓ 分析: ${r.original} -> ${r.decrypted} -> ${r.processed}`);
                console.log(`  结果: ${r.result}`);
            });

            console.log("✓ 复杂流程完成");
        })();
        "#,
    )?;

    runtime.run_event_loop(Default::default()).await?;
    println!();

    // ============================================
    // 示例 5: 错误处理
    // ============================================
    println!("🛡️  示例 5: 异步错误处理");
    println!("─────────────────────────────────────");

    runtime.execute_script(
        "<error_handling>",
        r#"
        (async () => {
            try {
                const result = await Promise.resolve(100);
                console.log("✓ 正常执行:", result);

                // 测试错误处理
                await Promise.reject("模拟错误");
            } catch (e) {
                console.log("✓ 捕获异常:", e);
            }

            // Promise.race 示例（不使用 setTimeout）
            const raceResult = await Promise.race([
                Promise.resolve("快"),
                new Promise(resolve => {
                    // 使用延迟 resolve
                    let count = 0;
                    while (count < 1000000) count++;
                    resolve("慢");
                })
            ]);
            console.log("✓ Promise.race 结果:", raceResult);

            console.log("✓ 错误处理测试完成");
        })();
        "#,
    )?;

    runtime.run_event_loop(Default::default()).await?;

    println!("\n╔═══════════════════════════════════════╗");
    println!("║      所有示例执行完成！ ✨          ║");
    println!("╚═══════════════════════════════════════╝");

    println!("\n📚 功能总结:");
    println!("✓ 完整支持 Promise 和 async/await");
    println!("✓ 支持异步 Rust ops（适合耗时操作）");
    println!("✓ 支持 Promise.all/race 等组合器");
    println!("✓ 完整的错误处理支持");
    println!("✓ 适合 JS 逆向分析中的异步场景");
    println!("\n💡 适用场景:");
    println!("  - 解密加密的 JS 代码");
    println!("  - 处理异步加载的混淆代码");
    println!("  - 模拟网络请求和响应");
    println!("  - 批量分析多个 JS 文件");

    Ok(())
}
