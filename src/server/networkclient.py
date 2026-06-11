import json
import socket
import struct
import threading
import queue


class NetworkClient:
    """
    NetworkClient handles TCP communication between the game client and server.
    It uses a JSON protocol to transfer player data and game states.
    """
    def __init__(self, server="127.0.0.1", port=5555):
        """Initialize the network client and connect it to the server with given IP address."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.settimeout(5)
        self.addr = (server, port)

        self.player_id = None

        # Incoming messages are stored in this queue.
        # The game loop reads from it without blocking.
        self.recv_queue = queue.Queue()
        self.connected = False
        self.connect()

    def send_message(self, data):
        """Sends a message with a 4-byte length prefix."""
        payload = json.dumps(data).encode("utf-8")
        header = struct.pack(">I", len(payload))
        self.socket.sendall(header + payload)

    def recv_exact(self, n):
        """Reads exactly n bytes – waits for additional chunks if necessary."""
        buf = b""
        while len(buf) < n:
            chunk = self.socket.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("Verbindung vom Server getrennt")
            buf += chunk
        return buf

    def recv_message(self):
        """Reads a complete message (length + payload)."""
        raw_len = self.recv_exact(4)
        length = struct.unpack(">I", raw_len)[0]
        raw_data = self.recv_exact(length)
        return json.loads(raw_data.decode("utf-8"))

    def recv_loop(self):
        """ Runs in a separate thread.
            Stores received messages in the queue so the game loop never has to wait for network data.
        """
        try:
            while self.connected:
                msg = self.recv_message()
                self.recv_queue.put(msg)
        except Exception as e:
            print(f"[RECV LOOP ERROR] {e}")
            self.connected = False

    def connect(self):
        """ Tries to connect to the server.
            If there is a valid connection, it starts a thread.
            The Thread allways listens to the incoming messages and store them"""
        try:
            self.socket.connect(self.addr)

            # First message from the server is an init message containing the player_id
            init = self.recv_message()
            if init:
                if init.get("type") == "init":
                    self.player_id = init["player_id"]
                    print(f"[CONNECTED] Spieler-ID: {self.player_id}")
                elif init.get("type") == "server_full":
                    print("Server ist voll!")
                    return

            # Set the timeout to none after connecting, so you cn wait till the second client connects
            self.socket.settimeout(None)
            self.connected = True
            # Start background thread (daemon=True -> automatically terminates when the main program ends)
            t = threading.Thread(target=self.recv_loop, daemon=True)
            t.start()

        except Exception as e:
            print(f"[CONNECT ERROR] {e}")

    def send(self, data):
        """Sends a message to the server."""
        try:
            self.send_message(data)
        except Exception as e:
            print(f"[SEND ERROR] {e}")

    def get_update(self):
        """Returns the latest message from the Server"""
        try:
            return self.recv_queue.get_nowait()
        except queue.Empty:
            return None