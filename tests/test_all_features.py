#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Never JSCore - 完整功能测试套件
测试所有已实现的功能
"""

import never_jscore
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_crypto():
    """测试加密API"""
    print("\n【加密 API】crypto, btoa/atob, md5, sha256...")
    ctx = never_jscore.Context()
    result = ctx.evaluate("""
        JSON.stringify({
            base64: btoa('hello'),
            decoded: atob(btoa('hello')),
            md5: md5('test'),
            sha256: sha256('test').substring(0, 16) + '...'
        });
    """)
    print(f"  ✅ {result}")
    del ctx

def test_fetch():
    """测试 HTTP fetch API"""
    print("\n【HTTP API】fetch()...")
    ctx = never_jscore.Context()
    result = ctx.evaluate("""
        (async () => {
            const res = await fetch('https://httpbin.org/get?test=1');
            return { status: res.status, ok: res.ok };
        })()
    """)
    print(f"  ✅ {result}")
    del ctx

def test_wasm():
    """测试 WebAssembly"""
    print("\n【WebAssembly】WASM 支持...")
    ctx = never_jscore.Context()
    result = ctx.evaluate("""
        (async () => {
            const code = new Uint8Array([
                0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00,
                0x01, 0x07, 0x01, 0x60, 0x02, 0x7f, 0x7f, 0x01, 0x7f,
                0x03, 0x02, 0x01, 0x00,
                0x07, 0x07, 0x01, 0x03, 0x61, 0x64, 0x64, 0x00, 0x00,
                0x0a, 0x09, 0x01, 0x07, 0x00, 0x20, 0x00, 0x20, 0x01, 0x6a, 0x0b
            ]);
            const module = await WebAssembly.instantiate(code);
            return module.instance.exports.add(10, 20);
        })()
    """)
    print(f"  ✅ WASM add(10, 20) = {result}")
    del ctx

def test_require():
    """测试 require() 模块系统"""
    print("\n【模块系统】require()...")
    with open('_test_module.js', 'w') as f:
        f.write('module.exports = { value: 999 };')

    ctx = never_jscore.Context()
    result = ctx.evaluate("const m = require('./_test_module.js'); m.value")
    print(f"  ✅ require() 返回: {result}")
    del ctx

    os.remove('_test_module.js')

def test_fs_path():
    """测试文件系统和路径"""
    print("\n【文件系统】fs, path...")
    with open('_test.txt', 'w') as f:
        f.write('test content')

    ctx = never_jscore.Context()
    result = ctx.evaluate("""
        const fs = require('fs');
        const path = require('path');
        JSON.stringify({
            pathJoin: path.join('a', 'b', 'c.txt'),
            fileExists: fs.existsSync('_test.txt'),
            content: fs.readFileSync('_test.txt')
        });
    """)
    print(f"  ✅ {result}")
    del ctx

    os.remove('_test.txt')

def test_storage():
    """测试 localStorage/sessionStorage"""
    print("\n【存储 API】localStorage, sessionStorage...")
    ctx = never_jscore.Context()
    result = ctx.evaluate("""
        localStorage.setItem('key1', 'value1');
        sessionStorage.setItem('key2', 'value2');
        JSON.stringify({
            local: localStorage.getItem('key1'),
            session: sessionStorage.getItem('key2')
        });
    """)
    print(f"  ✅ {result}")
    del ctx

def test_browser_env():
    """测试浏览器环境对象"""
    print("\n【浏览器环境】navigator, location, document, window...")
    ctx = never_jscore.Context()
    result = ctx.evaluate("""
        JSON.stringify({
            navigator: navigator.platform,
            location: location.hostname,
            document: document.readyState,
            window: window.innerWidth,
            screen: screen.width
        });
    """)
    print(f"  ✅ {result}")
    del ctx

def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("  Never JSCore - 完整功能测试")
    print("=" * 70)

    tests = [
        test_crypto,
        test_fetch,
        test_wasm,
        test_require,
        test_fs_path,
        test_storage,
        test_browser_env
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ❌ 测试失败: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"  测试完成: {passed} 通过, {failed} 失败")
    print("=" * 70)

    if failed == 0:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  有 {failed} 个测试失败")

if __name__ == "__main__":
    run_all_tests()
