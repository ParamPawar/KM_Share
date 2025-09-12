import React, { useState } from "react";
import { invoke } from "@tauri-apps/api/tauri";

export default function App() {
  const [peers, setPeers] = useState([]);

  async function handleDiscover() {
    const result = await invoke("discover_peers");
    setPeers(result);
  }

  return (
    <div style={{ fontFamily: "sans-serif", padding: "20px" }}>
      <h1>🔗 Smart_KVM (Week 1)</h1>
      <button onClick={handleDiscover}>Discover Peers</button>

      <ul>
        {peers.map((peer, i) => (
          <li key={i}>{peer.ip}</li>
        ))}
      </ul>
    </div>
  );
}
