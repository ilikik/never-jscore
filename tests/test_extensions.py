# -*- coding: utf-8 -*-
"""
测试自动注入的扩展功能
"""
import sys
import never_jscore

# Windows 控制台 UTF-8 支持
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def test_auto_injected_functions():
    """测试自动注入的全局函数"""
    print("\n=== 测试自动注入的全局函数 ===")
    ctx = never_jscore.Context()  # 默认 enable_extensions=True

    # 检测扩展是否加载
    result = ctx.evaluate("typeof __NEVER_JSCORE_EXTENSIONS_LOADED__")
    print(f"扩展加载标记: {result}")
    assert result == "boolean", "扩展应该被加载"

    # 测试 btoa/atob
    result = ctx.evaluate("btoa('hello')")
    print(f"btoa('hello'): {result}")
    assert result == "aGVsbG8=", f"Expected aGVsbG8=, got {result}"

    result = ctx.evaluate("atob('aGVsbG8=')")
    print(f"atob('aGVsbG8='): {result}")
    assert result == "hello", f"Expected hello, got {result}"

    # 测试哈希函数
    result = ctx.evaluate("md5('test')")
    print(f"md5('test'): {result}")
    assert result == "098f6bcd4621d373cade4e832627b4f6", "MD5 hash mismatch"

    result = ctx.evaluate("sha256('test')")
    print(f"sha256('test'): {result}")
    assert result == "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", "SHA256 hash mismatch"

    # 测试 URL 编码
    result = ctx.evaluate("encodeURIComponent('hello world')")
    print(f"encodeURIComponent('hello world'): {result}")
    assert result == "hello%20world", f"Expected hello%20world, got {result}"

    result = ctx.evaluate("decodeURIComponent('hello%20world')")
    print(f"decodeURIComponent('hello%20world'): {result}")
    assert result == "hello world", f"Expected 'hello world', got {result}"

    print("✓ 所有自动注入函数测试通过")
    del ctx


def test_crypto_utils_object():
    """测试 CryptoUtils 对象"""
    print("\n=== 测试 CryptoUtils 对象 ===")
    ctx = never_jscore.Context()

    # 检测 CryptoUtils 是否存在
    result = ctx.evaluate("typeof CryptoUtils")
    print(f"CryptoUtils 类型: {result}")
    assert result == "object", "CryptoUtils should be an object"

    # 测试 HMAC 函数
    result = ctx.evaluate("CryptoUtils.hmacSha256('key', 'message')")
    print(f"CryptoUtils.hmacSha256('key', 'message'): {result}")
    assert len(result) == 64, "HMAC-SHA256 应该返回 64 个字符"

    # 测试 Hex 函数
    result = ctx.evaluate("CryptoUtils.hexEncode('test')")
    print(f"CryptoUtils.hexEncode('test'): {result}")
    assert result == "74657374", f"Expected 74657374, got {result}"

    result = ctx.evaluate("CryptoUtils.hexDecode('74657374')")
    print(f"CryptoUtils.hexDecode('74657374'): {result}")
    assert result == "test", f"Expected test, got {result}"

    print("✓ CryptoUtils 对象测试通过")
    del ctx


def test_crypto_utils_chain_api():
    """测试 CryptoUtils 链式 API"""
    print("\n=== 测试 CryptoUtils 链式 API ===")
    ctx = never_jscore.Context()

    # 测试 createHash 链式调用
    result = ctx.evaluate("""
        CryptoUtils.createHash('sha256')
            .update('hello')
            .update(' ')
            .update('world')
            .digest('hex')
    """)
    print(f"createHash 链式调用结果: {result}")

    # 验证结果与直接哈希相同
    expected = ctx.evaluate("sha256('hello world')")
    assert result == expected, f"链式调用结果应该与直接调用相同"

    # 测试 createHmac 链式调用
    result = ctx.evaluate("""
        CryptoUtils.createHmac('sha256', 'secret')
            .update('data')
            .digest('hex')
    """)
    print(f"createHmac 链式调用结果: {result}")
    assert len(result) == 64, "HMAC-SHA256 应该返回 64 个字符"

    # 测试 base64 编码
    result = ctx.evaluate("""
        CryptoUtils.createHash('md5')
            .update('test')
            .digest('base64')
    """)
    print(f"createHash with base64: {result}")
    assert len(result) > 0, "Base64 编码应该返回非空字符串"

    print("✓ 链式 API 测试通过")
    del ctx


