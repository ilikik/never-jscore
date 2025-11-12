# never_jscore 中文文档

基于 Deno Core (V8) 的高性能 Python JavaScript 执行引擎，**专为 JS 逆向工程和补环境优化**。
努力成为PyExecJS上位替代品,目的仅为了学习技术研究,请勿用于违法用途,后果自负


加v进交流群: xu970821582
## 项目特点

- ⚡ **极致性能**:
  - 使用 Rust + Deno Core (V8 引擎)
  - 实例化 Context 复用优化
  - **比 PyExecJS 快 100-300倍**
  - **与 PyMiniRacer 性能相当，部分场景更快**
- 🔄 **Promise/async 支持**:
  - 完整支持 Promise 和 async/await
  - 自动等待异步结果
  - **唯一高性能 Promise 方案**（PyMiniRacer 不支持）
- 🎣 **Hook 拦截与提前返回** (v2.2.2):
  - 支持在任意位置终止JS执行并返回结果
  - Hook XMLHttpRequest.send 拦截加密数据
  - Hook 加密函数获取中间值
  - 完美适配 JS 逆向工程场景
- 🎲 **确定性随机数** (v2.3.0):
  - 支持固定随机数种子（random_seed）
  - Math.random、crypto.randomUUID、crypto.getRandomValues 全部可控
  - 相同种子产生相同随机数序列
  - 完美用于调试动态参数算法和可重现测试
- 🌐 **完整 Web API 扩展** (v2.2.0):
  - ✅ **Node.js APIs**: require()、fs、path、fetch()
  - ✅ **浏览器存储**: localStorage、sessionStorage
  - ✅ **浏览器环境(简易实现)**: navigator、location、document、window、screen
  - ✅ **URL 处理**: URL、URLSearchParams
  - ✅ **表单数据**: FormData
  - ✅ **事件系统**: Event、EventTarget
  - ✅ **网络请求**: fetch()、XMLHttpRequest
  - ✅ **性能监控** (v2.2.1): performance.now()、performance.mark()、performance.measure()
  - ✅ **Crypto APIs**: Base64、MD5、SHA1/256/512、HMAC、Hex
  - ✅ **URL 编码**: encodeURIComponent、encodeURI 等
  - ✅ **定时器**: setTimeout、setInterval（立即执行版本）
  - ✅ **随机数**: crypto.randomUUID()、crypto.getRandomValues()
  - 🎯 专为 JS 逆向和补环境设计，无需额外 polyfill
- 📦 **上下文隔离**: 每个 Context 独立的 V8 执行环境，互不干扰
- 🎯 **py_mini_racer 兼容**: API 设计类似 py_mini_racer，实例化使用
- 🧹 **自动内存管理**: 基于 Rust 的自动垃圾回收，无内存泄漏
- 🛡️ **类型安全**: 提供完整的类型提示（.pyi 文件）


## 特性对比表

| 特性 | never_jscore | PyExecJS | PyMiniRacer | js2py | dukpy |
|------|--------------|----------|-------------|-------|-------|
| 引擎 | V8           | Node/V8等 | V8 | 纯Python | Duktape |
| Promise | ✅ 完整         | ❌ | ⚠️ 有限 | ❌ | ❌ |
| async/await | ✅            | ❌ | ⚠️ | ❌ | ❌ |
| require() | ✅ 完整         | ✅ | ❌ | ❌ | ❌ |
| fetch() | ✅            | ❌ | ❌ | ❌ | ❌ |
| localStorage | ✅            | ❌ | ❌ | ❌ | ❌ |
| 浏览器环境 | ️ ⚠️大部分      | ❌ | ❌ | ⚠️ 部分 | ❌ |
| 性能 | ⚡⚡⚡⚡⚡        | ⚡⚡ | ⚡⚡⚡⚡⚡ | ⚡ | ⚡⚡⚡ |
| 安装难度 | 简单           | 需Node.js | 简单 | 简单 | 简单 |
| 上下文复用 | ✅            | ✅ | ✅ | ✅ | ✅ |
| 类型转换 | 自动           | 自动 | 自动 | 自动 | 自动 |
| ES6+ | ✅ 完整         | ✅ | ✅ | ⚠️ 部分 | ⚠️ 部分 |

---

## 常见问题

### Q: 为什么 PyMiniRacer 在某些测试中更快？
A: PyMiniRacer 是 V8 的直接绑定，开销最小。never_jscore 使用 rust开发以及Deno Core，有轻量级包装层，但提供了更多功能（如 Promise 支持）。

### Q: 什么时候选择 never_jscore？
A: 当你需要:
- Promise/async 支持（现代 JS 库）
- 高性能 + Rust 稳定性
- 完整的 Node.js 环境（require、fs、path）
- 浏览器环境模拟（补环境）
- fetch() 网络请求
- localStorage/sessionStorage
- JS 逆向工程

### Q: PyExecJS 为什么这么慢？
A: PyExecJS 通过进程调用外部 JS 运行时，每次都有进程通信开销。



## 可用测试文件
- [benchmark.py](examples/benchmark.py) - 性能基准测试
- [hook_examples.py](examples/hook_examples.py) - Hook拦截使用示例（v2.2.2 新增）
- [test_async_simple.py](tests/test_async_simple.py) - 异步功能测试
- [test_extensions.py](tests/test_extensions.py) - 扩展 API 测试
- [test_new_apis.py](tests/test_new_apis.py) - 新 API 测试
- [test_all_features.py](tests/test_all_features.py) - 完整功能测试套件
- [test_browser_apis.py](tests/test_browser_apis.py) - 浏览器 API 测试
- [test_high_priority_apis.py](tests/test_high_priority_apis.py) - 高优先级 API 测试
- [test_hook_interception.py](tests/test_hook_interception.py) - Hook拦截功能测试（v2.2.2 新增）
- [test_random_seed.py](tests/test_random_seed.py) - 随机数种子功能测试（v2.3.0 新增）
- [test_wasm.py](tests/test_wasm.py) - WebAssembly 测试
- [use_polyfill.py](examples/use_polyfill.py) - Polyfill 使用示例




## 性能对比
![img.png](img.png)

| 测试项目                         | never_jscore   | PyMiniRacer | PyExecJS |
|------------------------------|----------------|------------|----------|
| 简单计算                         | 0.007ms        | 0.005ms    | 2.3ms    |
| 字符串操作                        | **0.004ms** 🏆 | 0.008ms    | 2.3ms    |
| 数组操作                         | **0.004ms** 🏆 | 0.006ms    | 2.3ms    |
| 复杂算法参数生成<br/>(1000次循环 )<br/>[benchmark.py](examples/benchmark.py) | **0.0111s** 🏆 | 0.0383s    | 69.4735s |
| Promise                      | **✅ 0.003ms**  | ❌ 不支持      | ❌ 不支持    |


## 安装
```bash
pip install never-jscore
```

### 从源码安装

```bash
pip install maturin
maturin develop --release
```

## 快速开始

### 0. 创建 Context（启用扩展）

```python
import never_jscore

# 启用 Web API 扩展（默认，推荐用于 JS 逆向）
ctx = never_jscore.Context(enable_extensions=True)

# 或禁用扩展（纯净 V8 环境）
ctx = never_jscore.Context(enable_extensions=False)

# 启用日志输出（调试模式，v2.2.0+）
ctx = never_jscore.Context(enable_logging=True)

# 使用固定随机数种子（确定性执行，v2.3.0+）
ctx = never_jscore.Context(random_seed=12345)

# 组合使用
ctx = never_jscore.Context(
    enable_extensions=True,  # 启用扩展
    enable_logging=False,    # 关闭日志
    random_seed=42          # 固定种子
)
```

### 1. 基本用法（实例化 Context）

