use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3::IntoPyObjectExt;
use serde_json::Value as JsonValue;

/// Python 对象转换为 JSON 值
///
/// 支持的类型：
/// - None -> null
/// - bool -> boolean
/// - int -> number
/// - float -> number
/// - str -> string
/// - list -> array
/// - dict -> object
#[inline]
pub fn python_to_json(obj: &Bound<'_, PyAny>) -> PyResult<JsonValue> {
    if obj.is_none() {
        Ok(JsonValue::Null)
    } else if let Ok(b) = obj.extract::<bool>() {
        Ok(JsonValue::Bool(b))
    } else if let Ok(i) = obj.extract::<i64>() {
        Ok(JsonValue::Number(i.into()))
    } else if let Ok(f) = obj.extract::<f64>() {
        serde_json::Number::from_f64(f)
            .map(JsonValue::Number)
            .ok_or_else(|| PyException::new_err("Invalid float"))
    } else if let Ok(s) = obj.extract::<String>() {
        Ok(JsonValue::String(s))
    } else if obj.is_instance_of::<PyList>() {
        let list = obj.downcast::<PyList>()?;
        let mut vec = Vec::with_capacity(list.len());
        for item in list.iter() {
            vec.push(python_to_json(&item)?);
        }
        Ok(JsonValue::Array(vec))
    } else if obj.is_instance_of::<PyDict>() {
        let dict = obj.downcast::<PyDict>()?;
        let mut map = serde_json::Map::with_capacity(dict.len());
        for (key, value) in dict.iter() {
            let key_str = key.extract::<String>()?;
            map.insert(key_str, python_to_json(&value)?);
        }
        Ok(JsonValue::Object(map))
    } else {
        Err(PyException::new_err("Unsupported Python type"))
    }
}

/// JSON 值转换为 Python 对象
///
/// 支持的类型：
/// - null -> None
/// - boolean -> bool
/// - number -> int/float
/// - string -> str
/// - array -> list
/// - object -> dict
#[inline]
pub fn json_to_python<'py>(py: Python<'py>, value: &JsonValue) -> PyResult<Bound<'py, PyAny>> {
    match value {
        JsonValue::Null => Ok(py.None().into_bound(py)),
        JsonValue::Bool(b) => Ok(b.into_bound_py_any(py)?),
        JsonValue::Number(n) => {
            if let Some(i) = n.as_i64() {
                Ok(i.into_bound_py_any(py)?)
            } else if let Some(f) = n.as_f64() {
                Ok(f.into_bound_py_any(py)?)
            } else {
                Ok(n.to_string().into_bound_py_any(py)?)
            }
        }
        JsonValue::String(s) => Ok(s.into_bound_py_any(py)?),
        JsonValue::Array(arr) => {
            let list = PyList::new(py, arr.iter().map(|_| py.None()).collect::<Vec<_>>())?;
            for (i, item) in arr.iter().enumerate() {
                list.set_item(i, json_to_python(py, item)?)?;
            }
            Ok(list.into_any())
        }
        JsonValue::Object(obj) => {
            let dict = PyDict::new(py);
            for (k, v) in obj {
                dict.set_item(k, json_to_python(py, v)?)?;
            }
            Ok(dict.into_any())
        }
    }
}
