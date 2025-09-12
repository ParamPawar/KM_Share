use serde::Serialize;

#[derive(Serialize)]
struct Peer {
    ip: String,
}

#[tauri::command]
async fn discover_peers() -> Vec<Peer> {
    // Simulate peer discovery with dummy data
    vec![
        Peer { ip: "192.168.0.42".into() },
        Peer { ip: "192.168.0.43".into() },
    ]
}

#[tokio::main]
async fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![discover_peers])
        .run(tauri::generate_context!())
        .expect("❌ error while running Tauri app");
}