```python
import never_jscore

# 创建 JavaScript 执行上下文
ctx = never_jscore.Context()

# 一次性求值
result = ctx.evaluate("1 + 2 + 3")
print(result)  # 6

# 字符串操作
result = ctx.evaluate("'Hello'.toUpperCase()")
print(result)  # HELLO

# 数组操作
result = ctx.evaluate("[1, 2, 3].map(x => x * 2)")
print(result)  # [2, 4, 6]
```

### 2. 编译和调用

```python
import never_jscore

# 创建上下文
ctx = never_jscore.Context()

# 编译 JavaScript 代码
ctx.compile("""
    function add(a, b) {
        return a + b;
    }

    function greet(name) {
        return "Hello, " + name + "!";
    }
""")

# 调用函数
print(ctx.call("add", [5, 3]))        # 8
print(ctx.call("greet", ["World"]))   # Hello, World!
```

### 3. 异步支持（Promise/async/await）

```python
import never_jscore

ctx = never_jscore.Context()

# async 函数
ctx.compile("""
    async function fetchData(id) {
        // 模拟异步操作
        return await Promise.resolve({id: id, name: "User" + id});
    }
""")

# Promise 自动等待
result = ctx.evaluate("Promise.resolve(42)")
print(result)  # 42

result = ctx.call("fetchData", [123])
print(result)  # {'id': 123, 'name': 'User123'}

# Promise 链
result = ctx.evaluate("""
    Promise.resolve(10)
        .then(x => x * 2)
        .then(x => x + 5)
""")
print(result)  # 25

# Promise.all 并发
result = ctx.evaluate("""
    Promise.all([
        Promise.resolve(1),
        Promise.resolve(2),
        Promise.resolve(3)
    ])
""")
print(result)  # [1, 2, 3]
```

### 4. 上下文状态管理

```python
import never_jscore

ctx = never_jscore.Context()
ctx.compile("""
    var counter = 0;

    function increment() {
        return ++counter;
    }

    function getCounter() {
        return counter;
    }
""")

print(ctx.call("increment", []))  # 1
print(ctx.call("increment", []))  # 2
print(ctx.call("getCounter", []))  # 2
```

### 5. 复杂对象处理

```python
import never_jscore

ctx = never_jscore.Context()
ctx.compile("""
    function processUser(name, age, tags) {
        return {
            name: name,
            age: age,
            isAdult: age >= 18,
            tags: tags,
            summary: name + ' (' + age + '岁)'
        };
    }
""")

result = ctx.call("processUser", ["张三", 25, ["Python", "JavaScript"]])
print(result)
# {
#     'name': '张三',
#     'age': 25,
#     'isAdult': True,
#     'tags': ['Python', 'JavaScript'],
#     'summary': '张三 (25岁)'
# }
```

### 6. 性能监控

```python
import never_jscore

ctx = never_jscore.Context()
ctx.compile("function compute(n) { return n * n; }")

# 执行多次
for i in range(100):
    ctx.call("compute", [i])

# 查看统计
stats = ctx.get_stats()
print(f"执行次数: {stats[0]}")  # 100

# 请求垃圾回收（可选）
ctx.gc()

# 重置统计
ctx.reset_stats()
```

### 7. Hook拦截与提前返回（v2.2.2 新增）

```python
import never_jscore

ctx = never_jscore.Context()

# 示例1: Hook XMLHttpRequest.send 拦截加密数据
result = ctx.evaluate("""
    (async () => {
        // 定义加密函数
        function encrypt(data) {
            return btoa(JSON.stringify(data));
        }

        // Hook XMLHttpRequest.send
        const originalSend = XMLHttpRequest.prototype.send;
        XMLHttpRequest.prototype.send = function(data) {
            // 拦截到加密后的数据，立即返回到Python
            __neverjscore_return__({
                method: this._method,
                url: this._url,
                encrypted_data: data  // 拦截的加密数据
            });

            // 下面的代码不会执行
            originalSend.call(this, data);
        };

        // 执行加密和发送流程
        const sensitiveData = {
            username: 'test@example.com',
            password: 'secret123',
            timestamp: Date.now()
        };

        const encrypted = encrypt(sensitiveData);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://api.example.com/login');
        xhr.send(encrypted);  // 在这里被拦截并提前返回

        // 不会执行到这里
        return { status: 'sent' };
    })()
""")

print(f"拦截到的URL: {result['url']}")
print(f"拦截到的加密数据: {result['encrypted_data']}")

# 示例2: Hook加密函数获取中间值
result = ctx.evaluate("""
    function multiLayerEncrypt(data) {
        const layer1 = btoa(data);
        const layer2 = md5(layer1);

        // 在第二层加密后立即返回
        $return({
            layer: 2,
            result: layer2,
            original: data
        });

        // 第三层不会执行
        const layer3 = sha256(layer2);
        return layer3;
    }

    multiLayerEncrypt('sensitive_data');
""")

print(f"拦截到第{result['layer']}层加密: {result['result']}")

# 示例3: 条件拦截
result = ctx.evaluate("""
    function processData(data) {
        // 只有当数据包含目标标记时才拦截
        if (data.includes('TARGET')) {
            $exit({
                found: true,
                data: data,
                position: data.indexOf('TARGET')
            });
        }
        return data.toUpperCase();
    }

    processData('normal data');
    processData('this contains TARGET marker');  // 在这里拦截
    processData('will not reach here');  // 不会执行
""")

print(f"条件拦截结果: {result}")
```

**Hook API说明：**
- `__neverjscore_return__(value)` - 完整函数名
- `$return(value)` - 简短别名（推荐）
- `$exit(value)` - 替代别名

**功能特性：**
- ✅ 立即终止JavaScript执行
- ✅ 将拦截到的值返回到Python
- ✅ 跳过后续所有代码（包括异步操作）
- ✅ 支持同步和异步两种模式
- ✅ 自动处理JSON序列化

**适用场景：**
- 🎯 Hook加密函数获取中间值
- 🎯 拦截XMLHttpRequest.send获取请求数据
- 🎯 提取Akamai等反爬虫的传感器数据
- 🎯 在满足条件时提前终止并返回结果

更多示例请查看 [hook_examples.py](examples/hook_examples.py)

### 8. 确定性随机数（v2.3.0 新增）

```python
import never_jscore

# 使用固定种子创建上下文（确定性执行）
ctx = never_jscore.Context(random_seed=12345)

# Math.random() 会基于种子生成确定性随机数
result = ctx.evaluate("""
    const r1 = Math.random();  // 0.8831156266...
    const r2 = Math.random();  // 0.5465919174...
    const r3 = Math.random();  // 0.2821271724...
    [r1, r2, r3]
""")
print(result)  # [0.8831156266, 0.5465919174, 0.2821271724]

# 使用相同种子的另一个上下文会产生相同的随机数序列
ctx2 = never_jscore.Context(random_seed=12345)
result2 = ctx2.evaluate("""
    const r1 = Math.random();
    const r2 = Math.random();
    const r3 = Math.random();
    [r1, r2, r3]
""")
print(result2)  # [0.8831156266, 0.5465919174, 0.2821271724] - 完全相同！

# crypto API 也遵守种子
ctx3 = never_jscore.Context(random_seed=99999)
uuid1 = ctx3.evaluate("crypto.randomUUID()")
print(uuid1)  # "a2c9d035-05e8-416d-9395-58db68d61c19"

# 相同种子产生相同的 UUID
ctx4 = never_jscore.Context(random_seed=99999)
uuid2 = ctx4.evaluate("crypto.randomUUID()")
print(uuid2)  # "a2c9d035-05e8-416d-9395-58db68d61c19" - 相同！

# 实际应用：调试动态参数算法
ctx5 = never_jscore.Context(random_seed=42)
result = ctx5.evaluate("""
    function generateToken(userId) {
        const random1 = Math.random();
        const random2 = Math.random();
        const hash = Math.floor((random1 + random2 + userId) * 1000000);
        return hash.toString(16);
    }

    generateToken(12345);
""")
print(result)  # "2dfe3be76"

# 再次运行，结果完全相同（方便调试）
ctx6 = never_jscore.Context(random_seed=42)
result2 = ctx6.evaluate("""
    function generateToken(userId) {
        const random1 = Math.random();
        const random2 = Math.random();
        const hash = Math.floor((random1 + random2 + userId) * 1000000);
        return hash.toString(16);
    }

    generateToken(12345);
""")
print(result2)  # "2dfe3be76" - 完全相同！

# 不使用种子时，随机数是非确定性的（默认行为）
ctx7 = never_jscore.Context()  # 无 random_seed
random1 = ctx7.evaluate("Math.random()")
random2 = ctx7.evaluate("Math.random()")
print(f"非确定性: {random1} != {random2}")  # 每次运行都不同
```

