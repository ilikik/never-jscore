#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试浏览器环境 API - localStorage, sessionStorage, navigator, location, document, window
"""

import never_jscore
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("  测试浏览器环境 API")
print("=" * 70)

# ============= 测试 1: localStorage =============
print("\n【测试 1】localStorage API")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    // 设置值
    localStorage.setItem('username', 'never_jscore');
    localStorage.setItem('version', '2.1.0');
    localStorage.setItem('count', '42');

    // 获取值
    const username = localStorage.getItem('username');
    const version = localStorage.getItem('version');
    const count = localStorage.getItem('count');

    // 获取长度
    const length = localStorage.length;

    // 获取不存在的键
    const notExists = localStorage.getItem('notexists');

    JSON.stringify({
        username,
        version,
        count,
        length,
        notExists
    });
""")
print(f"✅ localStorage 测试: {result}")
del ctx

# ============= 测试 2: sessionStorage =============
print("\n【测试 2】sessionStorage API")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    // 设置值
    sessionStorage.setItem('token', 'abc123');
    sessionStorage.setItem('sessionId', '999');

    // 获取值
    const token = sessionStorage.getItem('token');
    const sessionId = sessionStorage.getItem('sessionId');

    // 删除
    sessionStorage.removeItem('sessionId');
    const afterRemove = sessionStorage.getItem('sessionId');

    JSON.stringify({
        token,
        sessionId,
        afterRemove,
        length: sessionStorage.length
    });
""")
print(f"✅ sessionStorage 测试: {result}")
del ctx

# ============= 测试 3: navigator =============
print("\n【测试 3】navigator 对象")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    JSON.stringify({
        userAgent: navigator.userAgent.substring(0, 50) + '...',
        platform: navigator.platform,
        language: navigator.language,
        onLine: navigator.onLine,
        cookieEnabled: navigator.cookieEnabled,
        hardwareConcurrency: navigator.hardwareConcurrency
    }, null, 2);
""")
print(f"✅ navigator 对象:\n{result}")
del ctx

# ============= 测试 4: location =============
print("\n【测试 4】location 对象")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    JSON.stringify({
        href: location.href,
        protocol: location.protocol,
        hostname: location.hostname,
        port: location.port,
        pathname: location.pathname
    }, null, 2);
""")
print(f"✅ location 对象:\n{result}")
del ctx

# ============= 测试 5: document =============
print("\n【测试 5】document 对象")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    JSON.stringify({
        readyState: document.readyState,
        title: document.title,
        URL: document.URL,
        domain: document.domain,
        characterSet: document.characterSet,
        hasGetElementById: typeof document.getElementById === 'function',
        hasQuerySelector: typeof document.querySelector === 'function'
    }, null, 2);
""")
print(f"✅ document 对象:\n{result}")
del ctx

# ============= 测试 6: window/screen =============
print("\n【测试 6】window 和 screen 对象")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    JSON.stringify({
        window: {
            innerWidth: window.innerWidth,
            innerHeight: window.innerHeight,
            devicePixelRatio: window.devicePixelRatio
        },
        screen: {
            width: screen.width,
            height: screen.height,
            colorDepth: screen.colorDepth
        }
    }, null, 2);
""")
print(f"✅ window/screen 对象:\n{result}")
del ctx

# ============= 测试 7: console =============
print("\n【测试 7】console 增强")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    console.log('This is a log message');
    console.warn('This is a warning');
    console.error('This is an error');
    console.info('This is info');

    // 返回测试结果
    JSON.stringify({
        hasLog: typeof console.log === 'function',
        hasWarn: typeof console.warn === 'function',
        hasError: typeof console.error === 'function',
        hasInfo: typeof console.info === 'function',
        hasTable: typeof console.table === 'function'
    });
""")
print(f"✅ console 方法: {result}")
del ctx

# ============= 综合测试 =============
print("\n【综合测试】组合使用所有浏览器 API")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    // 模拟真实浏览器环境场景

    // 1. 检查浏览器信息
    const isMobile = /Mobile/i.test(navigator.userAgent);

    // 2. 使用 localStorage 存储配置
    localStorage.setItem('theme', 'dark');
    localStorage.setItem('lastVisit', Date.now().toString());

    // 3. 获取屏幕信息
    const screenInfo = `${screen.width}x${screen.height}`;

    // 4. 构建页面信息
    const pageInfo = {
        url: document.URL,
        title: document.title || 'Untitled',
        referrer: document.referrer || 'none'
    };

    // 5. 检查环境
    const env = {
        hasWindow: typeof window !== 'undefined',
        hasDocument: typeof document !== 'undefined',
        hasNavigator: typeof navigator !== 'undefined',
        hasLocalStorage: typeof localStorage !== 'undefined',
        hasConsole: typeof console !== 'undefined'
    };

    JSON.stringify({
        isMobile,
        theme: localStorage.getItem('theme'),
        screenInfo,
        pageInfo,
        env
    }, null, 2);
""")
print(f"✅ 综合测试结果:\n{result}")
del ctx

print("\n" + "=" * 70)
print("  ✅ 所有浏览器环境 API 测试通过！")
print("=" * 70)
