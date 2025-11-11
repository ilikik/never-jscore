// src/ops/web_storage.rs
// localStorage 和 sessionStorage 实现
// 用于 JS 补环境，模拟浏览器存储API

use deno_core::{extension, op2};
use std::collections::HashMap;
use std::sync::RwLock;

// 全局存储（线程安全）
lazy_static::lazy_static! {
    static ref LOCAL_STORAGE: RwLock<HashMap<String, String>> = RwLock::new(HashMap::new());
    static ref SESSION_STORAGE: RwLock<HashMap<String, String>> = RwLock::new(HashMap::new());
}

// ============================================
// localStorage Operations
// ============================================

#[op2]
#[string]
/// 设置 localStorage 项
pub fn op_local_storage_set_item(#[string] key: String, #[string] value: String) -> String {
    match LOCAL_STORAGE.write() {
        Ok(mut storage) => {
            storage.insert(key, value);
            "OK".to_string()
        },
        Err(e) => format!("Error: Failed to write to localStorage: {}", e),
    }
}

#[op2]
#[string]
/// 获取 localStorage 项
pub fn op_local_storage_get_item(#[string] key: String) -> String {
    match LOCAL_STORAGE.read() {
        Ok(storage) => {
            storage.get(&key).cloned().unwrap_or_else(|| "null".to_string())
        },
        Err(e) => format!("Error: Failed to read from localStorage: {}", e),
    }
}

#[op2]
#[string]
/// 删除 localStorage 项
pub fn op_local_storage_remove_item(#[string] key: String) -> String {
    match LOCAL_STORAGE.write() {
        Ok(mut storage) => {
            storage.remove(&key);
            "OK".to_string()
        },
        Err(e) => format!("Error: Failed to remove from localStorage: {}", e),
    }
}

#[op2]
#[string]
/// 清空 localStorage
pub fn op_local_storage_clear() -> String {
    match LOCAL_STORAGE.write() {
        Ok(mut storage) => {
            storage.clear();
            "OK".to_string()
        },
        Err(e) => format!("Error: Failed to clear localStorage: {}", e),
    }
}

#[op2]
#[string]
/// 获取 localStorage 所有键
pub fn op_local_storage_keys() -> String {
    match LOCAL_STORAGE.read() {
        Ok(storage) => {
            let keys: Vec<String> = storage.keys().map(|k| format!("\"{}\"", k)).collect();
            format!("[{}]", keys.join(","))
        },
        Err(e) => format!("Error: Failed to read localStorage keys: {}", e),
    }
}

#[op2(fast)]
/// 获取 localStorage 长度
pub fn op_local_storage_length() -> u32 {
    LOCAL_STORAGE.read().map(|s| s.len() as u32).unwrap_or(0)
}

// ============================================
// sessionStorage Operations
// ============================================

#[op2]
#[string]
/// 设置 sessionStorage 项
pub fn op_session_storage_set_item(#[string] key: String, #[string] value: String) -> String {
    match SESSION_STORAGE.write() {
        Ok(mut storage) => {
            storage.insert(key, value);
            "OK".to_string()
        },
        Err(e) => format!("Error: Failed to write to sessionStorage: {}", e),
    }
}

#[op2]
#[string]
/// 获取 sessionStorage 项
pub fn op_session_storage_get_item(#[string] key: String) -> String {
    match SESSION_STORAGE.read() {
        Ok(storage) => {
            storage.get(&key).cloned().unwrap_or_else(|| "null".to_string())
        },
        Err(e) => format!("Error: Failed to read from sessionStorage: {}", e),
    }
}

#[op2]
#[string]
/// 删除 sessionStorage 项
pub fn op_session_storage_remove_item(#[string] key: String) -> String {
    match SESSION_STORAGE.write() {
        Ok(mut storage) => {
            storage.remove(&key);
            "OK".to_string()
        },
        Err(e) => format!("Error: Failed to remove from sessionStorage: {}", e),
    }
}

#[op2]
#[string]
/// 清空 sessionStorage
pub fn op_session_storage_clear() -> String {
    match SESSION_STORAGE.write() {
        Ok(mut storage) => {
            storage.clear();
            "OK".to_string()
        },
        Err(e) => format!("Error: Failed to clear sessionStorage: {}", e),
    }
}

#[op2]
#[string]
/// 获取 sessionStorage 所有键
pub fn op_session_storage_keys() -> String {
    match SESSION_STORAGE.read() {
        Ok(storage) => {
            let keys: Vec<String> = storage.keys().map(|k| format!("\"{}\"", k)).collect();
            format!("[{}]", keys.join(","))
        },
        Err(e) => format!("Error: Failed to read sessionStorage keys: {}", e),
    }
}

#[op2(fast)]
/// 获取 sessionStorage 长度
pub fn op_session_storage_length() -> u32 {
    SESSION_STORAGE.read().map(|s| s.len() as u32).unwrap_or(0)
}

// ============================================
// Extension Definition
// ============================================

extension!(
    web_storage_ops,
    ops = [
        op_local_storage_set_item,
        op_local_storage_get_item,
        op_local_storage_remove_item,
        op_local_storage_clear,
        op_local_storage_keys,
        op_local_storage_length,
        op_session_storage_set_item,
        op_session_storage_get_item,
        op_session_storage_remove_item,
        op_session_storage_clear,
        op_session_storage_keys,
        op_session_storage_length,
    ],
);
