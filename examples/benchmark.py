import execjs
from py_mini_racer import py_mini_racer
import never_jscore
import time

js_code = """
function add(a, b) {
  return a + b;
}
function sumArray(arr) {
  let s = 0;
  for (let i = 0; i < arr.length; i++) s += arr[i];
  return s;
}
"""

with open('demo.js','r',encoding='utf-8')as f:
    js_code2 = f.read()

arr = list(range(100))
iterations = 1000

print("=== execjs ===")
# ctx1 = execjs.compile(js_code)
#
# start = time.time()
# for _ in range(iterations):
#     ctx1.call('add', 1, 2)
# end = time.time()
# print(f"add() {iterations}次耗时: {end - start:.4f}s")
#
# start = time.time()
# for _ in range(iterations):
#     ctx1.call('sumArray', arr)
# end = time.time()
# print(f"sumArray() {iterations}次耗时: {end - start:.4f}s")
ctx1 = execjs.compile(js_code2)
start = time.time()
for _ in range(iterations):
    ctx1.call('get_token','5fffa6895ac0748d8c76e61c1f4066d73d6501cf63c3221234')
    # ctx1.call("batch", [[1, 2, 3, 4, 5]])
    # ctx1.call("main")
end = time.time()
print(f"get_token() {iterations}次耗时: {end - start:.4f}s")


print("\n=== py_mini_racer ===")
ctx2 = py_mini_racer.MiniRacer()
# ctx2.eval(js_code)
#
# start = time.time()
# for _ in range(iterations):
#     ctx2.call('add', 1, 2)
# end = time.time()
# print(f"add() {iterations}次耗时: {end - start:.4f}s")
#
# start = time.time()
# for _ in range(iterations):
#     ctx2.call('sumArray', arr)
# end = time.time()
# print(f"sumArray() {iterations}次耗时: {end - start:.4f}s")

ctx2.eval(js_code2)
ctx2.eval(js_code)
start = time.time()
for _ in range(iterations):
    ctx2.call('get_token', '5fffa6895ac0748d8c76e61c1f4066d73d6501cf63c3221234')
    # ctx2.call("batch", [[1, 2, 3, 4, 5]])
end = time.time()
print(f"get_token() {iterations}次耗时: {end - start:.4f}s")

print("\n=== never_jscore ===")
ctx3 = never_jscore.Context()
ctx3.compile(js_code2)
start = time.time()
for _ in range(iterations):
    ctx3.call('get_token',['5fffa6895ac0748d8c76e61c1f4066d73d6501cf63c3221234'])
    # ctx3.call("batch", [[1, 2, 3, 4, 5]])
end = time.time()
print(f"get_token() {iterations}次耗时: {end - start:.4f}s")




