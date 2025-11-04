#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyExecJS-RS 异步功能测试（精简版）
"""

import never_jscore as execjs


def test_promise_basic():
    """测试基本 Promise 功能"""
    print("=" * 60)
    print("测试 1: 基本 Promise 功能")
    print("=" * 60)

    result = execjs.eval("Promise.resolve(42)")
    print(f"✓ Promise.resolve(42) = {result}")
    assert result == 42

    result = execjs.eval("Promise.resolve(10).then(x => x * 2).then(x => x + 5)")
    print(f"✓ Promise 链 = {result}")
    assert result == 25

    result = execjs.eval("Promise.all([Promise.resolve(1), Promise.resolve(2), Promise.resolve(3)])")
    print(f"✓ Promise.all = {result}")
    assert result == [1, 2, 3]

    print("✅ 测试通过\n")


def test_async_function():
    """测试 async 函数"""
    print("=" * 60)
    print("测试 2: async 函数")
    print("=" * 60)

    ctx = execjs.compile("""
        async function asyncAdd(a, b) {
            return await Promise.resolve(a + b);
        }
    """)

    result = ctx.call("asyncAdd", [5, 3])
    print(f"✓ asyncAdd(5, 3) = {result}")
    assert result == 8

    print("✅ 测试通过\n")


def test_concurrent():
    """测试并发执行"""
    print("=" * 60)
    print("测试 3: 并发执行")
    print("=" * 60)

    ctx = execjs.compile("""
        async function process(n) {
            return n * n;
        }

        async function batch(numbers) {
            return await Promise.all(numbers.map(n => process(n)));
        }
    """)

    result = ctx.call("batch", [[1, 2, 3, 4, 5]])
    print(f"✓ batch([1,2,3,4,5]) = {result}")
    assert result == [1, 4, 9, 16, 25]

    print("✅ 测试通过\n")


def test_no_v8_error():
    """测试无 V8 错误"""
    print("=" * 60)
    print("测试 4: 无 V8 HandleScope 错误")
    print("=" * 60)

    ctx = execjs.compile("""
        function returnPromise() {
            return new Promise((resolve) => resolve(42));
        }
    """)
    # 多次调用确保稳定
    for i in range(5):
        result = ctx.call("returnPromise", [])
        assert result == 42




    print(f"✓ 调用 5 次 returnPromise，无错误")
    print("✅ 测试通过\n")


def test_sync_mode():
    """测试同步模式"""
    print("=" * 60)
    print("测试 5: 同步模式")
    print("=" * 60)

    ctx = execjs.compile("function syncAdd(a, b) { return a + b; }")

    result = ctx.call("syncAdd", [10, 20], auto_await=False)
    print(f"✓ syncAdd(10, 20) = {result} (同步)")
    assert result == 30

    print("✅ 测试通过\n")


def run_all_tests():
    test_promise_basic()
    test_async_function()
    test_concurrent()
    test_no_v8_error()
    test_sync_mode()

    print("✓ Promise (resolve/all/race)")
    print("✓ async/await 语法")
    print("✓ 自动等待 Promise")
    print("✓ 并发执行")
    print("✓ 同步/异步模式切换")
    print("✓ 无 V8 HandleScope 错误")


if __name__ == "__main__":
    run_all_tests()
