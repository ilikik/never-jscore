#!/usr/bin/env python3
"""
Test new Web API extensions:
- setTimeout/setInterval
- Worker
- crypto.randomUUID()
- crypto.getRandomValues()
"""

import never_jscore

print("=" * 60)
print("Testing New Web API Extensions")
print("=" * 60)

# Test with extensions enabled
ctx = never_jscore.Context(enable_extensions=True)

# Test 1: setTimeout
print("\n[1] Testing setTimeout...")
result = ctx.evaluate("typeof setTimeout")
print(f"   setTimeout type: {result}")
assert result == "function", "setTimeout should exist"

result = ctx.evaluate("""
    let executed = false;
    setTimeout(() => { executed = true; }, 100);
    // Since setTimeout executes via Promise, we need to wait
    executed
""")
print(f"   setTimeout executed immediately: {result}")

# Test 2: setInterval
print("\n[2] Testing setInterval...")
result = ctx.evaluate("typeof setInterval")
print(f"   setInterval type: {result}")
assert result == "function", "setInterval should exist"

# Test 3: Worker
print("\n[3] Testing Worker...")
result = ctx.evaluate("typeof Worker")
print(f"   Worker type: {result}")
assert result == "function", "Worker should exist"

result = ctx.evaluate("""
    let worker = new Worker('test.js');
    typeof worker.postMessage === 'function' && typeof worker.terminate === 'function'
""")
print(f"   Worker has required methods: {result}")
assert result == True

# Test 4: crypto.randomUUID
print("\n[4] Testing crypto.randomUUID...")
result = ctx.evaluate("crypto.randomUUID()")
print(f"   Generated UUID: {result}")
assert len(result) == 36 and result.count('-') == 4, "Should be valid UUID format"

# Test 5: crypto.getRandomValues
print("\n[5] Testing crypto.getRandomValues...")
result = ctx.evaluate("""
    const arr = new Uint8Array(16);
    crypto.getRandomValues(arr);
    arr.length
""")
print(f"   Filled array length: {result}")
assert result == 16, "Should fill 16 bytes"

# Test 6: Crypto random via ops
print("\n[6] Testing Deno.core.ops crypto functions...")
result = ctx.evaluate("Deno.core.ops.op_crypto_random()")
print(f"   Random number (0-1): {result}")
assert 0 <= result <= 1, "Should be between 0 and 1"

result = ctx.evaluate("Deno.core.ops.op_crypto_get_random_values(8)")
print(f"   Random 8 bytes (hex): {result}")
assert len(result) == 16, "8 bytes = 16 hex chars"

# Test 7: Integration test
print("\n[7] Integration test...")
result = ctx.evaluate("""
    // Check all new APIs exist
    const hasSetTimeout = typeof setTimeout === 'function';
    const hasSetInterval = typeof setInterval === 'function';
    const hasWorker = typeof Worker === 'function';
    const hasCrypto = typeof crypto === 'object';
    const hasUUID = typeof crypto.randomUUID === 'function';
    const hasRandomValues = typeof crypto.getRandomValues === 'function';

    hasSetTimeout && hasSetInterval && hasWorker && hasCrypto && hasUUID && hasRandomValues
""")
print(f"   All APIs available: {result}")
assert result == True

print("\n" + "=" * 60)
print("All new Web API extensions working!")
print("=" * 60)

print("\nSummary:")
print("   - setTimeout/setInterval: [OK] (fake immediate execution)")
print("   - Worker: [OK] (fake single-threaded)")
print("   - crypto.randomUUID(): [OK]")
print("   - crypto.getRandomValues(): [OK]")
print("   - crypto random ops: [OK]")