**支持的随机数 API：**
- ✅ `Math.random()` - 标准随机数（0 到 1）
- ✅ `crypto.randomUUID()` - UUID v4 生成
- ✅ `crypto.getRandomValues()` - 随机字节数组

**使用场景：**
- 🎯 调试包含随机数的加密算法
- 🎯 可重现的测试用例
- 🎯 对比不同参数下的算法行为
- 🎯 JS 逆向中的动态参数分析
- 🎯 Akamai 等反爬虫算法的确定性执行

更多示例请查看 [test_random_seed.py](tests/test_random_seed.py)

## API 参考

### Context 类

#### `never_jscore.Context(enable_extensions: bool = True, enable_logging: bool = False, random_seed: int = None)`

创建一个新的 JavaScript 执行上下文。

**参数**:
- `enable_extensions` (可选): 是否启用内置 Web API 扩展（默认 True）
  - `True`: 启用 Crypto、URL 编码、setTimeout、Worker 等扩展
  - `False`: 纯净 V8 环境，只有 ECMAScript 标准 API
- `enable_logging` (可选): 是否启用操作日志输出（默认 False）
  - `True`: 输出所有扩展操作的日志（用于调试）
  - `False`: 不输出日志（推荐生产环境）
- `random_seed` (可选): 随机数种子（默认 None）
  - `None`: 使用系统随机数（非确定性）
  - `int`: 使用固定种子（确定性），所有随机数 API 将基于此种子生成

**返回**: Context 对象

**示例**:
```python
# 启用扩展（默认，推荐用于 JS 逆向）
ctx = never_jscore.Context()
ctx = never_jscore.Context(enable_extensions=True)

# 禁用扩展（纯净 V8）
ctx = never_jscore.Context(enable_extensions=False)

# 启用日志（调试模式）
ctx = never_jscore.Context(enable_logging=True)

# 使用固定种子（确定性随机数）
ctx = never_jscore.Context(random_seed=12345)

# 组合使用
ctx = never_jscore.Context(enable_extensions=True, enable_logging=False, random_seed=42)
```

#### `compile(code: str) -> None`

编译 JavaScript 代码并加入全局作用域。

**参数**:
- `code`: JavaScript 代码字符串

**示例**:
```python
ctx.compile('''
    function add(a, b) { return a + b; }
''')
```

#### `eval(code: str, return_value: bool = False, auto_await: bool = True) -> Any`

执行代码并将其加入全局作用域。

**参数**:
- `code`: JavaScript 代码字符串
- `return_value`: 是否返回最后表达式的值（默认 False）
- `auto_await`: 是否自动等待 Promise（默认 True）

**返回**: 如果 return_value=True，返回执行结果；否则返回 None

**示例**:
```python
ctx.eval("var x = 10;")  # 添加到全局作用域
result = ctx.eval("x * 2", return_value=True)  # 返回 20
```

#### `evaluate(code: str, auto_await: bool = True) -> Any`

执行代码并返回结果（不影响全局作用域）。

**参数**:
- `code`: JavaScript 代码字符串
- `auto_await`: 是否自动等待 Promise（默认 True）

**返回**: 表达式的值

**示例**:
```python
result = ctx.evaluate("1 + 2 + 3")  # 6
result = ctx.evaluate("Promise.resolve(42)")  # 42
```

#### `call(name: str, args: list, auto_await: bool = True) -> Any`

调用 JavaScript 函数。

**参数**:
- `name`: 函数名称
- `args`: 参数列表
- `auto_await`: 是否自动等待 Promise（默认 True）

**返回**: 函数返回值

**示例**:
```python
result = ctx.call("add", [1, 2])
result = ctx.call("asyncFunc", [arg], auto_await=True)
```

#### `gc() -> None`

请求 V8 垃圾回收。

**注意**: 这只是提示，V8 会根据自己的策略决定是否执行。在大多数情况下无需手动调用。

#### `get_stats() -> tuple[int]`

获取执行统计信息。

**返回**: `(exec_count,)` 执行次数元组

#### `reset_stats() -> None`

重置统计信息。

## 类型转换

Python 和 JavaScript 之间的类型自动转换：

| Python 类型 | JavaScript 类型 | 说明 |
|------------|----------------|------|
| None       | null           | 空值 |
| bool       | boolean        | 布尔值 |
| int        | number         | 整数 |
| float      | number         | 浮点数 |
| str        | string         | 字符串 |
| list       | Array          | 数组 |
| dict       | Object         | 对象 |

**示例**:
```python
# Python -> JavaScript
ctx.call("func", [None, True, 42, 3.14, "hello", [1, 2], {"key": "value"}])

# JavaScript -> Python
result = ctx.evaluate("{name: 'John', age: 30}")  # dict
result = ctx.evaluate("[1, 2, 3]")  # list
result = ctx.evaluate("null")  # None
```

## 使用限制

### ⚠️ 多 Context 限制（重要！）

由于 V8 引擎的 thread-local storage 限制和内存管理机制，**多个 Context 必须遵循特定的使用模式**。

#### 限制 1: 不能交叉使用

**一旦创建了第二个 Context，就不能再使用第一个 Context！**

```python
# ❌ 错误用法：交叉使用会崩溃
ctx1 = never_jscore.Context()
ctx1.compile("function f1() { return 1; }")
result1 = ctx1.call("f1", [])  # OK

ctx2 = never_jscore.Context()
ctx2.compile("function f2() { return 2; }")
result2 = ctx2.call("f2", [])  # OK

result1 = ctx1.call("f1", [])  # ❌ 崩溃！不能回到 ctx1
```

#### 限制 2: LIFO 删除顺序

**多个 Context 必须按 LIFO 顺序删除（后创建先删除）**

```python
# ❌ 错误：按创建顺序删除会崩溃
ctx1 = never_jscore.Context()
ctx2 = never_jscore.Context()
ctx3 = never_jscore.Context()

del ctx1  # ❌ 崩溃！
del ctx2
del ctx3

# ✅ 正确：LIFO 顺序（后进先出）
ctx1 = never_jscore.Context()
ctx2 = never_jscore.Context()
ctx3 = never_jscore.Context()

# 使用最后创建的 Context
result = ctx3.call("func", [])

# 按逆序删除
del ctx3  # ✅ 最后创建，最先删除
del ctx2  # ✅
del ctx1  # ✅

# ❌ 错误：让 Python 自动清理（顺序不确定）
# 程序结束时会崩溃
```

#### 推荐的使用模式

**模式 1: 单 Context 模式（最推荐）**

将所有函数定义在一个 Context 中：

```python
import never_jscore

ctx = never_jscore.Context()
ctx.compile("""
    function f1() { return 1; }
    function f2() { return 2; }
    function f3() { return 3; }
""")

# 可以任意调用
ctx.call("f1", [])  # OK
ctx.call("f2", [])  # OK
ctx.call("f1", [])  # OK - 可以重复调用
```

