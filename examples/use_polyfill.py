"""
示例：如何在never_jscore中注入Web API polyfill

这个例子展示了如何加载polyfill来支持atob, btoa, setTimeout等Web API
"""

import never_jscore
from pathlib import Path
import time

# 读取polyfill文件
polyfill_path = Path(__file__).parent / "polyfill_example.js"
with open(polyfill_path, 'r', encoding='utf-8') as f:
    polyfill_code = f.read()


# ============================================
# 方式1: 将polyfill和业务代码一起编译
# ============================================
print("方式1: 组合编译")
print("=" * 50)

combined_code = polyfill_code + """

// 现在可以使用Web API了
function testAPIs() {
    // 测试atob/btoa
    const encoded = btoa("Hello World");
    const decoded = atob(encoded);

    // 测试console
    console.log("This is a log");

    // 测试setTimeout (注意：这不是真正的异步)
    const timerId = setTimeout(() => {}, 1000);
    clearTimeout(timerId);

    return {
        encoded: encoded,
        decoded: decoded,
        cryptoAvailable: typeof crypto !== 'undefined',
        performanceAvailable: typeof performance !== 'undefined'
    };
}
"""

ctx1 = never_jscore.Context()
ctx1.compile(combined_code)
result = ctx1.call("testAPIs", [])
print(f"测试结果: {result}")
print()


# ============================================
# 方式2: 先编译polyfill，再添加业务代码
# ============================================
print("方式2: 分步编译")
print("=" * 50)

# 首先加载polyfill
ctx2 = never_jscore.Context()
ctx2.compile(polyfill_code)

# 然后在同一个context中执行业务代码
ctx2.eval("""
    function encryptData(data) {
        // 使用atob/btoa进行简单的编码
        return btoa(data);
    }

    function decryptData(data) {
        return atob(data);
    }
""")

# 调用加密函数
encrypted = ctx2.call("encryptData", ["敏感数据123"])
print(f"加密后: {encrypted}")

decrypted = ctx2.call("decryptData", [encrypted])
print(f"解密后: {decrypted}")
print()


# ============================================
# 方式3: 测试实际的JS逆向场景
# ============================================
print("方式3: 模拟JS逆向场景")
print("=" * 50)

# 模拟从网站扒下来的加密JS（通常会使用各种Web API）
reverse_js = polyfill_code + """
// 这是从某个网站扒下来的加密函数（示例）
function generateSign(params) {
    // 很多网站的加密函数会用到atob/btoa
    const timestamp = Date.now();
    const nonce = Math.random().toString(36).substring(7);

    // 构造签名字符串
    const signStr = params + '|' + timestamp + '|' + nonce;

    // 使用btoa进行编码（很多网站用这个做简单加密）
    const encoded = btoa(signStr);

    // 可能还会用到URL编码
    const urlEncoded = encodeURIComponent(encoded);

    return {
        sign: urlEncoded,
        timestamp: timestamp,
        nonce: nonce
    };
}

// 有些网站会检查环境
function checkEnvironment() {
    return {
        hasWindow: typeof window !== 'undefined',
        hasDocument: typeof document !== 'undefined',
        hasNavigator: typeof navigator !== 'undefined',
        hasConsole: typeof console !== 'undefined',
        hasCrypto: typeof crypto !== 'undefined',
        hasAtob: typeof atob !== 'undefined'
    };
}
"""

ctx3 = never_jscore.Context()
ctx3.compile(reverse_js)

# 生成签名
sign_result = ctx3.call("generateSign", ["user=123&token=abc"])
print(f"生成的签名: {sign_result}")

# 检查环境
env_check = ctx3.call("checkEnvironment", [])
print(f"环境检查: {env_check}")
print()


# ============================================
# 性能测试
# ============================================
print("性能测试: 使用polyfill vs 不使用")
print("=" * 50)

# 测试1: 不使用polyfill（只用纯JS）
simple_ctx = never_jscore.Context()
simple_ctx.compile("""
    function simpleCalc(n) {
        return n * 2 + 1;
    }
""")

start = time.time()
for i in range(1000):
    simple_ctx.call("simpleCalc", [i])
time1 = (time.time() - start) * 1000

print(f"纯JS (1000次调用): {time1:.2f}ms")

# 测试2: 使用polyfill
polyfill_ctx = never_jscore.Context()
polyfill_ctx.compile(polyfill_code + """
    function calcWithPolyfill(n) {
        // 使用一些polyfill的功能
        const encoded = btoa(String(n));
        const decoded = atob(encoded);
        return parseInt(decoded) * 2 + 1;
    }
""")

start = time.time()
for i in range(1000):
    polyfill_ctx.call("calcWithPolyfill", [i])
time2 = (time.time() - start) * 1000

print(f"使用polyfill (1000次调用): {time2:.2f}ms")
print(f"性能差异: {((time2 - time1) / time1 * 100):.1f}%")

# 清理 - 按照LIFO顺序删除（后创建的先删除）
del polyfill_ctx
del simple_ctx
del ctx3
del ctx2
del ctx1

print("\n结论: polyfill会增加一些开销，但对于JS逆向来说完全可以接受")
