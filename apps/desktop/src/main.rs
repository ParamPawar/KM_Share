#[tauri::command]
async fn discover_peers() -> Vec<String> {
    core_discovery::discover_service().await.unwrap();
    vec!["192.168.0.42".into()] // mock until integrated
}

#[tokio::main]
async fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![discover_peers])
        .run(tauri::generate_context!())
        .expect("❌ error while running Tauri app");
}
