// timer_ops.rs - Fake timer APIs for JS reverse engineering
//
// These are NOT real async timers - they execute immediately!
// This is sufficient for most JS reverse engineering scenarios where
// code only checks for API existence, not actual timing behavior.

use deno_core::{extension, op2};
use std::cell::RefCell;
use std::collections::HashMap;

thread_local! {
    static TIMER_CALLBACKS: RefCell<HashMap<i32, String>> = RefCell::new(HashMap::new());
    static NEXT_TIMER_ID: RefCell<i32> = RefCell::new(1);
}

// ============================================
// setTimeout / setInterval (Fake - Immediate Execution)
// ============================================

#[op2(fast)]
/// Fake setTimeout - returns a timer ID but doesn't actually schedule anything
/// The callback will be executed immediately when op_run_timers is called
pub fn op_set_timeout(callback_id: i32, _delay: i32) -> i32 {
    NEXT_TIMER_ID.with(|next_id| {
        let id = *next_id.borrow();
        *next_id.borrow_mut() += 1;

        TIMER_CALLBACKS.with(|callbacks| {
            callbacks.borrow_mut().insert(id, format!("timeout_{}", callback_id));
        });

        id
    })
}

#[op2(fast)]
/// Fake setInterval - same as setTimeout (doesn't actually repeat)
pub fn op_set_interval(callback_id: i32, _delay: i32) -> i32 {
    NEXT_TIMER_ID.with(|next_id| {
        let id = *next_id.borrow();
        *next_id.borrow_mut() += 1;

        TIMER_CALLBACKS.with(|callbacks| {
            callbacks.borrow_mut().insert(id, format!("interval_{}", callback_id));
        });

        id
    })
}

#[op2(fast)]
/// Clear timeout/interval
pub fn op_clear_timeout(timer_id: i32) {
    TIMER_CALLBACKS.with(|callbacks| {
        callbacks.borrow_mut().remove(&timer_id);
    });
}

#[op2(fast)]
/// Clear interval (same as clearTimeout)
pub fn op_clear_interval(timer_id: i32) {
    TIMER_CALLBACKS.with(|callbacks| {
        callbacks.borrow_mut().remove(&timer_id);
    });
}

// ============================================
// Extension Definition
// ============================================

extension!(
    timer_ops,
    ops = [
        op_set_timeout,
        op_set_interval,
        op_clear_timeout,
        op_clear_interval,
    ],
);
