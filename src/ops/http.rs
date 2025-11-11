// fetch_ops.rs - HTTP Fetch operations for Node.js compatibility
use deno_core::{extension, op2};
use reqwest::blocking::Client;
use serde_json::{json, Value as JsonValue};
use std::collections::HashMap;
use std::time::Duration;

// ============================================
// HTTP Fetch Operations
// ============================================

#[op2]
#[string]
/// HTTP Fetch 操作（同步版本，用于兼容）
///
/// # Arguments
/// * `url` - 请求 URL
/// * `options_json` - 请求选项（JSON 字符串）
///   {
///     "method": "GET|POST|PUT|DELETE|PATCH|HEAD",
///     "headers": {"Header-Name": "value"},
///     "body": "request body",
///     "timeout": 30000  // 毫秒
///   }
///
/// # Returns
/// JSON 字符串包含响应信息：
/// {
///   "ok": true,
///   "status": 200,
///   "statusText": "OK",
///   "headers": {"content-type": "application/json"},
///   "body": "response body text",
///   "error": null
/// }
pub fn op_fetch(#[string] url: String, #[string] options_json: String) -> String {
    // 解析请求选项
    let options: JsonValue = match serde_json::from_str(&options_json) {
        Ok(opts) => opts,
        Err(e) => {
            return json!({
                "ok": false,
                "status": 0,
                "statusText": "",
                "headers": {},
                "body": "",
                "error": format!("Invalid options JSON: {}", e)
            }).to_string();
        }
    };

    // 提取请求参数
    let method = options["method"].as_str().unwrap_or("GET").to_uppercase();
    let headers_obj = options["headers"].as_object();
    let body = options["body"].as_str().unwrap_or("");
    let timeout_ms = options["timeout"].as_u64().unwrap_or(30000);

    // 创建 HTTP 客户端
    let client = match Client::builder()
        .timeout(Duration::from_millis(timeout_ms))
        .build()
    {
        Ok(c) => c,
        Err(e) => {
            return json!({
                "ok": false,
                "status": 0,
                "statusText": "",
                "headers": {},
                "body": "",
                "error": format!("Failed to create HTTP client: {}", e)
            }).to_string();
        }
    };

    // 构建请求
    let mut request_builder = match method.as_str() {
        "GET" => client.get(&url),
        "POST" => client.post(&url),
        "PUT" => client.put(&url),
        "DELETE" => client.delete(&url),
        "PATCH" => client.patch(&url),
        "HEAD" => client.head(&url),
        _ => {
            return json!({
                "ok": false,
                "status": 0,
                "statusText": "",
                "headers": {},
                "body": "",
                "error": format!("Unsupported HTTP method: {}", method)
            }).to_string();
        }
    };

    // 添加请求头
    if let Some(headers) = headers_obj {
        for (key, value) in headers {
            if let Some(value_str) = value.as_str() {
                request_builder = request_builder.header(key, value_str);
            }
        }
    }

    // 添加请求体（仅对非 GET/HEAD 请求）
    if !body.is_empty() && method != "GET" && method != "HEAD" {
        request_builder = request_builder.body(body.to_string());
    }

    // 发送请求
    let response = match request_builder.send() {
        Ok(resp) => resp,
        Err(e) => {
            return json!({
                "ok": false,
                "status": 0,
                "statusText": "",
                "headers": {},
                "body": "",
                "error": format!("Request failed: {}", e)
            }).to_string();
        }
    };

    // 提取响应信息
    let status = response.status().as_u16();
    let status_text = response.status().canonical_reason().unwrap_or("").to_string();
    let ok = response.status().is_success();

    // 提取响应头
    let mut response_headers = HashMap::new();
    for (key, value) in response.headers() {
        if let Ok(value_str) = value.to_str() {
            response_headers.insert(key.as_str().to_string(), value_str.to_string());
        }
    }

    // 读取响应体
    let body_text = match response.text() {
        Ok(text) => text,
        Err(e) => {
            return json!({
                "ok": false,
                "status": status,
                "statusText": status_text,
                "headers": response_headers,
                "body": "",
                "error": format!("Failed to read response body: {}", e)
            }).to_string();
        }
    };

    // 构建响应 JSON
    json!({
        "ok": ok,
        "status": status,
        "statusText": status_text,
        "headers": response_headers,
        "body": body_text,
        "error": null
    }).to_string()
}

#[op2]
#[string]
/// 简化的 HTTP GET 请求
///
/// # Arguments
/// * `url` - 请求 URL
///
/// # Returns
/// 响应文本，失败时返回错误信息
pub fn op_http_get(#[string] url: String) -> String {
    match Client::new().get(&url).send() {
        Ok(response) => {
            match response.text() {
                Ok(text) => text,
                Err(e) => format!("Error: Failed to read response: {}", e),
            }
        },
        Err(e) => format!("Error: HTTP request failed: {}", e),
    }
}

#[op2]
#[string]
/// 简化的 HTTP POST 请求（JSON）
///
/// # Arguments
/// * `url` - 请求 URL
/// * `json_body` - JSON 请求体字符串
///
/// # Returns
/// 响应文本，失败时返回错误信息
pub fn op_http_post_json(#[string] url: String, #[string] json_body: String) -> String {
    let client = Client::new();

    match client.post(&url)
        .header("Content-Type", "application/json")
        .body(json_body)
        .send()
    {
        Ok(response) => {
            match response.text() {
                Ok(text) => text,
                Err(e) => format!("Error: Failed to read response: {}", e),
            }
        },
        Err(e) => format!("Error: HTTP request failed: {}", e),
    }
}

// ============================================
// Extension Definition
// ============================================

extension!(
    fetch_ops,
    ops = [
        op_fetch,
        op_http_get,
        op_http_post_json,
    ],
);