**模式 2: 顺序使用（用完即删）**

```python
import never_jscore

# 使用第一个 Context
ctx1 = never_jscore.Context()
ctx1.compile("function f1() { return 1; }")
result = ctx1.call("f1", [])
del ctx1  # 用完立即删除

# 使用第二个 Context
ctx2 = never_jscore.Context()
ctx2.compile("function f2() { return 2; }")
result = ctx2.call("f2", [])
del ctx2  # 用完立即删除
```

**模式 3: LIFO 批量清理（高级用法）**

```python
import never_jscore

# 创建多个 Context（注意：创建第二个后不能再用第一个）
ctx1 = never_jscore.Context()
ctx1.compile("function f1() { return 1; }")
r1 = ctx1.call("f1", [])  # 在创建 ctx2 之前完成所有操作

ctx2 = never_jscore.Context()
ctx2.compile("function f2() { return 2; }")
r2 = ctx2.call("f2", [])  # ctx1 已不可用

ctx3 = never_jscore.Context()
ctx3.compile("function f3() { return 3; }")
r3 = ctx3.call("f3", [])  # ctx1, ctx2 已不可用

# LIFO 顺序删除（后进先出）
del ctx3
del ctx2
del ctx1
```

## v2.2.0 新功能：Node.js 和浏览器 API

### 1. require() - CommonJS 模块系统

完整的 Node.js 模块解析实现，支持相对路径、node_modules、package.json：

```python
import never_jscore

ctx = never_jscore.Context()

# 创建测试模块
with open('my_module.js', 'w') as f:
    f.write('''
        module.exports = {
            add: function(a, b) { return a + b; },
            version: '1.0.0'
        };
    ''')

# 使用 require() 加载模块
result = ctx.evaluate("""
    const myModule = require('./my_module.js');
    myModule.add(10, 20)
""")
print(result)  # 30

# 使用内置模块 fs 和 path
ctx.compile("""
    const fs = require('fs');
    const path = require('path');

    function readConfig() {
        const filePath = path.join('.', 'config.json');
        if (fs.existsSync(filePath)) {
            return fs.readFileSync(filePath);
        }
        return '{}';
    }
""")
```

**支持的功能**：
- ✅ 相对路径：`./module.js`, `../lib/utils.js`
- ✅ 绝对路径：`/path/to/module.js`
- ✅ node_modules 查找（递归向上）
- ✅ package.json 主入口解析
- ✅ 自动扩展名（`.js`, `.json`）
- ✅ 目录入口（`index.js`）
- ✅ 模块缓存（`require.cache`）

**内置模块**：
- `fs` - 文件系统操作
- `path` - 路径处理

### 2. fetch() - HTTP 网络请求

现代 HTTP API，兼容浏览器标准：

```python
import never_jscore

ctx = never_jscore.Context()

# GET 请求
result = ctx.evaluate("""
    (async () => {
        const response = await fetch('https://api.github.com/users/github');
        const data = await response.json();
        return {
            status: response.status,
            username: data.login,
            followers: data.followers
        };
    })()
""")
print(result)

# POST 请求
result = ctx.evaluate("""
    (async () => {
        const response = await fetch('https://httpbin.org/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer token123'
            },
            body: JSON.stringify({
                username: 'test',
                password: 'pass'
            }),
            timeout: 30000
        });

        const data = await response.json();
        return data;
    })()
""")
```

**支持的功能**：
- ✅ GET/POST/PUT/DELETE/PATCH 等所有 HTTP 方法
- ✅ 自定义请求头
- ✅ JSON 自动序列化/反序列化
- ✅ Response 对象（`text()`, `json()`, `blob()`, `arrayBuffer()`）
- ✅ 状态码和状态文本
- ✅ 超时控制

### 3. localStorage / sessionStorage

浏览器存储 API，用于补环境：

```python
import never_jscore

ctx = never_jscore.Context()

# localStorage - 持久化存储
ctx.eval("""
    localStorage.setItem('token', 'abc123');
    localStorage.setItem('user', JSON.stringify({name: 'John', id: 123}));
""")

# 获取值
token = ctx.evaluate("localStorage.getItem('token')")
print(token)  # 'abc123'

# sessionStorage - 会话存储
ctx.eval("""
    sessionStorage.setItem('sessionId', '999');
""")

# 完整示例
result = ctx.evaluate("""
    // 存储用户偏好
    localStorage.setItem('theme', 'dark');
    localStorage.setItem('language', 'zh-CN');

    // 读取偏好
    const preferences = {
        theme: localStorage.getItem('theme'),
        language: localStorage.getItem('language'),
        itemCount: localStorage.length
    };

    JSON.stringify(preferences);
""")
print(result)  # {"theme":"dark","language":"zh-CN","itemCount":2}
```

**API 方法**：
- `setItem(key, value)` - 设置值
- `getItem(key)` - 获取值（不存在返回 null）
- `removeItem(key)` - 删除键
- `clear()` - 清空所有
- `key(index)` - 按索引获取键名
- `length` - 获取键数量

### 4. 浏览器环境对象

模拟完整的浏览器环境（补环境必备）：

```python
import never_jscore

ctx = never_jscore.Context()

# navigator - 浏览器信息
result = ctx.evaluate("""
    JSON.stringify({
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        language: navigator.language,
        onLine: navigator.onLine,
        cookieEnabled: navigator.cookieEnabled,
        hardwareConcurrency: navigator.hardwareConcurrency
    })
""")
print(result)
# {"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36","platform":"Win32",...}

# location - URL 信息
result = ctx.evaluate("""
    JSON.stringify({
        href: location.href,
        protocol: location.protocol,
        hostname: location.hostname,
        pathname: location.pathname
    })
""")

# document - DOM 文档对象
result = ctx.evaluate("""
    JSON.stringify({
        readyState: document.readyState,
        title: document.title,
        URL: document.URL,
        domain: document.domain,
        characterSet: document.characterSet
    })
""")

# window - 窗口对象
result = ctx.evaluate("""
    JSON.stringify({
        innerWidth: window.innerWidth,
        innerHeight: window.innerHeight,
        devicePixelRatio: window.devicePixelRatio
    })
""")

# screen - 屏幕信息
result = ctx.evaluate("""
    JSON.stringify({
        width: screen.width,
        height: screen.height,
        colorDepth: screen.colorDepth
    })
""")
```

**可用对象**：
- `navigator` - 浏览器用户代理信息
- `location` - 页面 URL 信息
- `document` - DOM 文档对象（方法返回 null/空数组）
- `window` - 窗口对象
- `screen` - 屏幕信息

### 5. URL / URLSearchParams

完整的 URL 处理 API：

```python
import never_jscore

ctx = never_jscore.Context()

# URL 解析
result = ctx.evaluate("""
    const url = new URL('https://api.example.com:8080/search?q=test&page=1#results');

    JSON.stringify({
        href: url.href,
        protocol: url.protocol,
        hostname: url.hostname,
        port: url.port,
        pathname: url.pathname,
        search: url.search,
        hash: url.hash,
        origin: url.origin
    })
""")

# URLSearchParams - 查询字符串操作
result = ctx.evaluate("""
    const params = new URLSearchParams('name=John&age=30');

    // 获取参数
    const name = params.get('name');  // "John"

    // 设置参数
    params.set('age', '31');

    // 追加参数
    params.append('tag', 'developer');
    params.append('tag', 'python');

    // 获取所有同名参数
    const tags = params.getAll('tag');  // ["developer", "python"]

    // 转回查询字符串
    const queryString = params.toString();  // "name=John&age=31&tag=developer&tag=python"

    JSON.stringify({name, tags, queryString});
""")

# URL + URLSearchParams 组合
result = ctx.evaluate("""
    const url = new URL('https://api.example.com/search');
    url.searchParams.append('q', 'javascript');
    url.searchParams.append('limit', '10');

    url.href  // "https://api.example.com/search?q=javascript&limit=10"
""")
```

