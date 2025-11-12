#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试随机数种子功能
"""

import never_jscore
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def test_math_random_seeded():
    """测试 Math.random() 的种子功能"""
    print("=" * 80)
    print("测试 1: Math.random() 固定种子")
    print("=" * 80)

    # 第一次：创建上下文，生成随机数序列
    print("\n第一次运行 - 种子 12345")
    ctx1 = never_jscore.Context(random_seed=12345)
    results1 = []
    for i in range(5):
        r = ctx1.evaluate("Math.random()")
        results1.append(r)
        print(f"  Round {i+1}: {r:.10f}")
    del ctx1

    # 第二次：使用相同种子，应该产生相同序列
    print("\n第二次运行 - 种子 12345")
    ctx2 = never_jscore.Context(random_seed=12345)
    results2 = []
    for i in range(5):
        r = ctx2.evaluate("Math.random()")
        results2.append(r)
        print(f"  Round {i+1}: {r:.10f}")
    del ctx2

    # 比较结果
    print("\n比较两次运行：")
    for i in range(5):
        match = "✅" if results1[i] == results2[i] else "❌"
        print(f"  Round {i+1}: {results1[i]:.10f} vs {results2[i]:.10f} {match}")

    if results1 == results2:
        print("\n✅ 相同种子产生相同的随机数序列")
    else:
        print("\n❌ 失败：相同种子应该产生相同的随机数序列")


def test_different_seeds():
    """测试不同种子产生不同随机数"""
    print("\n" + "=" * 80)
    print("测试 2: 不同种子产生不同随机数")
    print("=" * 80)

    # 第一次：种子 12345
    print("\n第一次运行 - 种子 12345")
    ctx1 = never_jscore.Context(random_seed=12345)
    results1 = []
    for i in range(5):
        r = ctx1.evaluate("Math.random()")
        results1.append(r)
        print(f"  Round {i+1}: {r:.10f}")
    del ctx1

    # 第二次：种子 54321
    print("\n第二次运行 - 种子 54321")
    ctx2 = never_jscore.Context(random_seed=54321)
    results2 = []
    for i in range(5):
        r = ctx2.evaluate("Math.random()")
        results2.append(r)
        print(f"  Round {i+1}: {r:.10f}")
    del ctx2

    # 比较结果
    print("\n比较两次运行：")
    for i in range(5):
        different = "✅" if results1[i] != results2[i] else "❌"
        print(f"  Round {i+1}: {results1[i]:.10f} vs {results2[i]:.10f} {different}")

    if results1 != results2:
        print("\n✅ 不同种子产生不同的随机数序列")
    else:
        print("\n❌ 失败：不同种子应该产生不同的随机数序列")


def test_no_seed():
    """测试不使用种子（非确定性）"""
    print("\n" + "=" * 80)
    print("测试 3: 不使用种子（非确定性）")
    print("=" * 80)

    # 第一次：无种子
    print("\n第一次运行 - 无种子")
    ctx1 = never_jscore.Context()  # No seed
    results1 = []
    for i in range(5):
        r = ctx1.evaluate("Math.random()")
        results1.append(r)
        print(f"  Round {i+1}: {r:.10f}")
    del ctx1

    # 第二次：无种子
    print("\n第二次运行 - 无种子")
    ctx2 = never_jscore.Context()  # No seed
    results2 = []
    for i in range(5):
        r = ctx2.evaluate("Math.random()")
        results2.append(r)
        print(f"  Round {i+1}: {r:.10f}")
    del ctx2

    # 比较结果
    print("\n比较两次运行：")
    for i in range(5):
        print(f"  Round {i+1}: {results1[i]:.10f} vs {results2[i]:.10f}")

    if results1 != results2:
        print("\n✅ 无种子产生不同的随机数序列（非确定性）")
    else:
        print("\n⚠️  警告：无种子但产生了相同序列（概率极低但可能）")


def test_crypto_random():
    """测试 crypto 随机数 API"""
    print("\n" + "=" * 80)
    print("测试 4: crypto 随机数 API")
    print("=" * 80)

    print("\n测试 crypto.randomUUID()")

    # 第一次：种子 99999
    print("第一次运行 - 种子 99999")
    ctx1 = never_jscore.Context(random_seed=99999)
    uuid1_list = []
    for i in range(3):
        uuid1 = ctx1.evaluate("crypto.randomUUID()")
        uuid1_list.append(uuid1)
        print(f"  UUID {i+1}: {uuid1}")
    del ctx1

    # 第二次：种子 99999
    print("\n第二次运行 - 种子 99999")
    ctx2 = never_jscore.Context(random_seed=99999)
    uuid2_list = []
    for i in range(3):
        uuid2 = ctx2.evaluate("crypto.randomUUID()")
        uuid2_list.append(uuid2)
        print(f"  UUID {i+1}: {uuid2}")
    del ctx2

    print("\n比较结果：")
    for i in range(3):
        match = "✅" if uuid1_list[i] == uuid2_list[i] else "❌"
        print(f"  UUID {i+1}: {uuid1_list[i] == uuid2_list[i]} {match}")

    if uuid1_list == uuid2_list:
        print("✅ crypto.randomUUID() 使用固定种子")
    else:
        print("❌ crypto.randomUUID() 种子未生效")

    print("\n测试 crypto.getRandomValues()")

    # 第一次：种子 77777
    print("第一次运行 - 种子 77777")
    ctx1 = never_jscore.Context(random_seed=77777)
    results1 = []
    for i in range(3):
        result = ctx1.evaluate("""
            const arr = new Uint8Array(8);
            crypto.getRandomValues(arr);
            Array.from(arr);
        """)
        results1.append(result)
        print(f"  Array {i+1}: {result}")
    del ctx1

    # 第二次：种子 77777
    print("\n第二次运行 - 种子 77777")
    ctx2 = never_jscore.Context(random_seed=77777)
    results2 = []
    for i in range(3):
        result = ctx2.evaluate("""
            const arr = new Uint8Array(8);
            crypto.getRandomValues(arr);
            Array.from(arr);
        """)
        results2.append(result)
        print(f"  Array {i+1}: {result}")
    del ctx2

    print("\n比较结果：")
    for i in range(3):
        match = "✅" if results1[i] == results2[i] else "❌"
        print(f"  Array {i+1}: {results1[i] == results2[i]} {match}")

    if results1 == results2:
        print("✅ crypto.getRandomValues() 使用固定种子")
    else:
        print("❌ crypto.getRandomValues() 种子未生效")


def test_reproducible_algorithm():
    """测试可重现的算法对比"""
    print("\n" + "=" * 80)
    print("测试 5: 可重现算法对比（实际应用场景）")
    print("=" * 80)

    js_code = """
    function generateToken(userId) {
        const random1 = Math.random();
        const random2 = Math.random();
        const hash = Math.floor((random1 + random2 + userId) * 1000000);
        return hash.toString(16);
    }

    generateToken(12345);
    """

    print("\n多次执行相同算法")

    tokens = []
    for run in range(3):
        ctx = never_jscore.Context(random_seed=42)
        token = ctx.evaluate(js_code)
        tokens.append(token)
        print(f"  Run {run+1}: {token}")
        del ctx

    if len(set(tokens)) == 1:
        print(f"\n✅ 所有运行产生相同结果: {tokens[0]}")
        print("   这对调试动态参数算法非常有用！")
    else:
        print("\n❌ 失败：相同种子应该产生相同结果")


def run_all_tests():
    """运行所有测试"""
    test_math_random_seeded()
    test_different_seeds()
    test_no_seed()
    test_crypto_random()
    test_reproducible_algorithm()

    print("\n" + "=" * 80)
    print("随机数种子功能测试完成")
    print("=" * 80)


if __name__ == "__main__":
    run_all_tests()
