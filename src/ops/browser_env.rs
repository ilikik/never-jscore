// src/ops/browser_env.rs
// 浏览器环境对象：window, navigator, location, document
// 用于 JS 补环境

use deno_core::{extension, op2};
use serde_json::json;

// ============================================
// Navigator Operations
// ============================================

#[op2]
#[string]
/// 获取 navigator 对象信息
pub fn op_get_navigator() -> String {
    json!({
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "platform": "Win32",
        "language": "zh-CN",
        "languages": ["zh-CN", "zh", "en"],
        "onLine": true,
        "cookieEnabled": true,
        "doNotTrack": "1",
        "hardwareConcurrency": 8,
        "maxTouchPoints": 0,
        "vendor": "Google Inc.",
        "vendorSub": "",
        "product": "Gecko",
        "productSub": "20030107",
        "appName": "Netscape",
        "appCodeName": "Mozilla",
        "appVersion": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "webdriver": false
    }).to_string()
}

// ============================================
// Location Operations
// ============================================

#[op2]
#[string]
/// 获取 location 对象信息
pub fn op_get_location(#[string] url: String) -> String {
    // 简单的 URL 解析
    let default_url = "https://example.com/";
    let parse_url = if url.is_empty() { default_url } else { &url };

    // 基础解析（简化版）
    let parts: Vec<&str> = parse_url.split("://").collect();
    let (protocol, rest) = if parts.len() > 1 {
        (parts[0], parts[1])
    } else {
        ("https", parts[0])
    };

    let parts: Vec<&str> = rest.splitn(2, '/').collect();
    let host = parts[0];
    let pathname = if parts.len() > 1 {
        format!("/{}", parts[1])
    } else {
        "/".to_string()
    };

    let parts: Vec<&str> = host.splitn(2, ':').collect();
    let hostname = parts[0];
    let port = if parts.len() > 1 { parts[1] } else { "" };

    json!({
        "href": parse_url,
        "protocol": format!("{}:", protocol),
        "host": host,
        "hostname": hostname,
        "port": port,
        "pathname": pathname,
        "search": "",
        "hash": "",
        "origin": format!("{}://{}", protocol, host)
    }).to_string()
}

// ============================================
// Document Operations
// ============================================

#[op2]
#[string]
/// 获取 document 基础属性
pub fn op_get_document_props() -> String {
    json!({
        "documentElement": {
            "tagName": "HTML",
            "nodeName": "HTML"
        },
        "head": {
            "tagName": "HEAD",
            "nodeName": "HEAD"
        },
        "body": {
            "tagName": "BODY",
            "nodeName": "BODY"
        },
        "readyState": "complete",
        "title": "",
        "URL": "https://example.com/",
        "domain": "example.com",
        "cookie": "",
        "referrer": "",
        "characterSet": "UTF-8",
        "charset": "UTF-8",
        "compatMode": "CSS1Compat",
        "hidden": false,
        "visibilityState": "visible"
    }).to_string()
}

// ============================================
// Window Operations
// ============================================

#[op2]
#[string]
/// 获取 window 对象属性
pub fn op_get_window_props() -> String {
    json!({
        "innerWidth": 1920,
        "innerHeight": 1080,
        "outerWidth": 1920,
        "outerHeight": 1080,
        "screenX": 0,
        "screenY": 0,
        "screenLeft": 0,
        "screenTop": 0,
        "scrollX": 0,
        "scrollY": 0,
        "pageXOffset": 0,
        "pageYOffset": 0,
        "devicePixelRatio": 1.0,
        "name": "",
        "closed": false,
        "isSecureContext": true
    }).to_string()
}

#[op2]
#[string]
/// 获取 screen 对象属性
pub fn op_get_screen() -> String {
    json!({
        "width": 1920,
        "height": 1080,
        "availWidth": 1920,
        "availHeight": 1040,
        "colorDepth": 24,
        "pixelDepth": 24,
        "orientation": {
            "type": "landscape-primary",
            "angle": 0
        }
    }).to_string()
}

// ============================================
// Console Operations (增强版)
// ============================================

#[op2]
#[string]
/// console.log 实现（输出到 Rust）
pub fn op_console_log(#[string] message: String) -> String {
    println!("[JS Console] {}", message);
    "OK".to_string()
}

#[op2]
#[string]
/// console.warn 实现
pub fn op_console_warn(#[string] message: String) -> String {
    eprintln!("[JS Warning] {}", message);
    "OK".to_string()
}

#[op2]
#[string]
/// console.error 实现
pub fn op_console_error(#[string] message: String) -> String {
    eprintln!("[JS Error] {}", message);
    "OK".to_string()
}

#[op2]
#[string]
/// console.info 实现
pub fn op_console_info(#[string] message: String) -> String {
    println!("[JS Info] {}", message);
    "OK".to_string()
}

// ============================================
// URL Operations
// ============================================

#[op2]
#[string]
/// 解析 URL 并返回各个组成部分
pub fn op_parse_url(#[string] url: String) -> String {
    // 简单的 URL 解析
    let url_trimmed = url.trim();

    // 解析协议
    let (protocol, rest) = if let Some(idx) = url_trimmed.find("://") {
        let protocol = &url_trimmed[..idx];
        let rest = &url_trimmed[idx+3..];
        (protocol.to_string(), rest.to_string())
    } else {
        ("http".to_string(), url_trimmed.to_string())
    };

    // 解析 hostname, port, pathname, search, hash
    let mut hostname = String::new();
    let mut port = String::new();
    let mut pathname = String::from("/");
    let mut search = String::new();
    let mut hash = String::new();

    // 分离 hash
    let (before_hash, after_hash) = if let Some(idx) = rest.find('#') {
        let before = &rest[..idx];
        let after = &rest[idx+1..];
        (before, after)
    } else {
        (rest.as_str(), "")
    };
    hash = after_hash.to_string();

    // 分离 search
    let (before_search, after_search) = if let Some(idx) = before_hash.find('?') {
        let before = &before_hash[..idx];
        let after = &before_hash[idx+1..];
        (before, after)
    } else {
        (before_hash, "")
    };
    search = after_search.to_string();

    // 分离 hostname/port 和 pathname
    let (host_part, path_part) = if let Some(idx) = before_search.find('/') {
        let host = &before_search[..idx];
        let path = &before_search[idx..];
        (host, path)
    } else {
        (before_search, "/")
    };
    pathname = path_part.to_string();

    // 分离 hostname 和 port
    if let Some(idx) = host_part.find(':') {
        hostname = host_part[..idx].to_string();
        port = host_part[idx+1..].to_string();
    } else {
        hostname = host_part.to_string();
        port = if protocol == "https" { "443".to_string() } else { "80".to_string() };
    }

    let host = if port == "80" || port == "443" {
        hostname.clone()
    } else {
        format!("{}:{}", hostname, port)
    };

    let origin = format!("{}://{}", protocol, host);

    json!({
        "href": url_trimmed,
        "protocol": format!("{}:", protocol),
        "hostname": hostname,
        "port": port,
        "host": host,
        "pathname": pathname,
        "search": if search.is_empty() { String::new() } else { format!("?{}", search) },
        "hash": if hash.is_empty() { String::new() } else { format!("#{}", hash) },
        "origin": origin
    }).to_string()
}

// ============================================
// Extension Definition
// ============================================

extension!(
    browser_env_ops,
    ops = [
        op_get_navigator,
        op_get_location,
        op_get_document_props,
        op_get_window_props,
        op_get_screen,
        op_console_log,
        op_console_warn,
        op_console_error,
        op_console_info,
        op_parse_url,
    ],
);
