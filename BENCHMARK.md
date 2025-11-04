# 性能测试说明

本目录包含三个性能测试脚本，用于对比 PyExecJS-RS 与其他 Python JavaScript 执行库的性能。

## 测试脚本

### 1. benchmark_quick.py - 快速对比测试 ⚡

**用途**: 快速查看各库在常见操作上的性能差异

**测试项目**:
- 简单计算
- 字符串操作
- 数组操作 (map/reduce)
- 函数编译和调用
- Promise 处理
- 复杂计算 (Fibonacci)

**运行**:
```bash
python benchmark_quick.py
```

**预计耗时**: 约 30-60 秒

---

### 2. benchmark_comparison.py - 全面性能对比 📊

**用途**: 详细的性能基准测试，包含统计数据

**测试项目**:
- 简单计算
- 字符串操作
- 数组操作
- 对象操作
- 函数编译和调用
- Promise 处理
- 复杂计算
- JSON 处理

**特点**:
- 每个测试运行 100 次
- 提供平均值、中位数、标准差
- 自动生成对比表格
- 显示相对速度倍数

**运行**:
```bash
python benchmark_comparison.py
```

**预计耗时**: 约 2-5 分钟

---

### 3. benchmark_reverse.py - JS逆向场景测试 🔐

**用途**: 模拟真实的 JS 逆向工程场景

**测试场景**:
1. **Base64 编码/解码** - 数据传输
2. **哈希签名生成** - 参数验证
3. **URL参数签名** - API 请求
4. **加密函数调用** - 批量加密
5. **JSON数据处理** - API 响应
6. **字符串反混淆** - 代码还原
7. **Token生成** - 会话管理
8. **异步Promise处理** - 现代加密库

**运行**:
```bash
python benchmark_reverse.py
```

**预计耗时**: 约 1-2 分钟

---

## 依赖安装

### 安装 PyExecJS-RS (本项目)
```bash
# 在项目根目录
maturin develop --release
```

### 安装其他对比库
```bash
# PyExecJS (需要 Node.js 环境)
pip install PyExecJS

# PyMiniRacer (基于 V8)
pip install py-mini-racer

# js2py (纯 Python 实现)
pip install js2py

# dukpy (基于 Duktape)
pip install dukpy
```

**注意**:
- PyExecJS 需要系统安装 Node.js 或其他 JS 运行时
- 其他库为可选，未安装的库会自动跳过测试

---

## 预期结果

根据我们的测试，预期性能排名（从快到慢）:

### 简单操作 (eval)
1. **PyMiniRacer** - 最快（V8 直接绑定）
2. **PyExecJS-RS** - 接近 (V8 + 轻量级包装)
3. **dukpy** - 中等 (轻量级引擎)
4. **PyExecJS** - 较慢 (进程调用开销)
5. **js2py** - 最慢 (纯 Python 实现)

### 函数调用 (compile + call)
1. **PyExecJS-RS** - 最快（上下文复用）
2. **PyMiniRacer** - 接近
3. **dukpy** - 中等
4. **PyExecJS** - 较慢
5. **js2py** - 最慢

### Promise/异步操作
- **PyExecJS-RS** - ✅ 原生支持，自动等待
- 其他库 - ❌ 不支持或支持有限

---

## 示例输出

```
==================================================
快速性能对比 (1000次迭代)
==================================================

测试1: 简单计算 (1 + 2 + 3 + 4 + 5)
--------------------------------------------------
PyExecJS-RS                             :   0.0245ms (总计: 24.50ms)
PyExecJS                                :   2.3456ms (总计: 2345.60ms)
  → PyExecJS 是 PyExecJS-RS 的 95.76x
PyMiniRacer                             :   0.0198ms (总计: 19.80ms)
  → PyMiniRacer 是 PyExecJS-RS 的 0.81x
dukpy                                   :   0.1234ms (总计: 123.40ms)
  → dukpy 是 PyExecJS-RS 的 5.04x
js2py                                   :  15.6789ms (总计: 1567.89ms)
  → js2py 是 PyExecJS-RS 的 640.16x
```

---

## 性能优化建议

根据测试结果，使用 PyExecJS-RS 时的最佳实践：

### ✅ 推荐做法
```python
import pyexecjs_rs as execjs

# 1. 编译一次，多次调用
ctx = execjs.compile("""
    function encrypt(data) { return btoa(data); }
""")

for item in data_list:
    result = ctx.call("encrypt", [item])  # 复用上下文
```

### ❌ 避免做法
```python
# 不要每次都重新编译
for item in data_list:
    ctx = execjs.compile("...")  # 性能差
    result = ctx.call("encrypt", [item])
```

### 📌 适用场景
- **App 逆向**: 签名算法破解
- **网站爬虫**: 加密参数生成
- **自动化测试**: Cookie/Token 生成
- **数据处理**: 混淆代码执行

---

## 特性对比表

| 特性 | PyExecJS-RS | PyExecJS | PyMiniRacer | js2py | dukpy |
|------|-------------|----------|-------------|-------|-------|
| 引擎 | V8 (Deno) | Node/V8等 | V8 | 纯Python | Duktape |
| Promise | ✅ 完整 | ❌ | ⚠️ 有限 | ❌ | ❌ |
| async/await | ✅ | ❌ | ⚠️ | ❌ | ❌ |
| 性能 | ⚡⚡⚡⚡ | ⚡⚡ | ⚡⚡⚡⚡⚡ | ⚡ | ⚡⚡⚡ |
| 安装难度 | 简单 | 需Node.js | 简单 | 简单 | 简单 |
| 上下文复用 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 类型转换 | 自动 | 自动 | 自动 | 自动 | 自动 |
| ES6+ | ✅ 完整 | ✅ | ✅ | ⚠️ 部分 | ⚠️ 部分 |

---

## 常见问题

### Q: 为什么 PyMiniRacer 在某些测试中更快？
A: PyMiniRacer 是 V8 的直接绑定，开销最小。PyExecJS-RS 使用 Deno Core，有轻量级包装层，但提供了更多功能（如 Promise 支持）。

### Q: 什么时候选择 PyExecJS-RS？
A: 当你需要:
- Promise/async 支持（现代 JS 库）
- 高性能 + Rust 稳定性
- 批量函数调用
- JS 逆向工程

### Q: PyExecJS 为什么这么慢？
A: PyExecJS 通过进程调用外部 JS 运行时，每次都有进程通信开销。

### Q: 如何选择测试脚本？
- **快速查看**: `benchmark_quick.py`
- **详细数据**: `benchmark_comparison.py`
- **实际场景**: `benchmark_reverse.py`

---

## 贡献测试用例

欢迎提交更多测试场景！请确保：
1. 测试用例贴近实际使用场景
2. 代码能在所有库中运行（或注明不支持）
3. 包含预期结果说明

---

## 相关链接

- [PyExecJS-RS 文档](../中文文档.md)
- [PyExecJS](https://github.com/doloopwhile/PyExecJS)
- [PyMiniRacer](https://github.com/sqreen/PyMiniRacer)
- [js2py](https://github.com/PiotrDabkowski/Js2Py)
- [dukpy](https://github.com/amol-/dukpy)
