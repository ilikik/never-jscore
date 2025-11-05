// Web APIs Polyfill for JS Reverse Engineering
// 这个文件包含常用的Web API polyfill，专门为JS逆向工程设计

// ============================================
// Base64 编码/解码 (atob, btoa) - 支持 UTF-8
// ============================================
if (typeof atob === 'undefined') {
    globalThis.atob = function(input) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
        let str = String(input).replace(/[=]+$/, '');
        let output = '';

        if (str.length % 4 === 1) {
            throw new Error("'atob' failed: The string to be decoded is not correctly encoded.");
        }

        for (let bc = 0, bs = 0, buffer, i = 0; buffer = str.charAt(i++);
             ~buffer && (bs = bc % 4 ? bs * 64 + buffer : buffer,
             bc++ % 4) ? output += String.fromCharCode(255 & bs >> (-2 * bc & 6)) : 0
        ) {
            buffer = chars.indexOf(buffer);
        }

        // 支持 UTF-8：将解码的字节转回 UTF-8 字符串
        try {
            return decodeURIComponent(escape(output));
        } catch (e) {
            return output;  // 如果不是 UTF-8，返回原始字符串
        }
    };
}

if (typeof btoa === 'undefined') {
    globalThis.btoa = function(input) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';

        // 支持 UTF-8：先将字符串转换为 UTF-8 字节
        let str = unescape(encodeURIComponent(String(input)));
        let output = '';

        for (let block = 0, charCode, i = 0, map = chars;
             str.charAt(i | 0) || (map = '=', i % 1);
             output += map.charAt(63 & block >> 8 - i % 1 * 8)) {
            charCode = str.charCodeAt(i += 3/4);
            if (charCode > 0xFF) {
                throw new Error("'btoa' failed: The string to be encoded contains characters outside of the Latin1 range.");
            }
            block = block << 8 | charCode;
        }
        return output;
    };

    // 同时提供原始的 btoa（仅 Latin1）
    globalThis.btoaLatin1 = function(input) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
        let str = String(input);
        let output = '';

        for (let block = 0, charCode, i = 0, map = chars;
             str.charAt(i | 0) || (map = '=', i % 1);
             output += map.charAt(63 & block >> 8 - i % 1 * 8)) {
            charCode = str.charCodeAt(i += 3/4);
            if (charCode > 0xFF) {
                throw new Error("'btoaLatin1' failed: The string to be encoded contains characters outside of the Latin1 range.");
            }
            block = block << 8 | charCode;
        }
        return output;
    };
}

// ============================================
// Timer APIs (setTimeout, setInterval, clearTimeout, clearInterval)
// ============================================
if (typeof setTimeout === 'undefined') {
    let timerId = 0;
    const timers = new Map();

    globalThis.setTimeout = function(callback, delay, ...args) {
        const id = ++timerId;
        // 在纯JS环境中，我们只能同步执行
        // 注意：这不是真正的异步，仅用于满足API调用
        timers.set(id, { callback, args, delay });
        return id;
    };

    globalThis.clearTimeout = function(id) {
        timers.delete(id);
    };

    globalThis.setInterval = function(callback, delay, ...args) {
        const id = ++timerId;
        timers.set(id, { callback, args, delay, interval: true });
        return id;
    };

    globalThis.clearInterval = function(id) {
        timers.delete(id);
    };

    // 注意：这个实现不会真正异步执行，只是满足API存在性检查
    // 如果逆向的代码真的依赖setTimeout的异步行为，需要使用方案2或3
}

// ============================================
// Console API (基础版本)
// ============================================
if (typeof console === 'undefined') {
    globalThis.console = {
        log: function(...args) {
            // V8有print函数，但在deno_core中需要通过ops暴露
            // 这里提供一个空实现，避免报错
        },
        warn: function(...args) {},
        error: function(...args) {},
        info: function(...args) {},
        debug: function(...args) {},
        dir: function(...args) {},
        table: function(...args) {},
        trace: function(...args) {},
        assert: function(condition, ...args) {
            if (!condition) {
                throw new Error('Assertion failed: ' + args.join(' '));
            }
        },
        clear: function() {},
        count: function(label) {},
        countReset: function(label) {},
        group: function(...args) {},
        groupCollapsed: function(...args) {},
        groupEnd: function() {},
        time: function(label) {},
        timeEnd: function(label) {},
        timeLog: function(label, ...args) {}
    };
}

