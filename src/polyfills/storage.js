// ============================================
// localStorage / sessionStorage Polyfill
// 浏览器本地存储 API
// ============================================

/**
 * localStorage 实现
 */
if (typeof localStorage === 'undefined') {
    class Storage {
        setItem(key, value) {
            const result = Deno.core.ops.op_local_storage_set_item(String(key), String(value));
            if (result !== 'OK') {
                throw new Error(result);
            }
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

    globalThis.localStorage = new Storage();
}

/**
 * sessionStorage 实现
 */
if (typeof sessionStorage === 'undefined') {
    class SessionStorage {
        setItem(key, value) {
            const result = Deno.core.ops.op_session_storage_set_item(String(key), String(value));
            if (result !== 'OK') {
                throw new Error(result);
            }
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

    globalThis.sessionStorage = new SessionStorage();
}
