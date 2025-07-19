import sys
import socket
import threading
import json
import pyperclip
import pyautogui
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt, QTimer
from cryptography.fernet import Fernet
import uuid
import time
import random
from pynput import mouse

# Configuration
HOST = '0.0.0.0'
PORT = 5555
ENCRYPTION_KEY = Fernet.generate_key()
CIPHER = Fernet(ENCRYPTION_KEY)
pyautogui.FAILSAFE = False

class MouseShareApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-PC Mouse & Keyboard Sharing")
        self.clients = {}
        self.layout_config = {"screens": []}
        self.is_server = False
        self.current_client = None
        self.setup_ui()
        self.setup_network()
        self.setup_clipboard_monitor()

    def setup_ui(self):
        # Main widget and layout
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Setup wizard
        self.code_label = QLabel("Shared Code:")
        self.code_input = QLineEdit(str(random.randint(1000, 9999)))
        self.start_server_btn = QPushButton("Start as Server")
        self.connect_btn = QPushButton("Connect to Server")
        layout.addWidget(self.code_label)
        layout.addWidget(self.code_input)
        layout.addWidget(self.start_server_btn)
        layout.addWidget(self.connect_btn)

        # Status display
        self.status_label = QLabel("Status: Not connected")
        layout.addWidget(self.status_label)

        # Layout configuration
        self.layout_btn = QPushButton("Configure Layout")
        layout.addWidget(self.layout_btn)

        # System tray
        self.tray_icon = QSystemTrayIcon(self)
        tray_menu = QMenu()
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Connect buttons
        self.start_server_btn.clicked.connect(self.start_server)
        self.connect_btn.clicked.connect(self.connect_to_server)
        self.layout_btn.clicked.connect(self.configure_layout)

        self.control_on_this_pc = True  # Track if this PC currently has control
        self.screen_width, self.screen_height = pyautogui.size()
        self.edge_threshold = 2  # Pixels from edge to trigger transfer
        self.is_transferring = False
        # Start global mouse listener if server
        if self.is_server:
            self.start_global_mouse_listener()

    def setup_network(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def setup_clipboard_monitor(self):
        self.last_clipboard = pyperclip.paste()
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.check_clipboard)
        self.clipboard_timer.start(500)

    def start_server(self):
        self.is_server = True
        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen()
            self.status_label.setText("Status: Server running")
            threading.Thread(target=self.accept_clients, daemon=True).start()
        except Exception as e:
            self.status_label.setText(f"Status: Server error - {str(e)}")

    def accept_clients(self):
        while True:
            client, addr = self.server_socket.accept()
            client_id = str(uuid.uuid4())[:8]
            self.clients[client_id] = {"socket": client, "addr": addr}
            self.status_label.setText(f"Status: Connected to {len(self.clients)} clients")
            threading.Thread(target=self.handle_client, args=(client, client_id), daemon=True).start()

    def connect_to_server(self):
        server_ip = "192.168.145.217"  # Replace with actual server IP input
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((server_ip, PORT))
            self.clients["server"] = {"socket": client_socket}
            self.status_label.setText("Status: Connected to server")
            threading.Thread(target=self.handle_server, args=(client_socket,), daemon=True).start()
        except Exception as e:
            self.status_label.setText(f"Status: Connection error - {str(e)}")

    def handle_client(self, client_socket, client_id):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                decrypted = CIPHER.decrypt(data).decode()
                self.process_message(json.loads(decrypted), client_id)
            except:
                break
        del self.clients[client_id]
        client_socket.close()
        self.status_label.setText(f"Status: Connected to {len(self.clients)} clients")

    def handle_server(self, server_socket):
        while True:
            try:
                data = server_socket.recv(1024)
                if not data:
                    break
                decrypted = CIPHER.decrypt(data).decode()
                self.process_message(json.loads(decrypted), "server")
            except:
                break
        server_socket.close()
        self.status_label.setText("Status: Disconnected from server")

    def process_message(self, message, client_id):
        if message["type"] == "input":
            self.handle_input(message["data"])
        elif message["type"] == "clipboard":
            pyperclip.copy(message["data"])
        elif message["type"] == "file":
            self.handle_file_transfer(message["data"], client_id)
        elif message["type"] == "control_transfer":
            if message["data"] == "to_server":
                self.control_on_this_pc = True
                self.status_label.setText("Status: Control returned to this PC")
            elif message["data"] == "to_client":
                self.control_on_this_pc = True
                self.status_label.setText("Status: Control transferred to this PC")
                self.start_client_global_mouse_listener()

    def handle_input(self, data):
        if data["event"] == "mouse_move":
            pyautogui.moveTo(data["x"], data["y"])
        elif data["event"] == "mouse_click":
            pyautogui.click(button=data["button"])
        elif data["event"] == "key_press":
            pyautogui.press(data["key"])

    def handle_file_transfer(self, data, client_id):
        with open(os.path.join("transfers", data["name"]), "wb") as f:
            f.write(data["content"])
        self.tray_icon.showMessage("File Transfer", f"Received {data['name']}")

    def check_clipboard(self):
        current = pyperclip.paste()
        if current != self.last_clipboard:
            self.last_clipboard = current
            self.broadcast({"type": "clipboard", "data": current})

    def broadcast(self, message):
        encrypted = CIPHER.encrypt(json.dumps(message).encode())
        for client_id, client in self.clients.items():
            try:
                client["socket"].send(encrypted)
            except:
                continue

    def configure_layout(self):
        # Placeholder for layout configuration UI
        pass

    def start_global_mouse_listener(self):
        def on_move(x, y):
            if not self.control_on_this_pc:
                return  # Ignore if this PC doesn't have control
            # Left edge detection
            if x <= self.edge_threshold and not self.is_transferring:
                self.is_transferring = True
                self.transfer_control_to_client()
            # Right edge detection (for future, if client returns control)
            elif x >= self.screen_width - self.edge_threshold:
                pass  # Placeholder for right edge logic
            else:
                self.is_transferring = False
        self.mouse_listener = mouse.Listener(on_move=on_move)
        self.mouse_listener.start()

    def start_client_global_mouse_listener(self):
        self.client_screen_width, self.client_screen_height = pyautogui.size()
        self.client_edge_threshold = 2
        self.client_is_transferring = False
        def on_move(x, y):
            if not self.control_on_this_pc:
                return
            # Right edge detection: return control to server
            if x >= self.client_screen_width - self.client_edge_threshold and not self.client_is_transferring:
                self.client_is_transferring = True
                self.transfer_control_to_server()
            elif x <= self.client_edge_threshold:
                pass  # Placeholder for left edge logic if needed
            else:
                self.client_is_transferring = False
        self.client_mouse_listener = mouse.Listener(on_move=on_move)
        self.client_mouse_listener.start()

    def transfer_control_to_client(self):
        # Hide or lock local mouse (optional, for now just send message)
        self.status_label.setText("Status: Transferring control to client...")
        # Send a message to client to take control
        self.broadcast({"type": "control_transfer", "data": "to_client"})
        self.control_on_this_pc = False
        # Optionally, move mouse to far right to simulate leaving screen
        pyautogui.moveTo(self.screen_width - 1, pyautogui.position().y)

    def transfer_control_to_server(self):
        self.status_label.setText("Status: Returning control to server...")
        # Send a message to server to take control back
        if "server" in self.clients:
            encrypted = CIPHER.encrypt(json.dumps({"type": "control_transfer", "data": "to_server"}).encode())
            try:
                self.clients["server"]["socket"].send(encrypted)
            except:
                pass
        self.control_on_this_pc = False
        # Optionally, move mouse to far left to simulate leaving screen
        pyautogui.moveTo(1, pyautogui.position().y)

    def mousePressEvent(self, event):
        if self.is_server:
            self.broadcast({
                "type": "input",
                "data": {"event": "mouse_click", "button": "left" if event.button() == Qt.LeftButton else "right"}
            })

    def mouseMoveEvent(self, event):
        if self.is_server:
            pos = event.pos()
            self.broadcast({
                "type": "input",
                "data": {"event": "mouse_move", "x": pos.x(), "y": pos.y()}
            })

    def keyPressEvent(self, event):
        if self.is_server:
            self.broadcast({
                "type": "input",
                "data": {"event": "key_press", "key": event.text()}
            })

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MouseShareApp()
    window.show()
    sys.exit(app.exec_())