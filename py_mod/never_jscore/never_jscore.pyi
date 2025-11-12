"""
never_jscore - 基于 Deno Core 的 JavaScript 运行时

完整支持 Promise 和 async/await，适合 JS 逆向分析。
py_mini_racer 风格的实例化 API。
"""

from typing import Any, List, Union, Optional

class Context:
    """
    JavaScript 执行上下文（支持异步）

    每个 Context 包含一个独立的 V8 isolate 和 JavaScript 运行时环境。
    默认自动等待 Promise，可以无缝调用异步 JavaScript 函数。

    ⚠️ 重要限制:
    - 创建第二个 Context 后，不能再使用第一个 Context
    - 多个 Context 必须按 LIFO 顺序删除（后创建先删除）
    - 推荐使用单 Context 模式，将所有函数定义在一个 Context 中

    🆕 扩展功能 (enable_extensions=True 时自动加载):
    - Base64: btoa(), atob()
    - 哈希: md5(), sha1(), sha256(), sha512()
    - HMAC: CryptoUtils.hmacMd5(), hmacSha1(), hmacSha256()
    - URL 编码: encodeURIComponent(), decodeURIComponent(), encodeURI(), decodeURI()
    - Hex: CryptoUtils.hexEncode(), hexDecode()
    - 链式 API: CryptoUtils.createHash(), createHmac()

    Example:
        >>> # 基本用法（默认启用扩展）
        >>> ctx = Context()
        >>> ctx.compile("function add(a, b) { return a + b; }")
        >>> result = ctx.call("add", [1, 2])
        >>> print(result)
        3

        >>> # 使用扩展功能
        >>> ctx = Context()
        >>> result = ctx.evaluate("btoa('hello')")
        >>> print(result)
        aGVsbG8=

        >>> result = ctx.evaluate("md5('hello')")
        >>> print(result)
        5d41402abc4b2a76b9719d911017c592

        >>> # 纯净 V8 环境（不加载扩展）
        >>> ctx = Context(enable_extensions=False)
        >>> # 只有 ECMAScript 标准 API
    """

    def __init__(self, enable_extensions: bool = True, enable_logging: bool = False, random_seed: Optional[int] = None) -> None:
        """
        创建一个新的 JavaScript 执行上下文

        Args:
            enable_extensions: 是否启用扩展（crypto, encoding 等），默认 True
                             - True: 自动加载 btoa/atob/md5/sha256 等函数
                             - False: 纯净 V8 环境，只包含 ECMAScript 标准 API
            enable_logging: 是否启用操作日志输出，默认 False
                           - True: 输出所有扩展操作的日志（用于调试）
                           - False: 不输出日志（推荐生产环境）
            random_seed: 随机数种子（可选），用于确定性随机数生成
                        - None: 使用系统随机数（非确定性）
                        - int: 使用固定种子（确定性）
                          所有随机数 API（Math.random、crypto.getRandomValues 等）
                          将基于此种子生成，方便调试和算法对比

        Example:
            >>> # 使用固定随机数种子
            >>> ctx = Context(random_seed=12345)
            >>> r1 = ctx.evaluate("Math.random()")  # 确定性随机数
            >>> r2 = ctx.evaluate("Math.random()")  # 下一个确定性随机数
            >>>
            >>> # 另一个相同种子的上下文将产生相同的随机数序列
            >>> ctx2 = Context(random_seed=12345)
            >>> r3 = ctx2.evaluate("Math.random()")  # r3 == r1
        """
        ...

    def compile(self, code: str) -> None:
        """
        编译 JavaScript 代码并加入全局作用域

        Args:
            code: JavaScript 代码字符串

        Raises:
            Exception: 当代码编译失败时

        Example:
            >>> ctx = Context()
            >>> ctx.compile('''
            ...     function add(a, b) { return a + b; }
            ...     function multiply(a, b) { return a * b; }
            ... ''')
            >>> ctx.call("add", [1, 2])
            3
        """
        ...

    def eval(
        self,
        code: str,
        return_value: bool = False,
        auto_await: Optional[bool] = None
    ) -> Any:
        """
        执行代码并将其加入全局作用域

        Args:
            code: JavaScript 代码字符串
            return_value: 是否返回最后一个表达式的值（默认 False）
            auto_await: 是否自动等待 Promise（默认 True）

        Returns:
            如果 return_value=True，返回最后表达式的值；否则返回 None

        Raises:
            Exception: 当代码执行失败时

        Example:
            >>> ctx = Context()
            >>> ctx.eval("var x = 10;")  # 添加到全局作用域
            >>> result = ctx.eval("x * 2", return_value=True)
            >>> print(result)
            20
        """
        ...

    def evaluate(self, code: str, auto_await: Optional[bool] = None) -> Any:
        """
        执行代码并返回结果（不影响全局作用域）

        Args:
            code: JavaScript 代码字符串
            auto_await: 是否自动等待 Promise（默认 True）

        Returns:
            表达式的值，自动转换为 Python 对象

        Raises:
            Exception: 当代码执行失败时

        Example:
            >>> ctx = Context()
            >>> result = ctx.evaluate("1 + 2 + 3")
            >>> print(result)
            6

            >>> # Promise（自动等待）
            >>> result = ctx.evaluate("Promise.resolve(42)")
            >>> print(result)
            42
        """
        ...

    def call(
        self,
        name: str,
        args: List[Any] = [],
        auto_await: Optional[bool] = None
    ) -> Any:
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
            >>> ctx = Context()
            >>> ctx.compile("async function decrypt(data) { return data.split('').reverse().join(''); }")
            >>> result = ctx.call("decrypt", ["olleh"])
            >>> print(result)
            hello
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

# 类型别名
JSValue = Union[None, bool, int, float, str, List[Any], dict[str, Any]]
"""JavaScript 值的 Python 类型表示"""

__version__: str = "2.0.0"
"""模块版本号"""

__all__ = [
    "Context",
    "JSValue",
]