### 6. FormData

表单数据处理 API：

```python
import never_jscore

ctx = never_jscore.Context()

result = ctx.evaluate("""
    const formData = new FormData();

    // 添加字段
    formData.append('username', 'john_doe');
    formData.append('email', 'john@example.com');
    formData.append('tags', 'js');
    formData.append('tags', 'python');

    // 获取单个值
    const username = formData.get('username');  // "john_doe"

    // 获取所有同名值
    const tags = formData.getAll('tags');  // ["js", "python"]

    // 设置（覆盖）
    formData.set('email', 'new@example.com');

    // 检查是否存在
    const hasUser = formData.has('username');  // true

    // 删除
    formData.delete('tags');

    JSON.stringify({username, tags, hasUser});
""")
```

### 7. Event / EventTarget

完整的事件系统：

```python
import never_jscore

ctx = never_jscore.Context()

result = ctx.evaluate("""
    // 创建事件目标
    const target = new EventTarget();

    let eventData = [];

    // 添加事件监听器
    target.addEventListener('custom', (event) => {
        eventData.push({
            type: event.type,
            bubbles: event.bubbles,
            cancelable: event.cancelable
        });
    });

    // 创建并分发事件
    const event = new Event('custom', {
        bubbles: true,
        cancelable: true
    });

    target.dispatchEvent(event);

    // 支持 once 选项
    target.addEventListener('once-event', () => {
        eventData.push('fired once');
    }, { once: true });

    const onceEvent = new Event('once-event');
    target.dispatchEvent(onceEvent);
    target.dispatchEvent(onceEvent);  // 第二次不会触发

    JSON.stringify(eventData);
""")
```

### 8. XMLHttpRequest

传统 AJAX API（基于 fetch 实现）：

```python
import never_jscore

ctx = never_jscore.Context()

result = ctx.evaluate("""
    (async () => {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();

            xhr.onload = function() {
                if (xhr.status === 200) {
                    resolve({
                        status: xhr.status,
                        statusText: xhr.statusText,
                        responseText: xhr.responseText.substring(0, 100),
                        readyState: xhr.readyState
                    });
                } else {
                    reject('Error: ' + xhr.status);
                }
            };

            xhr.onerror = function() {
                reject('Network error');
            };

            // 发送请求
            xhr.open('GET', 'https://httpbin.org/get');
            xhr.setRequestHeader('X-Custom-Header', 'value');
            xhr.send();
        });
    })()
""")

print(result)
```

**支持的功能**：
- ✅ open() / send() / abort()
- ✅ setRequestHeader() / getResponseHeader()
- ✅ onload / onerror / onreadystatechange 事件
- ✅ readyState / status / statusText
- ✅ responseText / response
- ✅ addEventListener / removeEventListener

### 9. Performance API（v2.2.1 新增）

高精度性能测量 API，兼容 Web Performance Timing 标准：

```python
import never_jscore

ctx = never_jscore.Context()

# 1. 高精度时间戳
result = ctx.evaluate("""
    const start = performance.now();

    // 执行一些操作
    let sum = 0;
    for (let i = 0; i < 1000000; i++) {
        sum += i;
    }

    const end = performance.now();

    ({
        start: start,
        end: end,
        elapsed: end - start,
        sum: sum
    })
""")
print(f"耗时: {result['elapsed']:.4f}ms")

# 2. 性能标记和测量
result = ctx.evaluate("""
    // 创建性能标记
    performance.mark('task-start');

    // 步骤 1
    performance.mark('step1-start');
    let data = [];
    for (let i = 0; i < 100000; i++) {
        data.push(i * 2);
    }
    performance.mark('step1-end');

    // 步骤 2
    performance.mark('step2-start');
    let sum = data.reduce((acc, val) => acc + val, 0);
    performance.mark('step2-end');

    // 创建性能测量
    const measure1 = performance.measure('step1-duration', 'step1-start', 'step1-end');
    const measure2 = performance.measure('step2-duration', 'step2-start', 'step2-end');
    const total = performance.measure('total-duration', 'task-start', 'step2-end');

    // 获取所有测量结果
    const measures = performance.getEntriesByType('measure');

    ({
        measures: measures.map(m => ({
            name: m.name,
            duration: m.duration.toFixed(4) + 'ms'
        })),
        sum: sum
    })
""")

for measure in result['measures']:
    print(f"{measure['name']}: {measure['duration']}")
# 输出示例：
# step1-duration: 2.3456ms
# step2-duration: 1.2345ms
# total-duration: 3.5801ms

# 3. 获取性能条目
result = ctx.evaluate("""
    performance.mark('test1');
    performance.mark('test2');
    performance.measure('test-measure', 'test1', 'test2');

    ({
        allEntries: performance.getEntries(),
        marksOnly: performance.getEntriesByType('mark'),
        measuresOnly: performance.getEntriesByType('measure'),
        byName: performance.getEntriesByName('test1')
    })
""")

print(f"所有条目: {len(result['allEntries'])}")
print(f"标记数量: {len(result['marksOnly'])}")
print(f"测量数量: {len(result['measuresOnly'])}")

# 4. 清除标记和测量
ctx.eval("""
    performance.clearMarks('test1');    // 清除单个标记
    performance.clearMarks();           // 清除所有标记
    performance.clearMeasures();        // 清除所有测量
""")
```

**可用 API**：
- `performance.now()` - 高精度时间戳（毫秒）
- `performance.timeOrigin` - 时间原点（Unix 时间戳）
- `performance.mark(name)` - 创建性能标记
- `performance.measure(name, startMark?, endMark?)` - 测量两个标记之间的时间
- `performance.clearMarks(name?)` - 清除标记
- `performance.clearMeasures(name?)` - 清除测量
- `performance.getEntries()` - 获取所有性能条目
- `performance.getEntriesByType(type)` - 按类型获取（'mark' 或 'measure'）
- `performance.getEntriesByName(name, type?)` - 按名称获取

**使用场景**：
- 🎯 代码性能分析和优化
- 🎯 多步骤操作的时间分解
- 🎯 JS 逆向中的性能瓶颈定位
- 🎯 API 调用耗时统计


## 内置 Web API 扩展（v2.0+）

never_jscore 内置了常用的 Web API，**无需额外 polyfill**，开箱即用！

### Crypto APIs（加密相关）

```python
import never_jscore

ctx = never_jscore.Context(enable_extensions=True)

# Base64 编解码
result = ctx.evaluate("btoa('Hello World')")  # "SGVsbG8gV29ybGQ="
result = ctx.evaluate("atob('SGVsbG8gV29ybGQ=')")  # "Hello World"

# 哈希函数
result = ctx.evaluate("md5('test')")  # "098f6bcd4621d373cade4e832627b4f6"
result = ctx.evaluate("sha256('test')")  # "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

# HMAC
result = ctx.evaluate("CryptoUtils.hmacSha256('key', 'message')")

# Hex 编解码
result = ctx.evaluate("CryptoUtils.hexEncode('test')")  # "74657374"
result = ctx.evaluate("CryptoUtils.hexDecode('74657374')")  # "test"

# 链式 API（类 Node.js crypto）
result = ctx.evaluate("""
    CryptoUtils.createHash('sha256')
        .update('hello')
        .update(' world')
        .digest('hex')
""")
```

### URL 编码

```python
# URL 编码（兼容浏览器 API）
result = ctx.evaluate("encodeURIComponent('hello world')")  # "hello%20world"
result = ctx.evaluate("decodeURIComponent('hello%20world')")  # "hello world"
```

### 随机数生成（支持种子控制）

