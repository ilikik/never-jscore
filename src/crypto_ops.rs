// crypto_ops.rs - Cryptographic operations for JS reverse engineering
use deno_core::{extension, op2};
use base64::prelude::*;
use md5::Md5;
use sha1::Sha1;
use sha2::{Sha256, Sha512, Digest};
use hmac::{Hmac, Mac};

type HmacSha256 = Hmac<Sha256>;
type HmacSha1 = Hmac<Sha1>;
type HmacMd5 = Hmac<Md5>;

// ============================================
// Base64 Operations
// ============================================

#[op2]
#[string]
/// Base64 encode (standard encoding)
pub fn op_base64_encode(#[string] input: String) -> String {
    BASE64_STANDARD.encode(input.as_bytes())
}

#[op2]
#[string]
/// Base64 decode (standard encoding)
/// 返回 Latin-1/binary 字符串（每个字节对应一个字符，charCode = 字节值）
pub fn op_base64_decode(#[string] input: String) -> String {
    match BASE64_STANDARD.decode(&input) {
        Ok(bytes) => {
            // 将字节转换为 Latin-1 字符串（每个字节 0-255 对应一个 char）
            // 这样 JavaScript 可以通过 charCodeAt 获取原始字节值
            bytes.iter().map(|&b| b as char).collect()
        },
        Err(e) => format!("Error: Base64 decode failed: {}", e),
    }
}

#[op2]
#[string]
/// Base64 URL-safe encode
pub fn op_base64url_encode(#[string] input: String) -> String {
    BASE64_URL_SAFE.encode(input.as_bytes())
}

#[op2]
#[string]
/// Base64 URL-safe decode
pub fn op_base64url_decode(#[string] input: String) -> String {
    match BASE64_URL_SAFE.decode(&input) {
        Ok(bytes) => match String::from_utf8(bytes) {
            Ok(s) => s,
            Err(e) => format!("Error: UTF-8 decode failed: {}", e),
        },
        Err(e) => format!("Error: Base64URL decode failed: {}", e),
    }
}

// ============================================
// Hash Functions (MD5, SHA1, SHA256, SHA512)
// ============================================

#[op2]
#[string]
/// MD5 hash (hex output)
pub fn op_md5(#[string] input: String) -> String {
    let mut hasher = Md5::new();
    hasher.update(input.as_bytes());
    let result = hasher.finalize();
    hex::encode(result)
}

#[op2]
#[string]
/// SHA1 hash (hex output)
pub fn op_sha1(#[string] input: String) -> String {
    let mut hasher = Sha1::new();
    hasher.update(input.as_bytes());
    let result = hasher.finalize();
    hex::encode(result)
}

#[op2]
#[string]
/// SHA256 hash (hex output)
pub fn op_sha256(#[string] input: String) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input.as_bytes());
    let result = hasher.finalize();
    hex::encode(result)
}

#[op2]
#[string]
/// SHA512 hash (hex output)
pub fn op_sha512(#[string] input: String) -> String {
    let mut hasher = Sha512::new();
    hasher.update(input.as_bytes());
    let result = hasher.finalize();
    hex::encode(result)
}

// ============================================
// HMAC Operations
// ============================================

#[op2]
#[string]
/// HMAC-MD5 (hex output)
pub fn op_hmac_md5(#[string] key: String, #[string] message: String) -> String {
    match HmacMd5::new_from_slice(key.as_bytes()) {
        Ok(mut mac) => {
            mac.update(message.as_bytes());
            hex::encode(mac.finalize().into_bytes())
        },
        Err(e) => format!("Error: HMAC-MD5 key error: {}", e),
    }
}

#[op2]
#[string]
/// HMAC-SHA1 (hex output)
pub fn op_hmac_sha1(#[string] key: String, #[string] message: String) -> String {
    match HmacSha1::new_from_slice(key.as_bytes()) {
        Ok(mut mac) => {
            mac.update(message.as_bytes());
            hex::encode(mac.finalize().into_bytes())
        },
        Err(e) => format!("Error: HMAC-SHA1 key error: {}", e),
    }
}

#[op2]
#[string]
/// HMAC-SHA256 (hex output)
pub fn op_hmac_sha256(#[string] key: String, #[string] message: String) -> String {
    match HmacSha256::new_from_slice(key.as_bytes()) {
        Ok(mut mac) => {
            mac.update(message.as_bytes());
            hex::encode(mac.finalize().into_bytes())
        },
        Err(e) => format!("Error: HMAC-SHA256 key error: {}", e),
    }
}

// ============================================
// Hex Operations
// ============================================

#[op2]
#[string]
/// Hex encode
pub fn op_hex_encode(#[string] input: String) -> String {
    hex::encode(input.as_bytes())
}

#[op2]
#[string]
/// Hex decode
pub fn op_hex_decode(#[string] input: String) -> String {
    match hex::decode(&input) {
        Ok(bytes) => match String::from_utf8(bytes) {
            Ok(s) => s,
            Err(e) => format!("Error: UTF-8 decode failed: {}", e),
        },
        Err(e) => format!("Error: Hex decode failed: {}", e),
    }
}

// ============================================
// Random / Crypto Operations
// ============================================

#[op2]
#[string]
/// Generate a random UUID v4
pub fn op_crypto_random_uuid() -> String {
    // Generate 16 random bytes
    let mut bytes = [0u8; 16];
    crate::random_state::fill_bytes(&mut bytes);

    // Set version (4) and variant bits according to RFC 4122
    bytes[6] = (bytes[6] & 0x0f) | 0x40; // Version 4
    bytes[8] = (bytes[8] & 0x3f) | 0x80; // Variant 10

    // Format as UUID string
    format!(
        "{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}",
        bytes[0], bytes[1], bytes[2], bytes[3],
        bytes[4], bytes[5],
        bytes[6], bytes[7],
        bytes[8], bytes[9],
        bytes[10], bytes[11], bytes[12], bytes[13], bytes[14], bytes[15]
    )
}

#[op2]
#[string]
/// Generate random bytes as hex string (length in bytes)
pub fn op_crypto_get_random_values(length: u32) -> String {
    let mut buf = vec![0u8; length as usize];
    crate::random_state::fill_bytes(&mut buf);
    hex::encode(buf)
}

#[op2(fast)]
/// Generate a random number between 0 and 1
pub fn op_crypto_random() -> f64 {
    crate::random_state::random_f64()
}

// ============================================
// Extension Definition
// ============================================

extension!(
    crypto_ops,
    ops = [
        op_base64_encode,
        op_base64_decode,
        op_base64url_encode,
        op_base64url_decode,
        op_md5,
        op_sha1,
        op_sha256,
        op_sha512,
        op_hmac_md5,
        op_hmac_sha1,
        op_hmac_sha256,
        op_hex_encode,
        op_hex_decode,
        op_crypto_random_uuid,
        op_crypto_get_random_values,
        op_crypto_random,
    ],
);
