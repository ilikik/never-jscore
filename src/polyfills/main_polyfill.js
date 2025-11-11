// main_polyfill.js
// 主 polyfill 文件 - 整合所有浏览器环境模拟
// 用于 JS 补环境

// 加载所有模块（内联）
// 注意：这是简化版本，实际使用时应该将各个模块内容内联到这里

// ============================================
// 1. Storage APIs
// ============================================

if (typeof localStorage === 'undefined') {
    class Storage {
        setItem(key, value) {
            const result = Deno.core.ops.op_local_storage_set_item(String(key), String(value));
            if (result !== 'OK') throw new Error(result);
        }
        getItem(key) {
            const result = Deno.core.ops.op_local_storage_get_item(String(key));
            return result === 'null' ? null : result;
        }
        removeItem(key) {
            Deno.core.ops.op_local_storage_remove_item(String(key));
        }
        clear() {
            Deno.core.ops.op_local_storage_clear();
        }
        key(index) {
            const keys = JSON.parse(Deno.core.ops.op_local_storage_keys());
            return keys[index] || null;
        }
        get length() {
            return Deno.core.ops.op_local_storage_length();
        }
    }

    class SessionStorage {
        setItem(key, value) {
            const result = Deno.core.ops.op_session_storage_set_item(String(key), String(value));
            if (result !== 'OK') throw new Error(result);
        }
        getItem(key) {
            const result = Deno.core.ops.op_session_storage_get_item(String(key));
            return result === 'null' ? null : result;
        }
        removeItem(key) {
            Deno.core.ops.op_session_storage_remove_item(String(key));
        }
        clear() {
            Deno.core.ops.op_session_storage_clear();
        }
        key(index) {
            const keys = JSON.parse(Deno.core.ops.op_session_storage_keys());
            return keys[index] || null;
        }
        get length() {
            return Deno.core.ops.op_session_storage_length();
        }
    }

    globalThis.localStorage = new Storage();
    globalThis.sessionStorage = new SessionStorage();
}

// ============================================
// 2. Browser Environment (navigator, location, document, window, screen)
// ============================================

if (typeof navigator === 'undefined') {
    const navigatorData = JSON.parse(Deno.core.ops.op_get_navigator());
    globalThis.navigator = navigatorData;
}

if (typeof location === 'undefined') {
    const locationData = JSON.parse(Deno.core.ops.op_get_location('https://example.com/'));
    globalThis.location = locationData;
}

if (typeof document === 'undefined') {
    const docProps = JSON.parse(Deno.core.ops.op_get_document_props());
    globalThis.document = Object.assign({
        getElementById: () => null,
        getElementsByClassName: () => [],
        getElementsByTagName: () => [],
        querySelector: () => null,
        querySelectorAll: () => [],
        createElement: (tag) => ({ tagName: tag.toUpperCase() }),
        addEventListener: () => {},
        removeEventListener: () => {}
    }, docProps);
}

if (typeof window === 'undefined') {
    globalThis.window = globalThis;
}

const windowProps = JSON.parse(Deno.core.ops.op_get_window_props());
Object.assign(globalThis, windowProps);

if (typeof screen === 'undefined') {
    const screenData = JSON.parse(Deno.core.ops.op_get_screen());
    globalThis.screen = screenData;
}

// ============================================
// 3. Enhanced Console
// ============================================

if (typeof console === 'undefined' || !console.log) {
    globalThis.console = {
        log: (...args) => {
            const msg = args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ');
            Deno.core.ops.op_console_log(msg);
        },
        warn: (...args) => Deno.core.ops.op_console_warn(args.join(' ')),
        error: (...args) => Deno.core.ops.op_console_error(args.join(' ')),
        info: (...args) => Deno.core.ops.op_console_info(args.join(' ')),
        debug: function(...args) { this.log(...args); },
        trace: function(...args) { this.log('[Trace]', ...args); },
        assert: function(cond, ...args) { if (!cond) this.error('Assertion failed:', ...args); }
    };
}

// ============================================
// 标记扩展已加载
// ============================================
globalThis.__NEVER_JSCORE_BROWSER_ENV_LOADED__ = true;