// ============================================
// URL 和 URLSearchParams (简化版)
// ============================================
if (typeof URL === 'undefined') {
    globalThis.URL = class URL {
        constructor(url, base) {
            // 简化实现，仅用于满足基本需求
            this.href = url;
            const match = url.match(/^(https?:)\/\/([^\/]+)(\/[^?#]*)(\?[^#]*)?(#.*)?$/);
            if (match) {
                this.protocol = match[1] || '';
                this.host = match[2] || '';
                this.pathname = match[3] || '/';
                this.search = match[4] || '';
                this.hash = match[5] || '';
            }
        }

        toString() {
            return this.href;
        }
    };
}

if (typeof URLSearchParams === 'undefined') {
    globalThis.URLSearchParams = class URLSearchParams {
        constructor(init) {
            this.params = new Map();
            if (typeof init === 'string') {
                init = init.replace(/^\?/, '');
                init.split('&').forEach(pair => {
                    const [key, value] = pair.split('=');
                    if (key) this.params.set(decodeURIComponent(key), decodeURIComponent(value || ''));
                });
            }
        }

        get(name) {
            return this.params.get(name);
        }

        set(name, value) {
            this.params.set(name, value);
        }

        has(name) {
            return this.params.has(name);
        }

        toString() {
            const parts = [];
            for (const [key, value] of this.params) {
                parts.push(encodeURIComponent(key) + '=' + encodeURIComponent(value));
            }
            return parts.join('&');
        }
    };
}

// ============================================
// TextEncoder / TextDecoder
// ============================================
if (typeof TextEncoder === 'undefined') {
    globalThis.TextEncoder = class TextEncoder {
        encode(str) {
            const utf8 = [];
            for (let i = 0; i < str.length; i++) {
                let charcode = str.charCodeAt(i);
                if (charcode < 0x80) utf8.push(charcode);
                else if (charcode < 0x800) {
                    utf8.push(0xc0 | (charcode >> 6), 0x80 | (charcode & 0x3f));
                } else if (charcode < 0xd800 || charcode >= 0xe000) {
                    utf8.push(0xe0 | (charcode >> 12), 0x80 | ((charcode >> 6) & 0x3f), 0x80 | (charcode & 0x3f));
                } else {
                    i++;
                    charcode = 0x10000 + (((charcode & 0x3ff) << 10) | (str.charCodeAt(i) & 0x3ff));
                    utf8.push(0xf0 | (charcode >> 18), 0x80 | ((charcode >> 12) & 0x3f), 0x80 | ((charcode >> 6) & 0x3f), 0x80 | (charcode & 0x3f));
                }
            }
            return new Uint8Array(utf8);
        }
    };
}

if (typeof TextDecoder === 'undefined') {
    globalThis.TextDecoder = class TextDecoder {
        decode(bytes) {
            let str = '';
            let i = 0;
            while (i < bytes.length) {
                let byte1 = bytes[i++];
                if (byte1 < 0x80) {
                    str += String.fromCharCode(byte1);
                } else if (byte1 < 0xe0) {
                    let byte2 = bytes[i++];
                    str += String.fromCharCode(((byte1 & 0x1f) << 6) | (byte2 & 0x3f));
                } else if (byte1 < 0xf0) {
                    let byte2 = bytes[i++];
                    let byte3 = bytes[i++];
                    str += String.fromCharCode(((byte1 & 0x0f) << 12) | ((byte2 & 0x3f) << 6) | (byte3 & 0x3f));
                } else {
                    let byte2 = bytes[i++];
                    let byte3 = bytes[i++];
                    let byte4 = bytes[i++];
                    let codepoint = ((byte1 & 0x07) << 18) | ((byte2 & 0x3f) << 12) | ((byte3 & 0x3f) << 6) | (byte4 & 0x3f);
                    codepoint -= 0x10000;
                    str += String.fromCharCode((codepoint >> 10) + 0xd800, (codepoint & 0x3ff) + 0xdc00);
                }
            }
            return str;
        }
    };
}

// ============================================
// Crypto API (基础版本，适合某些简单的逆向场景)
// ============================================
if (typeof crypto === 'undefined') {
    globalThis.crypto = {
        getRandomValues: function(array) {
            // 简单的伪随机实现
            // 注意：这不是加密安全的！
            for (let i = 0; i < array.length; i++) {
                array[i] = Math.floor(Math.random() * 256);
            }
            return array;
        }
    };
}

// ============================================
// Performance API (简化版)
// ============================================
if (typeof performance === 'undefined') {
    const startTime = Date.now();
    globalThis.performance = {
        now: function() {
            return Date.now() - startTime;
        },
        timing: {},
        navigation: {}
    };
}

// ============================================
// 其他常用的全局对象
// ============================================
if (typeof window === 'undefined') {
    globalThis.window = globalThis;
}

if (typeof global === 'undefined') {
    globalThis.global = globalThis;
}

if (typeof self === 'undefined') {
    globalThis.self = globalThis;
}

// 导出一个标记，表示polyfill已加载
globalThis.__POLYFILL_LOADED__ = true;
