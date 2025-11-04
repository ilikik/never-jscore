use std::cell::RefCell;

/// JavaScript 执行结果存储
///
/// 用于在 Rust 和 JavaScript 之间传递执行结果。
/// 通过 Deno Core 的 op 机制，JavaScript 可以将结果存储到这里。
pub struct ResultStorage {
    pub value: RefCell<Option<String>>,
}

impl ResultStorage {
    pub fn new() -> Self {
        Self {
            value: RefCell::new(None),
        }
    }

    pub fn clear(&self) {
        *self.value.borrow_mut() = None;
    }

    pub fn store(&self, value: String) {
        *self.value.borrow_mut() = Some(value);
    }

    pub fn take(&self) -> Option<String> {
        self.value.borrow_mut().take()
    }
}

impl Default for ResultStorage {
    fn default() -> Self {
        Self::new()
    }
}
