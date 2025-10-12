#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use serde::Serialize;
use tauri::Manager;

#[tauri::command]
async fn hello() -> String {
    "Hello from Rust!".into()
}

#[derive(Serialize)]
struct Peer {
    ip: String,
}

#[tauri::command]
async fn discover_peers() -> Vec<Peer> {
    vec![
        Peer { ip: "192.168.0.42".into() },
        Peer { ip: "192.168.0.43".into() },
    ]
}

#[tokio::main]
async fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![hello, discover_peers])
        .run(tauri::generate_context!())
        .expect("error while running Tauri app");
}
