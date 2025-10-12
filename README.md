# 🔗 Smart_KVM

Smart_KVM is an **open-source, cross-platform LAN utility** for seamless **keyboard & mouse sharing, clipboard sync, file/media sharing, and audio streaming** between devices.  
Inspired by **Microsoft Borderless** and **Glidex**, but designed to be **fast, privacy-focused, and open**.

---

## 🎯 Vision

> *“A single keyboard, mouse, and clipboard for all your devices — Windows, Linux, macOS, Android.”*  

- **Zero Cloud Dependency** → 100% local network communication.  
- **Low Latency** → Built with **Rust + WebRTC** for speed.  
- **Open Source** → Transparent, hackable, community-driven.  
- **Cross-Platform** → Works across desktops and mobiles.  

---

## 🏗️ System Design

📹 [System Design Video](#) *(https://www.youtube.com/@Eye_TechLab)*  

High-level overview:  
1. **Discovery Layer** → Devices find each other via **mDNS/DNS-SD**  
2. **Transport Layer** → Secure P2P data channels via **WebRTC**  
3. **Modules**:  
   - Keyboard & Mouse Input Forwarding  
   - Clipboard Sync  
   - File & Media Sharing  
   - Audio Forwarding (like a network “Bluetooth Receiver”)  
4. **UI Layer** → Cross-platform desktop/mobile apps powered by **Tauri + React**  

---

## 📚 Roadmap

### ✅ Phase 1 (Week 1 - Prototype)
- [x] Rust workspace setup  
- [x] mDNS discovery service (LAN peer finding)  
- [x] WebRTC transport stub (ping/pong)  
- [x] Tauri desktop app (basic UI with peer list)  

### 🚧 Phase 2 (Weeks 2–4)
- [ ] Secure pairing (QR code exchange, TOFU trust model)  
- [ ] Real WebRTC signaling (via local channel)  
- [ ] Clipboard sync  
- [ ] File transfer MVP  

### 🚀 Phase 3
- [ ] Input sharing (keyboard + mouse)  
- [ ] Audio sharing (LAN “Bluetooth receiver”)  
- [ ] Mobile client (Android prototype)  

### 🌐 Phase 4
- [ ] Full cross-platform support (macOS, Linux, Windows, Android)  
- [ ] Config UI for manual + auto network config  
- [ ] Advanced admin tools  

---

## 🔧 Tech Stack

- **Language** → [Rust](https://www.rust-lang.org/)  
- **Runtime** → [Tokio](https://tokio.rs/) (async)  
- **Discovery** → [mDNS](https://en.wikipedia.org/wiki/Multicast_DNS)  
- **Transport** → [WebRTC-rs](https://github.com/webrtc-rs/webrtc)  
- **UI Framework** → [Tauri](https://tauri.app/) + [React (Vite)](https://vitejs.dev/)  
- **Logging** → [tracing](https://github.com/tokio-rs/tracing)  

---

## 🚀 Getting Started

### Prerequisites
- Rust (`rustup` → [Install Rust](https://rustup.rs/))  
- Node.js (LTS recommended)  
- Tauri CLI  
  ```bash
  cargo install tauri-cli