```python
# 默认：非确定性随机数
ctx = never_jscore.Context()

# Math.random() - 标准随机数（0 到 1）
result = ctx.evaluate("Math.random()")  # 每次不同

# UUID 生成
uuid = ctx.evaluate("crypto.randomUUID()")  # "a3111236-1431-4d0d-807e-6c7b388d4433"

# 随机数组
result = ctx.evaluate("""
    const arr = new Uint8Array(16);
    crypto.getRandomValues(arr);
    Array.from(arr)
""")  # [123, 45, 67, ...]

# 使用固定种子（v2.3.0 新增）- 确定性随机数
ctx_seeded = never_jscore.Context(random_seed=12345)

# 所有随机数 API 都遵守种子
r1 = ctx_seeded.evaluate("Math.random()")  # 0.8831156266... (固定)
uuid = ctx_seeded.evaluate("crypto.randomUUID()")  # 固定的 UUID
random_bytes = ctx_seeded.evaluate("""
    const arr = new Uint8Array(8);
    crypto.getRandomValues(arr);
    Array.from(arr)
""")  # 固定的字节数组

# 相同种子产生相同的随机数序列
ctx_same_seed = never_jscore.Context(random_seed=12345)
r2 = ctx_same_seed.evaluate("Math.random()")  # 0.8831156266... (与 r1 相同!)
```

**种子控制的优势：**
- 🎯 调试动态参数算法时可重现执行
- 🎯 对比不同算法实现的行为差异
- 🎯 编写可重现的单元测试
- 🎯 分析依赖随机数的加密算法

### 定时器（立即执行版本）

```python
# setTimeout/setInterval（用于 API 检测，立即执行）
result = ctx.evaluate("""
    let value = 0;
    setTimeout(() => { value = 42; }, 100);  // 立即执行
    value  // 需要等待 Promise
""")
```

⚠️ **注意**：setTimeout/setInterval 是**假的异步**（立即执行），仅用于通过 JS 代码中的 API 存在性检测。

### Worker API（单线程模拟）

```python
# Worker API（用于兼容检测，单线程模拟）
result = ctx.evaluate("""
    typeof Worker === 'function' &&
    typeof Worker.prototype.postMessage === 'function'
""")  # True
```

⚠️ **注意**：Worker 是**单线程模拟**，不会真正创建多线程，仅用于通过代码检测。

### 禁用扩展（纯净 V8）

如果不需要这些 API，可以禁用扩展：

```python
ctx = never_jscore.Context(enable_extensions=False)

# 此时只有 ECMAScript 标准 API
result = ctx.evaluate("typeof btoa")  # "undefined"
result = ctx.evaluate("JSON.stringify({a: 1})")  # '{"a":1}' - 标准 API 可用
```

## 适用场景

### JavaScript 逆向分析（推荐）

```python
import never_jscore

# 加载目标网站的加密 JS
with open("target_crypto.js") as f:
    js_code = f.read()

ctx = never_jscore.Context(enable_extensions=True)  # 启用内置 Web API
ctx.compile(js_code)

# 直接调用加密函数（无需额外 polyfill）
encrypted = ctx.call("encrypt", [plain_text, key])

# 如果 JS 代码使用了 btoa、md5、sha256 等，都可以直接使用
result = ctx.evaluate("btoa(md5('test'))")
```

### 真实场景：API 签名生成

```python
import never_jscore

ctx = never_jscore.Context(enable_extensions=True)

# 典型的签名算法（无需 polyfill，直接运行）
ctx.compile("""
    function generateSignature(params, secret) {
        // 1. 参数排序
        const keys = Object.keys(params).sort();

        // 2. 拼接查询字符串
        const query = keys.map(k =>
            encodeURIComponent(k) + '=' + encodeURIComponent(params[k])
        ).join('&');

        // 3. 添加密钥并计算 HMAC
        const message = query + '&key=' + secret;
        const signature = CryptoUtils.hmacSha256(secret, message);

        // 4. Base64 编码
        return btoa(signature);
    }
""")

# 调用签名函数
signature = ctx.call("generateSignature", [
    {"user": "test", "timestamp": "1234567890"},
    "my-secret-key"
])
print(f"Signature: {signature}")
```

### Hook拦截：提取加密数据（v2.2.2 新增）

```python
import never_jscore

ctx = never_jscore.Context(enable_extensions=True)

# 场景1: Hook Akamai传感器生成
result = ctx.evaluate("""
    (async () => {
        // 模拟Akamai传感器生成函数
        function generateSensorData(userAgent, timestamp) {
            const fingerprint = md5(userAgent + timestamp);
            const hash1 = sha256(fingerprint);
            const signature = hmacSha256('secret_key', hash1);

            // Hook: 拦截传感器数据，不执行后续的网络请求
            __neverjscore_return__({
                sensor: signature,
                fingerprint: fingerprint,
                timestamp: timestamp
            });

            // 后续的网络请求不会执行
            fetch('/verify', {
                method: 'POST',
                body: JSON.stringify({ sig: signature })
            });
        }

        return generateSensorData(navigator.userAgent, Date.now());
    })()
""")

print(f"传感器签名: {result['sensor']}")
print(f"指纹: {result['fingerprint']}")

# 场景2: 拦截多层加密的中间值
ctx.compile("""
    function complexEncrypt(data, key) {
        const step1 = btoa(data);
        const step2 = md5(step1);
        const step3 = hmacSha256(key, step2);

        // Hook第二层加密结果
        if (globalThis.__debug_mode__) {
            $return({
                step: 2,
                md5_result: step2,
                base64_result: step1,
                original: data
            });
        }

        return btoa(step3);
    }
""")

# 开启调试模式，拦截中间值
ctx.eval("globalThis.__debug_mode__ = true;")
result = ctx.call("complexEncrypt", ["sensitive_data", "secret_key"])

print(f"拦截到第{result['step']}步: {result['md5_result']}")

# 场景3: XMLHttpRequest拦截
result = ctx.evaluate("""
    (async () => {
        // Hook所有XMLHttpRequest.send
        const originalSend = XMLHttpRequest.prototype.send;
        let interceptedRequests = [];

        XMLHttpRequest.prototype.send = function(data) {
            interceptedRequests.push({
                url: this._url,
                method: this._method,
                data: data,
                headers: this._headers
            });

            // 拦截第一个POST请求
            if (this._method === 'POST') {
                $return({
                    totalRequests: interceptedRequests.length,
                    lastRequest: interceptedRequests[interceptedRequests.length - 1]
                });
            }

            originalSend.call(this, data);
        };

        // 执行一系列请求
        for (let i = 0; i < 3; i++) {
            const xhr = new XMLHttpRequest();
            xhr.open(i === 2 ? 'POST' : 'GET', '/api/data/' + i);
            xhr.send('data_' + i);
        }
    })()
""")

print(f"拦截到的请求: {result['lastRequest']}")
```

**Hook拦截的优势：**
- ✅ 无需修改原始JS代码
- ✅ 精确控制拦截点
- ✅ 获取加密中间值用于分析
- ✅ 避免执行不必要的网络请求
- ✅ 支持条件拦截和多点拦截

### 异步数据处理

```python
import never_jscore

ctx = never_jscore.Context()
ctx.compile("""
    async function processBatch(items) {
        const results = await Promise.all(
            items.map(async item => {
                // 模拟异步处理
                return await Promise.resolve(item * 2);
            })
        );
        return results;
    }
""")

result = ctx.call("processBatch", [[1, 2, 3, 4, 5]])
print(result)  # [2, 4, 6, 8, 10]
```

## 性能优化建议

1. **重用 Context**: 对于需要多次调用的代码，创建一个 Context 并复用
2. **批量处理**: 在 JavaScript 端批量处理数据，减少 Python-JS 调用次数
3. **单 Context 模式**: 尽可能将所有函数定义在一个 Context 中
4. **合理使用 auto_await**: 对于不需要等待的同步代码，设置 `auto_await=False` 可略微提升性能
5. **避免频繁创建 Context**: 创建 Context 有开销，应尽量复用

