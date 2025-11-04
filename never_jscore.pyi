"""
PyExecJS-RS - 基于 Deno Core 的 JavaScript 运行时

完整支持 Promise 和 async/await，适合 JS 逆向分析。
"""

from typing import Any, List, Union

class Context:
    """
    JavaScript 执行上下文（支持异步）

    每个 Context 包含一个独立的 V8 isolate 和 JavaScript 运行时环境。
    默认自动等待 Promise，可以无缝调用异步 JavaScript 函数。

    注意：由于 V8 限制，多个 Context 不能交叉使用。
    建议在一个 Context 中定义所有需要的函数。

    Example:
        >>> # 同步函数
        >>> ctx = compile("function add(a, b) { return a + b; }")
        >>> result = ctx.call("add", [1, 2])
        >>> print(result)
        3

        >>> # 异步函数（自动等待）
        >>> ctx = compile("async function asyncAdd(a, b) { return a + b; }")
        >>> result = ctx.call("asyncAdd", [5, 3])
        >>> print(result)
        8
    """

    def call(self, name: str, args: List[Any], auto_await: bool = True) -> Any:
        """
        调用 JavaScript 函数（支持 Promise）

        Args:
            name: 函数名称
            args: 参数列表
            auto_await: 是否自动等待 Promise（默认 True）

        Returns:
            函数返回值，自动转换为 Python 对象

        Raises:
            Exception: 当函数调用失败时

        Example:
            >>> ctx = compile("async function decrypt(data) { return data.split('').reverse().join(''); }")
            >>> result = ctx.call("decrypt", ["olleh"])
            >>> print(result)
            hello
        """
        ...

    def eval(self, code: str, auto_await: bool = True) -> Any:
        """
        在当前上下文中执行 JavaScript 代码（支持 Promise）

        Args:
            code: JavaScript 代码字符串
            auto_await: 是否自动等待 Promise（默认 True）

        Returns:
            执行结果，自动转换为 Python 对象

        Raises:
            Exception: 当代码执行失败时

        Example:
            >>> # 同步执行
            >>> ctx = compile("var x = 10;")
            >>> result = ctx.eval("x * 2")
            >>> print(result)
            20

            >>> # Promise（自动等待）
            >>> result = ctx.eval("Promise.resolve(42)")
            >>> print(result)
            42
        """
        ...

    def gc(self) -> None:
        """
        请求 V8 垃圾回收

        注意：这只是向 V8 发送 GC 请求，V8 会根据自己的策略决定是否执行。
        在大多数情况下，V8 的自动 GC 已经足够好，无需手动调用。
        """
        ...

    def get_stats(self) -> tuple[int]:
        """
        获取执行统计信息

        Returns:
            包含执行次数的元组 (exec_count,)
        """
        ...

    def reset_stats(self) -> None:
        """
        重置统计信息
        """
        ...

def compile(code: str) -> Context:
    """
    编译 JavaScript 代码并返回执行上下文

    Args:
        code: JavaScript 代码字符串

    Returns:
        Context 对象，可用于调用函数和执行代码

    Raises:
        Exception: 当代码编译失败时

    Example:
        >>> ctx = compile('''
        ...     function greet(name) {
        ...         return "Hello, " + name + "!";
        ...     }
        ... ''')
        >>> result = ctx.call("greet", ["World"])
        >>> print(result)
        Hello, World!
    """
    ...

def eval(code: str, auto_await: bool = True) -> Any:
    """
    直接执行 JavaScript 代码并返回结果（支持 Promise）

    默认自动等待 Promise。适合执行简单的一次性代码。
    对于需要多次调用的场景，建议使用 compile() + Context.call()。

    Args:
        code: JavaScript 代码字符串
        auto_await: 是否自动等待 Promise（默认 True）

    Returns:
        执行结果，自动转换为 Python 对象

    Raises:
        Exception: 当代码执行失败时

    Example:
        >>> # 同步代码
        >>> result = eval("1 + 2 + 3")
        >>> print(result)
        6

        >>> # Promise（自动等待）
        >>> result = eval("Promise.resolve(42)")
        >>> print(result)
        42

        >>> # async 函数
        >>> result = eval("(async () => { return await Promise.resolve(100); })()")
        >>> print(result)
        100
    """
    ...

def compile_file(path: str) -> Context:
    """
    从文件读取并编译 JavaScript 代码

    Args:
        path: JavaScript 文件路径

    Returns:
        Context 对象

    Raises:
        Exception: 当文件读取或编译失败时

    Example:
        >>> # 假设 script.js 包含: function add(a, b) { return a + b; }
        >>> ctx = compile_file("script.js")
        >>> result = ctx.call("add", [5, 3])
        >>> print(result)
        8
    """
    ...

def eval_file(path: str, auto_await: bool = True) -> Any:
    """
    从文件读取并执行 JavaScript 代码（支持 Promise）

    Args:
        path: JavaScript 文件路径
        auto_await: 是否自动等待 Promise（默认 True）

    Returns:
        执行结果

    Raises:
        Exception: 当文件读取或执行失败时

    Example:
        >>> result = eval_file("script.js")
        >>> print(result)
    """
    ...

# 类型别名
JSValue = Union[None, bool, int, float, str, List[Any], dict[str, Any]]
"""JavaScript 值的 Python 类型表示"""

__version__: str
"""模块版本号"""

__all__ = [
    "Context",
    "compile",
    "eval",
    "compile_file",
    "eval_file",
]
