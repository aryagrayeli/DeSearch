/*
 * Example smart contract written in RUST
 *
 * Learn more about writing NEAR smart contracts with Rust:
 * https://near-docs.io/develop/Contract
 *
 */

use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::{log, near_bindgen};
use near_sdk::collections::{ Vector };

// Define the default message
const DEFAULT_MESSAGE: &str = "Hello";

// Define the contract structure
#[near_bindgen]
#[derive(BorshDeserialize, BorshSerialize)]
pub struct Contract {
    search: Vector<String>,
}

// Define the default, which automatically initializes the contract
impl Default for Contract{
    fn default() -> Self {
        Self { 
            search: Vector::new(b"m")
        }
    }
}

// Implement the contract structure
#[near_bindgen]
impl Contract {
    //search = vec!["trest test st etst".to_string()];

    pub fn new() -> Self {
        //assert!(env::state_read::<Self>().is_none(), "Already initialized");
        let mut contract = Self {
            search: Vector::new(b"m")
        };

        contract
    }

    // Public method - returns the greeting saved, defaulting to DEFAULT_MESSAGE
    pub fn get_search(&self) -> String {
        return "".to_string();
    }

    // Public method - accepts a greeting, such as "howdy", and records it
    pub fn set_search(&mut self, search: String) {
        // Use env::log to record logs permanently to the blockchain!
        self.search.push(&search);
        log!("Saving greeting {}", search);
        self.search.push(search);
        self.search = vec!["".to_string()];
    }
}