## 模块化架构

项目采用清晰的模块化设计：

```
src/
├── lib.rs              # 模块入口，仅导出 Context 类
├── context.rs          # Context 实现（V8 isolate 封装）
├── runtime.rs          # V8/Tokio runtime 管理
├── convert.rs          # Python ↔ JavaScript 类型转换
├── storage.rs          # 结果存储
├── random_state.rs     # 线程本地 RNG 状态管理（v2.3.0 新增）
├── random_ops.rs       # 随机数种子控制（v2.3.0 新增）
├── fs_ops.rs           # 文件系统操作（11 个操作）
├── fetch_ops.rs        # HTTP 请求（基于 reqwest，支持二进制响应）
├── crypto_ops.rs       # 加密操作扩展（Base64、Hash、HMAC、Random）
├── encoding_ops.rs     # URL 编码扩展
├── timer_ops.rs        # 定时器扩展（setTimeout/setInterval）
├── worker_ops.rs       # Worker API 扩展
├── performance_ops.rs  # Performance API（v2.2.1 新增）
├── ops/                # 新增 ops 模块
│   ├── mod.rs         # 模块导出
│   ├── storage_ops.rs # 结果存储 ops（含 early_return，v2.2.2）
│   ├── web_storage.rs # localStorage/sessionStorage（12 个操作）
│   └── browser_env.rs # 浏览器环境对象（9 个操作）
└── dddd_js/
    └── js_polyfill.js  # JavaScript polyfill 层（自动注入，2100+ 行）

tests/
├── test_all_features.py        # 完整功能测试套件
├── test_browser_apis.py        # 浏览器 API 测试
├── test_high_priority_apis.py  # 高优先级 API 测试
├── test_wasm.py               # WebAssembly 测试
├── test_async_simple.py       # 异步功能测试
├── test_extensions.py         # 扩展 API 测试
├── test_new_apis.py           # 新 API 测试
├── test_hook_interception.py  # Hook 拦截测试（v2.2.2）
├── test_random_seed.py        # 随机数种子测试（v2.3.0）
└── test_performance.py        # Performance API 测试（v2.2.1）
```

### 扩展系统架构

- **Rust 层**: 使用 Deno Core 的 `#[op2]` 宏定义底层操作
- **JavaScript 层**: 在 `js_polyfill.js` 中封装为标准 Web API
- **自动注入**: `enable_extensions=True` 时自动加载所有扩展

## 测试

```bash
# 基础功能测试
python test_async_simple.py

# Web API 扩展测试
python test_extensions.py
python test_new_apis.py
```

## 技术细节

- **V8 引擎**: 使用 Deno Core 提供的 V8 bindings
- **Tokio Runtime**: 全局单线程 runtime，支持异步操作
- **类型转换**: Python ↔ JSON ↔ JavaScript 三层转换
- **内存管理**: 使用 `std::mem::forget()` 避免 HandleScope 错误，每 100 次执行提示 GC
- **扩展系统**: 基于 Deno Core extension 机制，模块化设计
- **依赖库**:
  - `deno_core 0.367.0`: V8 运行时
  - `pyo3 0.27.1`: Python 绑定（abi3-py38）
  - `tokio 1.48`: 异步运行时
  - `reqwest 0.12`: HTTP 客户端（支持 JSON 和 blocking）
  - `lazy_static 1.4`: 全局状态管理（localStorage/sessionStorage）
  - `rand 0.8`: 随机数生成
  - `base64`, `md-5`, `sha1`, `sha2`, `hmac`: 加密库
  - `urlencoding`, `percent-encoding`: URL 编解码

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关项目

