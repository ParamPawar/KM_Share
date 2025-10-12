import React, { useState } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [peers, setPeers] = useState([]);

  const sayHello = async () => {
    const response = await invoke("hello");
    setMessage(response);
  };

  const getPeers = async () => {
    const result = await invoke("discover_peers");
    setPeers(result);
  };

  return (
    <div className="app-container">
      <h1>Smart KVM</h1>
      <button onClick={sayHello}>Say Hello</button>
      <p>{message}</p>
      <button onClick={getPeers}>Discover Peers</button>
      <ul>
        {peers.map((peer, idx) => (
          <li key={idx}>{peer.ip}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;