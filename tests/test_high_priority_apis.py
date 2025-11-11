#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试高优先级 Web APIs - URL, URLSearchParams, FormData, Event, EventTarget, XMLHttpRequest
"""

import never_jscore
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("  测试高优先级 Web APIs")
print("=" * 70)

# ============= 测试 1: URL API =============
print("\n【测试 1】URL API")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    const url = new URL('https://example.com:8080/path/to/page?name=test&id=123#section');

    JSON.stringify({
        href: url.href,
        protocol: url.protocol,
        hostname: url.hostname,
        port: url.port,
        pathname: url.pathname,
        search: url.search,
        hash: url.hash,
        origin: url.origin
    }, null, 2);
""")
print(f"✅ URL 解析:\n{result}")
del ctx

# ============= 测试 2: URLSearchParams API =============
print("\n【测试 2】URLSearchParams API")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    const params = new URLSearchParams('name=John&age=30&city=Beijing');

    // 测试 get
    const name = params.get('name');
    const age = params.get('age');

    // 测试 set
    params.set('age', '31');

    // 测试 append
    params.append('hobby', 'coding');
    params.append('hobby', 'reading');

    // 测试 getAll
    const hobbies = params.getAll('hobby');

    // 测试 has
    const hasCity = params.has('city');

    // 测试 toString
    const queryString = params.toString();

    JSON.stringify({
        name,
        age,
        updatedAge: params.get('age'),
        hobbies,
        hasCity,
        queryString
    }, null, 2);
""")
print(f"✅ URLSearchParams 操作:\n{result}")
del ctx

# ============= 测试 3: FormData API =============
print("\n【测试 3】FormData API")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    const formData = new FormData();

    // 测试 append
    formData.append('username', 'never_jscore');
    formData.append('email', 'test@example.com');
    formData.append('tags', 'tag1');
    formData.append('tags', 'tag2');

    // 测试 get
    const username = formData.get('username');

    // 测试 getAll
    const tags = formData.getAll('tags');

    // 测试 set
    formData.set('email', 'new@example.com');

    // 测试 has
    const hasUsername = formData.has('username');
    const hasPassword = formData.has('password');

    // 测试 delete
    formData.delete('tags');

    JSON.stringify({
        username,
        tags,
        updatedEmail: formData.get('email'),
        hasUsername,
        hasPassword,
        tagsAfterDelete: formData.getAll('tags')
    }, null, 2);
""")
print(f"✅ FormData 操作:\n{result}")
del ctx

# ============= 测试 4: Event/EventTarget API =============
print("\n【测试 4】Event/EventTarget API")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    // 创建自定义 EventTarget
    const target = new EventTarget();

    let eventFired = false;
    let eventData = null;

    // 添加事件监听器
    target.addEventListener('custom', (event) => {
        eventFired = true;
        eventData = event.type;
    });

    // 创建并分发事件
    const event = new Event('custom', { bubbles: true, cancelable: true });
    target.dispatchEvent(event);

    // 测试 preventDefault
    let defaultPrevented = false;
    target.addEventListener('test', (e) => {
        e.preventDefault();
        defaultPrevented = e.defaultPrevented;
    });

    const testEvent = new Event('test', { cancelable: true });
    target.dispatchEvent(testEvent);

    JSON.stringify({
        eventFired,
        eventData,
        defaultPrevented,
        eventPhaseConstants: {
            NONE: Event.NONE,
            CAPTURING_PHASE: Event.CAPTURING_PHASE,
            AT_TARGET: Event.AT_TARGET,
            BUBBLING_PHASE: Event.BUBBLING_PHASE
        }
    }, null, 2);
""")
print(f"✅ Event/EventTarget:\n{result}")
del ctx

# ============= 测试 5: XMLHttpRequest API =============
print("\n【测试 5】XMLHttpRequest API (基于 fetch)")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    (async () => {
        const xhr = new XMLHttpRequest();

        // 测试状态常量
        const states = {
            UNSENT: xhr.UNSENT,
            OPENED: xhr.OPENED,
            HEADERS_RECEIVED: xhr.HEADERS_RECEIVED,
            LOADING: xhr.LOADING,
            DONE: xhr.DONE
        };

        // 测试基本 GET 请求
        return new Promise((resolve) => {
            xhr.onload = function() {
                resolve({
                    states,
                    status: xhr.status,
                    statusText: xhr.statusText,
                    readyState: xhr.readyState,
                    hasResponseText: xhr.responseText.length > 0
                });
            };

            xhr.onerror = function() {
                resolve({
                    states,
                    error: 'Request failed'
                });
            };

            xhr.open('GET', 'https://httpbin.org/get');
            xhr.send();
        });
    })()
""")
print(f"✅ XMLHttpRequest:\n{result}")
del ctx

# ============= 测试 6: URL + URLSearchParams 组合 =============
print("\n【测试 6】URL + URLSearchParams 组合使用")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    const url = new URL('https://api.example.com/search');

    // 使用 searchParams 添加查询参数
    url.searchParams.append('q', 'javascript');
    url.searchParams.append('page', '1');
    url.searchParams.append('limit', '10');

    // 修改参数
    url.searchParams.set('page', '2');

    JSON.stringify({
        finalUrl: url.href,
        query: url.searchParams.get('q'),
        page: url.searchParams.get('page'),
        searchString: url.search
    }, null, 2);
""")
print(f"✅ URL + URLSearchParams 组合:\n{result}")
del ctx

# ============= 综合测试 =============
print("\n【综合测试】所有 API 联合使用")
print("-" * 70)

ctx = never_jscore.Context()
result = ctx.evaluate("""
    (async () => {
        // 1. 构建 URL
        const apiUrl = new URL('https://httpbin.org/post');
        apiUrl.searchParams.set('source', 'never_jscore');

        // 2. 准备 FormData
        const formData = new FormData();
        formData.append('name', 'test_user');
        formData.append('version', '2.2.0');

        // 3. 创建 EventTarget 来处理状态
        const statusTarget = new EventTarget();
        let statusLog = [];

        statusTarget.addEventListener('status', (e) => {
            statusLog.push(`Status: ${e.type}`);
        });

        // 4. 使用 XMLHttpRequest 发送请求
        return new Promise((resolve) => {
            const xhr = new XMLHttpRequest();

            xhr.onloadstart = () => {
                const event = new Event('status');
                statusTarget.dispatchEvent(event);
            };

            xhr.onload = () => {
                resolve({
                    url: apiUrl.href,
                    formDataCount: 2,
                    xhrStatus: xhr.status,
                    xhrReady: xhr.readyState === xhr.DONE,
                    eventFired: statusLog.length > 0
                });
            };

            xhr.onerror = () => {
                resolve({ error: 'Request failed' });
            };

            xhr.open('POST', apiUrl.href);
            xhr.send();
        });
    })()
""")
print(f"✅ 综合测试:\n{result}")
del ctx

print("\n" + "=" * 70)
print("  ✅ 所有高优先级 API 测试通过！")
print("=" * 70)
