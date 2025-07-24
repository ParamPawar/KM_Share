# Multi-PC Mouse & Keyboard Sharing

This project is a desktop application that enables seamless control of multiple computers (up to four) using a single mouse and keyboard over a local network, similar to Microsoft Mouse Without Borders. Built with Python, PyQt5, and secure TCP sockets, it supports input sharing, real-time clipboard synchronization, and file transfers with AES encryption for security. The application is primarily Windows-compatible but designed with modularity for future macOS/Linux support.

## Features

- **Multi-Computer Control**: Seamlessly move your mouse and use your keyboard across multiple computers on the same LAN.
- **Clipboard Sharing**: Copy and paste text, images, and other clipboard content between connected devices.
- **File Transfer**: Transfer files to a designated folder on connected devices (drag-and-drop UI planned).
- **Secure Communication**: All data, including input events and file transfers, is encrypted using AES.
- **Custom Layout Configuration**: Arrange screens virtually for intuitive control (layout editor in development).
- **System Tray Integration**: Runs unobtrusively with notifications for connection status and file transfers.
- **Hotkey Support**: Planned for quick switching and actions (not yet implemented).
- **Cross-Platform Potential**: Windows-focused with a modular design for future macOS/Linux compatibility.

## Prerequisites

- Python 3.8 or higher
- Required Python packages:
  - `PyQt5`: For the graphical user interface
  - `pyperclip`: For clipboard access
  - `pyautogui`: For input simulation
  - `cryptography`: For AES encryption
- A local network connecting all devices
- Windows OS (macOS/Linux support pending further testing)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/multi-pc-mouse-keyboard-sharing.git
   cd multi-pc-mouse-keyboard-sharing
   ```
2. Install dependencies:

   ```bash
   pip install PyQt5 pyperclip pyautogui cryptography
   ```
3. Create a `transfers` folder in the project directory for file storage:

   ```bash
   mkdir transfers
   ```

## Usage

1. **Start the Server**:
   - Run the app on the main computer: `python mouse_share_app.py`
   - Click "Start as Server" to generate a unique pairing code.
2. **Connect Clients**:
   - On client computers, run the app and enter the server’s IP address and pairing code.
   - Click "Connect to Server" to join the network.
3. **Control Devices**:
   - Move the mouse or type on the server to control all connected clients.
   - Copy content (text/images) to sync clipboards across devices.
   - Send files to the `transfers` folder on clients (drag-and-drop UI in development).
4. **System Tray**:
   - The app minimizes to the system tray for unobtrusive operation.
   - Right-click the tray icon to quit the application.

## Architecture

- **Framework**: PyQt5 for the GUI, pyautogui for input simulation, and cryptography for secure data transfer.
- **Network**: TCP sockets ensure reliable, ordered communication. AES encryption secures all data exchanges.
- **Clipboard**: Uses pyperclip for cross-platform clipboard access, with QTimer polling for real-time sync.
- **File Transfer**: Basic file streaming to a `transfers` folder; future enhancements will support chunked transfers.
- **Modularity**: Code is structured for extensibility, with separate concerns for UI, network, and input handling.

## Screenshots

*(Screenshots of the GUI, setup wizard, and system tray will be added in future updates.)*

## Development Status

- **Completed**:
  - Core input sharing (mouse/keyboard).
  - Clipboard synchronization for text and images.
  - Basic file transfers to a designated folder.
  - System tray integration with basic functionality.
  - Secure communication with AES encryption.
- **In Progress/Planned**:
  - Visual layout editor for screen arrangement.
  - Drag-and-drop file transfer UI.
  - Hotkey support for quick actions.
  - Cross-platform compatibility for macOS/Linux (requires pyautogui testing).
- **Stretch Goals**:
  - Mobile device support as secondary clients.
  - Cloud relay for cross-subnet connectivity.
  - User profiles for saving configurations.

## Testing

- **Setup & Pairing**:
  - Verify server starts and generates a unique code.
  - Test client connections with valid/invalid codes.
- **Input Sharing**:
  - Confirm mouse movement and clicks propagate to clients.
  - Validate keyboard input across devices.
- **Clipboard Sync**:
  - Test text and image clipboard synchronisation in real-time.
- **File Transfer**:
  - Send a small file (&lt;10MB) and verify it appears in the client’s `transfers` folder.
- **Performance**:
  - Ensure input latency remains below 100ms.
  - Test stability with up to four connected clients.

## Known Limitations

- Windows-focused; macOS/Linux support requires additional pyautogui testing.
- File transfers are basic and best suited for small files (&lt;10MB).
- Drag-and-drop file transfer UI is not yet implemented.
- Layout configuration is a placeholder; screen arrangement is not fully functional.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add feature-name"`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.

Please ensure your code follows the project’s style and includes tests for new features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions, bug reports, or feedback, please open an issue on GitHub or contact \[your-email@example.com\].

## Acknowledgements

- Built with Python, PyQt5, pyautogui, pyperclip, and cryptography.
- Inspired by Microsoft Mouse Without Borders.

---

*Control multiple PCs with ease, securely, and efficiently!*
