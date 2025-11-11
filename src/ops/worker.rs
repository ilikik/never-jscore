// worker_ops.rs - Fake Worker API for JS reverse engineering
//
// This is NOT real multi-threading - everything runs in the same thread!
// This is sufficient for most JS reverse engineering scenarios where
// code only checks for Worker API existence.

use deno_core::{extension, op2};
use std::cell::RefCell;
use std::collections::HashMap;

thread_local! {
    static WORKERS: RefCell<HashMap<i32, WorkerData>> = RefCell::new(HashMap::new());
    static NEXT_WORKER_ID: RefCell<i32> = RefCell::new(1);
}

#[derive(Clone)]
struct WorkerData {
    script: String,
    ready: bool,
}

// ============================================
// Worker Operations (Fake - Single-threaded)
// ============================================

#[op2(fast)]
/// Create a fake worker (doesn't actually spawn a thread)
pub fn op_worker_create(#[string] script: String) -> i32 {
    NEXT_WORKER_ID.with(|next_id| {
        let id = *next_id.borrow();
        *next_id.borrow_mut() += 1;

        WORKERS.with(|workers| {
            workers.borrow_mut().insert(id, WorkerData {
                script,
                ready: true,
            });
        });

        id
    })
}

#[op2]
#[string]
/// Post message to worker (fake - just returns the message back)
pub fn op_worker_post_message(worker_id: i32, #[string] message: String) -> String {
    WORKERS.with(|workers| {
        if workers.borrow().contains_key(&worker_id) {
            // Fake processing - just echo back
            format!("{{\"type\":\"message\",\"data\":{}}}", message)
        } else {
            r#"{"type":"error","message":"Worker not found"}"#.to_string()
        }
    })
}

#[op2(fast)]
/// Terminate worker
pub fn op_worker_terminate(worker_id: i32) {
    WORKERS.with(|workers| {
        workers.borrow_mut().remove(&worker_id);
    });
}

#[op2(fast)]
/// Check if worker exists
pub fn op_worker_exists(worker_id: i32) -> bool {
    WORKERS.with(|workers| {
        workers.borrow().contains_key(&worker_id)
    })
}

// ============================================
// Extension Definition
// ============================================

extension!(
    worker_ops,
    ops = [
        op_worker_create,
        op_worker_post_message,
        op_worker_terminate,
        op_worker_exists,
    ],
);
