// random_ops.rs - Operations for controlling random number generation
use deno_core::{extension, op2};

#[op2(fast)]
/// Set the random seed for deterministic random number generation
///
/// # Arguments
/// * `seed` - The seed value (u64)
///
/// # Example
/// ```javascript
/// Deno.core.ops.op_set_random_seed(12345);
/// Math.random(); // Will be deterministic
/// ```
pub fn op_set_random_seed(seed: u32) {
    crate::random_state::set_random_seed(seed as u64);
}

#[op2(fast)]
/// Reset to non-deterministic random number generation
pub fn op_reset_random_seed() {
    crate::random_state::reset_random_seed();
}

#[op2(fast)]
/// Get current random seed (returns 0 if not set)
pub fn op_get_random_seed() -> u32 {
    crate::random_state::get_random_seed().unwrap_or(0) as u32
}

extension!(
    random_ops,
    ops = [
        op_set_random_seed,
        op_reset_random_seed,
        op_get_random_seed,
    ],
);
