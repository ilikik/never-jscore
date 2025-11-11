// encoding_ops.rs - Encoding operations for JS reverse engineering
use deno_core::{extension, op2};

// ============================================
// URL Encoding Operations
// ============================================

#[op2]
#[string]
/// URL encode (encode all special characters)
pub fn op_url_encode(#[string] input: String) -> String {
    urlencoding::encode(&input).to_string()
}

#[op2]
#[string]
/// URL decode
pub fn op_url_decode(#[string] input: String) -> String {
    match urlencoding::decode(&input) {
        Ok(s) => s.to_string(),
        Err(e) => format!("Error: URL decode failed: {}", e),
    }
}

// ============================================
// Percent Encoding Operations (Component-safe)
// ============================================

#[op2]
#[string]
/// Percent encode (equivalent to encodeURIComponent)
pub fn op_encode_uri_component(#[string] input: String) -> String {
    use percent_encoding::{utf8_percent_encode, NON_ALPHANUMERIC};
    utf8_percent_encode(&input, NON_ALPHANUMERIC).to_string()
}

#[op2]
#[string]
/// Percent encode (equivalent to encodeURI - preserves URI structure)
pub fn op_encode_uri(#[string] input: String) -> String {
    use percent_encoding::{utf8_percent_encode, AsciiSet, CONTROLS};

    // Define characters that should NOT be encoded by encodeURI
    // This matches JavaScript's encodeURI behavior
    const URI_RESERVED: &AsciiSet = &CONTROLS
        .add(b' ')
        .add(b'"')
        .add(b'<')
        .add(b'>')
        .add(b'`');

    utf8_percent_encode(&input, URI_RESERVED).to_string()
}

#[op2]
#[string]
/// Percent decode (equivalent to decodeURIComponent / decodeURI)
pub fn op_decode_uri_component(#[string] input: String) -> String {
    use percent_encoding::percent_decode_str;

    match percent_decode_str(&input).decode_utf8() {
        Ok(s) => s.to_string(),
        Err(e) => format!("Error: Percent decode failed: {}", e),
    }
}

// ============================================
// Extension Definition
// ============================================

extension!(
    encoding_ops,
    ops = [
        op_url_encode,
        op_url_decode,
        op_encode_uri_component,
        op_encode_uri,
        op_decode_uri_component,
    ],
);
