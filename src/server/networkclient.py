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
        # Packets are forwarded immediately to minimize latency and prevent stuttering.
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.settimeout(5)
        # Localhost address
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)

        self.player_id = None

        # Incoming messages are stored in this queue.
        # The game loop reads from it without blocking.
        self._recv_queue = queue.Queue()
        self._connected = False
        self.connect()

    def _send_message(self, data):
        """Sends a message with a 4-byte length prefix."""
        payload = json.dumps(data).encode("utf-8")
        header = struct.pack(">I", len(payload))
        self.socket.sendall(header + payload)

    def _recv_exact(self, n):
        """Reads exactly n bytes – waits for additional chunks if necessary."""
        buf = b""
        while len(buf) < n:
            chunk = self.socket.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("Verbindung vom Server getrennt")
            buf += chunk
        return buf

    def _recv_message(self):
        """Reads a complete message (length + payload)."""
        raw_len = self._recv_exact(4)
        length = struct.unpack(">I", raw_len)[0]
        raw_data = self._recv_exact(length)
        return json.loads(raw_data.decode("utf-8"))

    def _recv_loop(self):
        """ Runs in a separate thread.
            Stores received messages in the queue so the game loop never has to wait for network data.
        """
        try:
            while self._connected:
                msg = self._recv_message()
                self._recv_queue.put(msg)
        except Exception as e:
            print(f"[RECV LOOP ERROR] {e}")
            self._connected = False

    def connect(self):
        try:
            self.socket.connect(self.addr)

            # First message from the server is an init message containing the player_id
            init = self._recv_message()
            if init and init.get("type") == "init":
                self.player_id = init["player_id"]
                print(f"[CONNECTED] Spieler-ID: {self.player_id}")

            self.socket.settimeout(None)  # Set the timeout to none after connecting
            self._connected = True
            # Start background thread (daemon=True -> automatically terminates when the main program ends)
            t = threading.Thread(target=self._recv_loop, daemon=True)
            t.start()

        except Exception as e:
            print(f"[CONNECT ERROR] {e}")

    def send(self, data):
        """Sends a message to the server."""
        try:
            self._send_message(data)
        except Exception as e:
            print(f"[SEND ERROR] {e}")

    def get_update(self):
        """Returns the latest message from the queue, or None if no new message is available."""
        latest = None
        try:
            while True:
                latest = self._recv_queue.get_nowait()
        except queue.Empty:
            pass
        return latest