def test_pure_v8_environment():
    """测试纯净 V8 环境（不加载扩展）"""
    print("\n=== 测试纯净 V8 环境 ===")
    ctx = never_jscore.Context(enable_extensions=False)

    # 检测扩展是否未加载
    result = ctx.evaluate("typeof __NEVER_JSCORE_EXTENSIONS_LOADED__")
    print(f"扩展加载标记: {result}")
    assert result == "undefined", "扩展不应该被加载"

    # 检测 btoa 是否不存在
    result = ctx.evaluate("typeof btoa")
    print(f"btoa 类型: {result}")
    assert result == "undefined", "纯净环境中不应该有 btoa"

    # 检测 md5 是否不存在
    result = ctx.evaluate("typeof md5")
    print(f"md5 类型: {result}")
    assert result == "undefined", "纯净环境中不应该有 md5"

    # 检测 CryptoUtils 是否不存在
    result = ctx.evaluate("typeof CryptoUtils")
    print(f"CryptoUtils 类型: {result}")
    assert result == "undefined", "纯净环境中不应该有 CryptoUtils"

    # 但 ECMAScript 标准 API 应该存在
    result = ctx.evaluate("JSON.stringify({test: 1})")
    print(f"JSON.stringify 测试: {result}")
    assert result == '{"test":1}', "标准 API 应该可用"

    result = ctx.evaluate("Promise.resolve(42)")
    print(f"Promise 测试: {result}")
    assert result == 42, "Promise 应该可用"

    print("✓ 纯净 V8 环境测试通过")
    del ctx


def test_real_world_js_code():
    """测试真实场景的 JS 代码"""
    print("\n=== 测试真实场景 JS 代码 ===")
    ctx = never_jscore.Context()

    # 模拟真实的 JS 逆向场景
    ctx.compile("""
        // 常见的 API 签名算法
        function generateSignature(params) {
            // 1. 排序参数
            const keys = Object.keys(params).sort();

            // 2. 拼接参数
            const parts = keys.map(k => k + '=' + params[k]);
            const query = parts.join('&');

            // 3. 添加密钥
            const secret = 'my-secret-key';
            const message = query + '&key=' + secret;

            // 4. SHA256 哈希
            const hash = sha256(message);

            // 5. Base64 编码
            return btoa(hash);
        }

        // 常见的数据加密
        function encryptData(data) {
            const key = 'encryption-key';
            const json = JSON.stringify(data);

            // HMAC-SHA256
            const mac = CryptoUtils.hmacSha256(key, json);

            // Base64 编码
            return btoa(mac);
        }

        // URL 参数编码
        function buildUrl(base, params) {
            const parts = Object.keys(params).map(k => {
                return encodeURIComponent(k) + '=' + encodeURIComponent(params[k]);
            });
            return base + '?' + parts.join('&');
        }
    """)

    # 测试签名生成
    signature = ctx.call("generateSignature", [{"user": "test", "timestamp": "123456"}])
    print(f"生成的签名: {signature}")
    assert len(signature) > 0, "签名不应该为空"

    # 测试数据加密
    encrypted = ctx.call("encryptData", [{"secret": "data"}])
    print(f"加密的数据: {encrypted}")
    assert len(encrypted) > 0, "加密数据不应该为空"

    # 测试 URL 构建
    url = ctx.call("buildUrl", ["https://api.example.com/test", {"q": "hello world", "lang": "zh-CN"}])
    print(f"构建的 URL: {url}")
    assert "hello%20world" in url, "URL 应该包含编码后的参数"
    assert "zh-CN" in url, "URL 应该包含所有参数"

    print("✓ 真实场景测试通过")
    del ctx


if __name__ == "__main__":
    print("=" * 60)
    print("测试自动注入的扩展功能")
    print("=" * 60)

    try:
        test_auto_injected_functions()
        test_crypto_utils_object()
        test_crypto_utils_chain_api()
        test_pure_v8_environment()
        test_real_world_js_code()

        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
