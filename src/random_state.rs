// random_state.rs - Seedable RNG state management
use rand::rngs::StdRng;
use rand::SeedableRng;
use std::cell::RefCell;

thread_local! {
    /// Thread-local RNG state
    /// When seed is set, uses StdRng with that seed
    /// Otherwise uses thread_rng() behavior
    static RNG_STATE: RefCell<RngState> = RefCell::new(RngState::default());
}

struct RngState {
    /// Seeded RNG (if seed was set)
    seeded_rng: Option<StdRng>,
    /// Current seed value (for debugging)
    seed: Option<u64>,
}

impl Default for RngState {
    fn default() -> Self {
        Self {
            seeded_rng: None,
            seed: None,
        }
    }
}

/// Set the random seed for deterministic random number generation
pub fn set_random_seed(seed: u64) {
    RNG_STATE.with(|state| {
        let mut state = state.borrow_mut();
        state.seed = Some(seed);
        state.seeded_rng = Some(StdRng::seed_from_u64(seed));
    });
}

/// Reset to non-deterministic random number generation
pub fn reset_random_seed() {
    RNG_STATE.with(|state| {
        let mut state = state.borrow_mut();
        state.seed = None;
        state.seeded_rng = None;
    });
}

/// Get current seed (if set)
pub fn get_random_seed() -> Option<u64> {
    RNG_STATE.with(|state| state.borrow().seed)
}

/// Generate a random f64 between 0 and 1
pub fn random_f64() -> f64 {
    use rand::Rng;

    RNG_STATE.with(|state| {
        let mut state = state.borrow_mut();
        if let Some(ref mut rng) = state.seeded_rng {
            rng.gen::<f64>()
        } else {
            rand::thread_rng().gen::<f64>()
        }
    })
}

/// Fill buffer with random bytes
pub fn fill_bytes(buf: &mut [u8]) {
    use rand::RngCore;

    RNG_STATE.with(|state| {
        let mut state = state.borrow_mut();
        if let Some(ref mut rng) = state.seeded_rng {
            rng.fill_bytes(buf);
        } else {
            rand::thread_rng().fill_bytes(buf);
        }
    });
}

/// Generate a random u32
pub fn random_u32() -> u32 {
    use rand::Rng;

    RNG_STATE.with(|state| {
        let mut state = state.borrow_mut();
        if let Some(ref mut rng) = state.seeded_rng {
            rng.gen::<u32>()
        } else {
            rand::thread_rng().gen::<u32>()
        }
    })
}
