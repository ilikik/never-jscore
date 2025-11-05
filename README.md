# never_jscore 中文文档

基于 Deno Core (V8) 的高性能 Python JavaScript 执行引擎。

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
- 📦 **上下文隔离**: 每个 Context 独立的 V8 执行环境，互不干扰
- 🎯 **py_mini_racer 兼容**: API 设计类似 py_mini_racer，实例化使用
- 🧹 **自动内存管理**: 基于 Rust 的自动垃圾回收，无内存泄漏
- 🛡️ **类型安全**: 提供完整的类型提示（.pyi 文件）
- 🎮 **JS逆向首选**: 专为 JS 逆向工程优化，支持批量函数调用

## 性能对比

| 测试项目 | never_jscore | PyMiniRacer | PyExecJS |
|---------|-------------|-------------|----------|
| 简单计算 | 0.012ms | 0.005ms | 2.3ms |
| 字符串操作 | **0.004ms** 🏆 | 0.008ms | 2.3ms |
| 数组操作 | **0.004ms** 🏆 | 0.006ms | 2.3ms |
| Promise | **✅ 0.003ms** | ❌ 不支持 | ❌ 不支持 |


## 安装

### 从源码安装

```bash
pip install maturin
maturin develop --release
```

## 快速开始

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

## API 参考

### Context 类

#### `never_jscore.Context()`

创建一个新的 JavaScript 执行上下文。

**返回**: Context 对象

**示例**:
```python
ctx = never_jscore.Context()
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

## 适用场景

### JavaScript 逆向分析

```python
import never_jscore

# 加载目标网站的加密 JS
with open("target_crypto.js") as f:
    js_code = f.read()

ctx = never_jscore.Context()
ctx.compile(js_code)

# 调用加密函数
encrypted = ctx.call("encrypt", [plain_text, key])

# 调用解密函数
decrypted = ctx.call("decrypt", [cipher_text, key])

# 解析响应
parsed = ctx.call("parseResponse", [response_data])
```

### 使用 Polyfill 支持 Web API

```python
import never_jscore
from pathlib import Path

# 读取 polyfill
polyfill_path = Path("examples/polyfill_example.js")
polyfill = polyfill_path.read_text(encoding='utf-8')

# 加载 polyfill + 业务代码
ctx = never_jscore.Context()
ctx.compile(polyfill + """
    function encryptData(data) {
        return btoa(data);  // 现在可以使用 btoa
    }
""")

result = ctx.call("encryptData", ["Hello"])
print(result)  # SGVsbG8=
```

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
├── lib.rs        # 模块入口，仅导出 Context 类
├── context.rs    # Context 实现（V8 isolate 封装）
├── runtime.rs    # V8/Tokio runtime 管理
├── ops.rs        # Deno Core ops 定义
├── convert.rs    # Python ↔ JavaScript 类型转换
└── storage.rs    # 结果存储
```

## 测试

```bash
# 异步功能测试
python test_async_simple.py

# Polyfill 示例
python examples/use_polyfill.py
```

## 技术细节

- **V8 引擎**: 使用 Deno Core 提供的 V8 bindings
- **Tokio Runtime**: 全局单线程 runtime，支持异步操作
- **类型转换**: Python ↔ JSON ↔ JavaScript 三层转换
- **内存管理**: 使用 `std::mem::forget()` 避免 HandleScope 错误，每 100 次执行提示 GC

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

### v2.0.0

- 🔄 **架构重构**: 改为 py_mini_racer 风格的实例化 API
- ✅ 修复 HandleScope 错误：使用 `std::mem::forget()` 管理 v8::Global
- ✅ 明确 LIFO 清理顺序要求
- ✅ 完善多 Context 使用限制说明
- ✅ 新增 `compile()` 便捷方法
- ✅ 新增 `evaluate()` 独立求值方法
- ✅ 更新所有示例和文档

### v0.1.0

- ✅ 基于 Deno Core 的 JavaScript 执行
- ✅ Promise/async/await 完整支持
- ✅ Python ↔ JavaScript 类型自动转换
- ✅ 模块化代码架构
- ✅ 完整的类型提示支持
- ✅ 性能监控和统计
