#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
never_jscore 异步功能测试（精简版）
"""

import never_jscore
import sys

# 设置输出编码为 UTF-8（Windows 兼容）
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def test_promise_basic():
    """测试基本 Promise 功能"""
    print("=" * 60)
    print("测试 1: 基本 Promise 功能")
    print("=" * 60)

    ctx = never_jscore.Context()

    result = ctx.evaluate("Promise.resolve(42)")
    print(f"✓ Promise.resolve(42) = {result}")
    assert result == 42

    result = ctx.evaluate("Promise.resolve(10).then(x => x * 2).then(x => x + 5)")
    print(f"✓ Promise 链 = {result}")
    assert result == 25

    result = ctx.evaluate("Promise.all([Promise.resolve(1), Promise.resolve(2), Promise.resolve(3)])")
    print(f"✓ Promise.all = {result}")
    assert result == [1, 2, 3]

    print("✅ 测试通过\n")
    del ctx


def test_async_function():
    """测试 async 函数"""
    print("=" * 60)
    print("测试 2: async 函数")
    print("=" * 60)

    ctx = never_jscore.Context()
    ctx.compile("""
        async function asyncAdd(a, b) {
            return await Promise.resolve(a + b);
        }
    """)

    result = ctx.call("asyncAdd", [5, 3])
    print(f"✓ asyncAdd(5, 3) = {result}")
    assert result == 8

    print("✅ 测试通过\n")
    del ctx


def test_concurrent():
    """测试并发执行"""
    print("=" * 60)
    print("测试 3: 并发执行")
    print("=" * 60)

    ctx = never_jscore.Context()
    ctx.compile("""
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
    del ctx


def test_no_v8_error():
    """测试无 V8 错误"""
    print("=" * 60)
    print("测试 4: 无 V8 HandleScope 错误")
    print("=" * 60)

    ctx = never_jscore.Context()
    ctx.compile("""
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
    del ctx


def test_sync_mode():
    """测试同步模式"""
    print("=" * 60)
    print("测试 5: 同步模式")
    print("=" * 60)

    ctx = never_jscore.Context()
    ctx.compile("function syncAdd(a, b) { return a + b; }")

    result = ctx.call("syncAdd", [10, 20], auto_await=False)
    print(f"✓ syncAdd(10, 20) = {result} (同步)")
    assert result == 30

    print("✅ 测试通过\n")
    del ctx


def test_multiple_contexts():
    """测试多个 Context（顺序使用+LIFO 清理）"""
    print("=" * 60)
    print("测试 6: 多个 Context (顺序使用+LIFO 清理)")
    print("=" * 60)

    # 创建并使用第一个 Context
    ctx1 = never_jscore.Context()
    ctx1.compile("function add(a, b) { return a + b; }")
    r1 = ctx1.call("add", [1, 2])
    print(f"✓ ctx1.add(1, 2) = {r1}")
    del ctx1

    # 创建并使用第二个 Context
    ctx2 = never_jscore.Context()
    ctx2.compile("function mul(a, b) { return a * b; }")
    r2 = ctx2.call("mul", [3, 4])
    print(f"✓ ctx2.mul(3, 4) = {r2}")
    del ctx2

    # 创建并使用第三个 Context
    ctx3 = never_jscore.Context()
    ctx3.compile("function sub(a, b) { return a - b; }")
    r3 = ctx3.call("sub", [10, 5])
    print(f"✓ ctx3.sub(10, 5) = {r3}")
    del ctx3

    print("✅ 测试通过（顺序创建和清理成功）\n")


def test_lifo_cleanup():
    """测试 LIFO 清理顺序"""
    print("=" * 60)
    print("测试 7: LIFO 清理（不交叉使用）")
    print("=" * 60)

    # 如果需要同时存在多个Context，必须按LIFO顺序删除
    # 但注意：创建第二个Context后，不能再使用第一个Context！
    ctx1 = never_jscore.Context()
    ctx1.compile("function f1() { return 'ctx1'; }")

    # 在创建ctx2之前完成ctx1的所有操作
    result1 = ctx1.call("f1", [])
    print(f"✓ ctx1 result: {result1}")

    # 现在创建ctx2，之后不能再使用ctx1
    ctx2 = never_jscore.Context()
    ctx2.compile("function f2() { return 'ctx2'; }")
    result2 = ctx2.call("f2", [])
    print(f"✓ ctx2 result: {result2}")

    ctx3 = never_jscore.Context()
    ctx3.compile("function f3() { return 'ctx3'; }")
    result3 = ctx3.call("f3", [])
    print(f"✓ ctx3 result: {result3}")

    # LIFO 顺序删除
    del ctx3
    del ctx2
    del ctx1

    print("✅ 测试通过（LIFO 清理成功）\n")


def run_all_tests():
    test_promise_basic()
    test_async_function()
    test_concurrent()
    test_no_v8_error()
    test_sync_mode()
    test_multiple_contexts()
    test_lifo_cleanup()

    print("=" * 60)
    print("所有测试通过！")
    print("=" * 60)
    print("✓ Promise (resolve/all)")
    print("✓ async/await 语法")
    print("✓ 自动等待 Promise")
    print("✓ 并发执行")
    print("✓ 同步/异步模式切换")
    print("✓ 无 V8 HandleScope 错误")
    print("✓ 多 Context 顺序使用")
    print("✓ LIFO 清理顺序")


if __name__ == "__main__":
    run_all_tests()