- [py_mini_racer](https://github.com/sqreen/PyMiniRacer) - Python MiniRacer 实现
- [PyExecJS](https://github.com/doloopwhile/PyExecJS) - 原 Python ExecJS 实现
- [Deno](https://github.com/denoland/deno) - 现代 JavaScript/TypeScript 运行时
- [PyO3](https://github.com/PyO3/pyo3) - Rust Python bindings

## 更新日志

### v2.3.0 (2025-11-12) - 确定性随机数与二进制数据修复

#### 确定性随机数（Seedable RNG）
- ✨ **随机数种子控制**: Context 新增 `random_seed` 参数
  - 支持固定种子创建确定性执行环境
  - 所有随机数 API 统一受种子控制
  - 相同种子产生完全相同的随机数序列
- 🎲 **支持的随机数 API**:
  - `Math.random()`: 标准随机数（0 到 1）
  - `crypto.randomUUID()`: UUID v4 生成
  - `crypto.getRandomValues()`: 随机字节数组
- 📊 **应用场景**:
  - 调试动态参数加密算法
  - 可重现的单元测试
  - 对比不同算法实现的行为
  - Akamai 等反爬虫算法的确定性执行

#### 二进制数据支持修复
- 🔧 **WASM 加载修复**: 修复 fetch() 对二进制数据的处理
  - `fetch_ops.rs`: 改用 `response.bytes()` 代替 `response.text()`
  - 添加 Content-Type 检测，自动识别二进制响应
  - 二进制数据通过 Base64 编码传输（`bodyBinary` 字段）
- 🔧 **Base64 解码修复**: 修复 `atob()` 对二进制数据的处理
  - `crypto_ops.rs`: `op_base64_decode` 返回 Latin-1 字符串
  - 避免 UTF-8 解码错误，正确处理二进制数据
- 🌐 **XMLHttpRequest 增强**:
  - 支持 `responseType="arraybuffer"`
  - 正确提取响应头（`getResponseHeader()`）
  - `Response.arrayBuffer()` 正确解码 Base64 二进制数据

#### 技术实现
- **新增文件**:
  - `src/random_state.rs`: 线程本地 RNG 状态管理（~90 行）
  - `src/random_ops.rs`: 随机数种子控制 ops（~30 行）
  - `tests/test_random_seed.py`: 随机数种子功能测试套件（5 个测试，全部通过）
- **修改文件**:
  - `src/lib.rs`: 添加 random_state 和 random_ops 模块
  - `src/crypto_ops.rs`: 所有随机函数统一使用 `random_state`
  - `src/fetch_ops.rs`: 二进制响应处理，添加 `bodyBinary` 字段
  - `src/context.rs`: Context 添加 `random_seed` 参数
  - `src/dddd_js/js_polyfill.js`: 覆盖 `Math.random()`，增强 `Response.arrayBuffer()`
  - `py_mod/never_jscore/never_jscore.pyi`: 更新类型提示

#### 测试覆盖
- ✅ 5 个随机数种子测试全部通过（100% 通过率）
  - Math.random() 固定种子测试
  - 不同种子产生不同随机数测试
  - 无种子非确定性测试
  - crypto API 种子控制测试
  - 可重现算法对比测试
- ✅ WASM 二进制加载测试通过
  - 124KB WASM 模块成功加载
  - 正确的 WASM magic bytes: `0x00 0x61 0x73 0x6d`

### v2.2.2 (2025-11-12) - Hook拦截与提前返回

#### Hook拦截功能
- ✨ **Hook拦截API**: 支持在任意位置终止JavaScript执行并返回结果
  - `__neverjscore_return__(value)`: 完整函数名
  - `$return(value)`: 简短别名（推荐使用）
  - `$exit(value)`: 替代别名
- 🎣 **提前返回机制**:
  - 立即终止JavaScript执行
  - 跳过后续所有代码（包括异步操作）
  - 将拦截到的值返回到Python
  - 支持同步和异步两种执行模式
  - 自动处理JSON序列化（失败时降级为字符串）

#### 应用场景
- 🎯 Hook `XMLHttpRequest.send` 拦截加密请求数据
- 🎯 Hook加密函数获取中间值
- 🎯 提取Akamai等反爬虫的传感器数据
- 🎯 条件拦截：只在满足条件时提前返回
- 🎯 多点拦截：在多个位置设置拦截点

#### 技术实现
- **Rust层**: 新增 `op_early_return` 操作，添加 `early_return` 标志
- **JavaScript层**: 通过抛出特殊异常实现立即终止
- **异步支持**: 跳过event loop，立即返回结果
- **同步支持**: 正确识别并处理提前返回信号

#### 新增文件
- `examples/hook_examples.py`: 5个实用Hook示例
- `tests/test_hook_interception.py`: 13个全面测试用例（全部通过）
- `HOOK_IMPLEMENTATION_REPORT.md`: 详细实现报告

#### 修改文件
- `src/storage.rs`: 添加 `early_return` 标志和相关方法
- `src/ops/storage_ops.rs`: 添加 `op_early_return` 操作
- `src/context.rs`: 异步和同步模式的提前返回处理
- `src/dddd_js/js_polyfill.js`: 添加提前返回API，重组日志工具

#### 测试覆盖
- ✅ 13个测试用例全部通过（100%通过率）
- ✅ Hook XMLHttpRequest.send测试
- ✅ Hook加密函数测试
- ✅ 条件拦截测试
- ✅ 复杂数据结构返回测试
- ✅ 跳过异步操作测试
- ✅ Akamai风格Hook测试

### v2.2.1 (2025-11-11) - Performance API

#### 性能监控 API
- ✨ **Performance API**: 完整的 Web Performance Timing API
  - `performance.now()`: 高精度时间戳（毫秒级）
  - `performance.timeOrigin`: 时间原点（Unix 时间戳）
  - `performance.mark(name)`: 创建性能标记
  - `performance.measure(name, start, end)`: 测量两个标记之间的时间
  - `performance.getEntries()`: 获取所有性能条目
  - `performance.getEntriesByType(type)`: 按类型获取（'mark' 或 'measure'）
  - `performance.getEntriesByName(name)`: 按名称获取
  - `performance.clearMarks()` / `performance.clearMeasures()`: 清除标记和测量

#### 新增文件
- `src/performance_ops.rs`: Performance API Rust 实现（~220 行）
- `test_performance.py`: Performance API 测试套件

#### 使用场景
- 🎯 JavaScript 代码性能分析
- 🎯 多步骤操作的时间分解
- 🎯 性能瓶颈定位
- 🎯 API 调用耗时统计

### v2.2.0 (2025-11-11) - 重大功能扩展

#### Node.js 环境 API
- ✨ **require()**: 完整的 CommonJS 模块系统
  - 相对/绝对路径模块加载
  - node_modules 递归查找
  - package.json 主入口解析
  - 模块缓存机制
- ✨ **fs 模块**: 文件系统操作（readFileSync, writeFileSync, existsSync 等）
- ✨ **path 模块**: 路径处理（resolve, join, dirname, basename 等）
- ✨ **fetch()**: 现代 HTTP API
  - 支持所有 HTTP 方法（GET/POST/PUT/DELETE 等）
  - 自定义请求头
  - JSON 自动序列化/反序列化
  - Response/Headers 对象
  - 超时控制

#### 浏览器环境 API（补环境）
- ✨ **localStorage/sessionStorage**: 浏览器存储 API
  - setItem/getItem/removeItem/clear
  - key() 和 length 属性
  - 线程安全全局存储
- ✨ **浏览器环境对象**:
  - `navigator`: 用户代理、平台、语言等信息
  - `location`: URL 解析（href, protocol, hostname 等）
  - `document`: DOM 文档对象（readyState, title, URL 等）
  - `window`: 窗口属性（innerWidth, innerHeight 等）
  - `screen`: 屏幕信息（width, height, colorDepth 等）
- ✨ **URL/URLSearchParams**: 完整的 URL 处理
  - URL 解析和构造
  - 查询参数操作（get/set/append/delete）
  - 迭代器支持
- ✨ **FormData**: 表单数据处理
  - append/get/set/delete 方法
  - getAll() 获取所有同名字段
  - 迭代器支持
- ✨ **Event/EventTarget**: 完整的事件系统
  - Event 类（preventDefault, stopPropagation）
  - EventTarget 类（addEventListener, removeEventListener, dispatchEvent）
  - 事件阶段常量和选项（once, capture）
- ✨ **XMLHttpRequest**: 传统 AJAX API
  - 基于 fetch() 实现
  - 完整的状态管理（UNSENT/OPENED/HEADERS_RECEIVED/LOADING/DONE）
  - 事件处理器（onload, onerror, onreadystatechange）
  - 请求头操作

#### 新增依赖
- `reqwest 0.12`: HTTP 客户端库（blocking 模式）
- `lazy_static 1.4`: 全局状态管理

#### 代码增量
- **Rust 代码**: ~800 行新增代码
  - fs_ops.rs (11 个操作)
  - fetch_ops.rs (3 个操作)
  - web_storage.rs (12 个操作)
  - browser_env.rs (9 个操作)
- **JavaScript 代码**: ~890 行新增代码
  - require() 实现（~200 行）
  - fetch/Response/Headers（~60 行）
  - localStorage/sessionStorage（~50 行）
  - URL/URLSearchParams（~160 行）
  - FormData（~80 行）
  - Event/EventTarget（~130 行）
  - XMLHttpRequest（~180 行）
  - 浏览器环境对象（~40 行）

#### 测试覆盖
- ✅ test_all_features.py: 7 个综合测试（100% 通过）
- ✅ test_browser_apis.py: 浏览器 API 完整测试
- ✅ test_high_priority_apis.py: 高优先级 API 测试
- ✅ test_wasm.py: WebAssembly 验证测试

### v2.0.0 (2025-11-05)

#### 架构重构
- 🔄 **架构重构**: 改为 py_mini_racer 风格的实例化 API
- ✅ 修复 HandleScope 错误：使用 `std::mem::forget()` 管理 v8::Global
- ✅ 明确 LIFO 清理顺序要求
- ✅ 完善多 Context 使用限制说明
- ✅ 新增 `compile()` 便捷方法
- ✅ 新增 `evaluate()` 独立求值方法

#### Web API 扩展（全新）
- ✨ **Crypto APIs**:
  - Base64: `btoa()`, `atob()`
  - 哈希: `md5()`, `sha1()`, `sha256()`, `sha512()`
  - HMAC: `hmacMd5()`, `hmacSha1()`, `hmacSha256()`
  - Hex: `hexEncode()`, `hexDecode()`
  - 链式 API: `CryptoUtils.createHash()`, `CryptoUtils.createHmac()`
- ✨ **URL 编码**: `encodeURIComponent()`, `decodeURIComponent()`, `encodeURI()`, `decodeURI()`
- ✨ **定时器**: `setTimeout()`, `setInterval()`, `clearTimeout()`, `clearInterval()` (立即执行版本)
- ✨ **Worker API**: `Worker` 类（单线程模拟版本）
- ✨ **随机数**: `crypto.randomUUID()`, `crypto.getRandomValues()`, 随机数 ops
- 🎯 **扩展控制**: `Context(enable_extensions=True/False)` 可选启用/禁用
- 📦 **自动注入**: 无需手动加载 polyfill，开箱即用

#### 性能优化
- ⚡ 扩展模块采用 Rust 实现，性能接近原生
- ⚡ JavaScript polyfill 层仅在必要时使用

### v0.1.0 (2025-11-01)

- ✅ 基于 Deno Core 的 JavaScript 执行
- ✅ Promise/async/await 完整支持
- ✅ Python ↔ JavaScript 类型自动转换
- ✅ 模块化代码架构
- ✅ 完整的类型提示支持
- ✅ 性能监控和统计
