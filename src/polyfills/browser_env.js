// ============================================
// Browser Environment Polyfill
// window, navigator, location, document, screen, console
// ============================================

/**
 * Navigator 对象
 */
if (typeof navigator === 'undefined') {
    const navigatorData = JSON.parse(Deno.core.ops.op_get_navigator());

    class Navigator {
        constructor(data) {
            Object.assign(this, data);
        }
    }

    globalThis.navigator = new Navigator(navigatorData);
}

/**
 * Location 对象
 */
if (typeof location === 'undefined') {
    const locationData = JSON.parse(Deno.core.ops.op_get_location('https://example.com/'));

    class Location {
        constructor(data) {
            Object.assign(this, data);
        }

        assign(url) {
            // Simulated
        }

        reload() {
            // Simulated
        }

        replace(url) {
            // Simulated
        }
    }

    globalThis.location = new Location(locationData);
}

/**
 * Document 对象（简化版）
 */
if (typeof document === 'undefined') {
    const docProps = JSON.parse(Deno.core.ops.op_get_document_props());

    class Document {
        constructor(props) {
            Object.assign(this, props);
            this.cookie = '';
        }

        getElementById(id) {
            return null;
        }

        getElementsByClassName(className) {
            return [];
        }

        getElementsByTagName(tagName) {
            return [];
        }

        querySelector(selector) {
            return null;
        }

        querySelectorAll(selector) {
            return [];
        }

        createElement(tagName) {
            return {
                tagName: tagName.toUpperCase(),
                nodeName: tagName.toUpperCase(),
                setAttribute: function() {},
                getAttribute: function() { return null; },
                removeAttribute: function() {},
                appendChild: function() {},
                removeChild: function() {},
                innerHTML: '',
                outerHTML: '',
                textContent: ''
            };
        }

        createTextNode(text) {
            return {
                nodeType: 3,
                textContent: text
            };
        }

        addEventListener(type, listener) {
            // Simulated
        }

        removeEventListener(type, listener) {
            // Simulated
        }
    }

    globalThis.document = new Document(docProps);
}

/**
 * Window 对象属性
 */
if (typeof window === 'undefined') {
    globalThis.window = globalThis;
}

// 添加 window 属性
const windowProps = JSON.parse(Deno.core.ops.op_get_window_props());
Object.assign(globalThis, windowProps);

/**
 * Screen 对象
 */
if (typeof screen === 'undefined') {
    const screenData = JSON.parse(Deno.core.ops.op_get_screen());
    globalThis.screen = screenData;
}

/**
 * Console 增强
 */
if (typeof console === 'undefined' || !console.log) {
    globalThis.console = {
        log: function(...args) {
            const message = args.map(arg => {
                if (typeof arg === 'object') {
                    try {
                        return JSON.stringify(arg);
                    } catch (e) {
                        return String(arg);
                    }
                }
                return String(arg);
            }).join(' ');
            Deno.core.ops.op_console_log(message);
        },

        warn: function(...args) {
            const message = args.map(arg => String(arg)).join(' ');
            Deno.core.ops.op_console_warn(message);
        },

        error: function(...args) {
            const message = args.map(arg => String(arg)).join(' ');
            Deno.core.ops.op_console_error(message);
        },

        info: function(...args) {
            const message = args.map(arg => String(arg)).join(' ');
            Deno.core.ops.op_console_info(message);
        },

        debug: function(...args) {
            this.log(...args);
        },

        trace: function(...args) {
            this.log('[Trace]', ...args);
        },

        assert: function(condition, ...args) {
            if (!condition) {
                this.error('Assertion failed:', ...args);
            }
        },

        clear: function() {
            // Simulated
        },

        table: function(data) {
            this.log(JSON.stringify(data, null, 2));
        },

        time: function(label) {
            // Simulated
        },

        timeEnd: function(label) {
            // Simulated
        }
    };
}
