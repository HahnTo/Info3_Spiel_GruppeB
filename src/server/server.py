# ISBN: 978-3-8362-7926-0 - Python 3
# Kapitel 32: Netzwerkkommunikation

# https://youtu.be/3QiPPX-KeSc

import socket
import threading
import json
import struct


class Server:
    """ Server implements a simple TCP-based multiplayer backend.
        It uses a JSON protocol to transfer player data and game states between two clients.
        Each client runs in its own thread to handle communication in the background.
    """
    def __init__(self, host="192.168.0.237", port=5555):
        """Initializes the server with its IP address and port and starts it."""
        self.host = host
        self.port = port
        # Create a TCP/IPv4 socket for the server to accept client connections
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Packets are forwarded immediately to minimize latency and prevent stuttering.
        self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.server.bind((self.host, self.port))
        # Allows up to 2 clients to connect.
        self.server.listen(2)

        print(f"Server gestartet auf {self.host}:{self.port}")

        self.game_started = False

        self.clients = [None, None]
        self.lock = threading.Lock()
        # Initialize only the player data, not a Player() object
        self.players = [
            {"x": 20,  "y": 700, "vx": 0, "vy": 0, "facing_right": True, "on_ground": False},
            {"x": 60,  "y": 700, "vx": 0, "vy": 0, "facing_right": True, "on_ground": False},
        ]

    # TCP transmits data as a continuous stream without preserving message boundaries.
    # The length prefix defines the size of each message so the data can be correctly separated into individual packets.
    def send(self, client, data):
        """Sends a message with a 4-byte length prefix."""
        try:
            payload = json.dumps(data).encode("utf-8")
            # struct.pack returns 4 bytes in big-endian(>I) format.
            header = struct.pack(">I", len(payload))
            client.sendall(header + payload)
        except Exception as e:
            print(f"[SEND ERROR] {e}")

    def receive(self, client):
        """Receives a message with a 4-byte length prefix."""
        try:
            # read length
            raw_len = self._recv_exact(client, 4)
            if raw_len is None:
                return None
            length = struct.unpack(">I", raw_len)[0]

            # 2) read payload
            raw_data = self._recv_exact(client, length)
            if raw_data is None:
                return None

            return json.loads(raw_data.decode("utf-8"))

        except Exception as e:
            print(f"[RECEIVE ERROR] {e}")
            return None

    def _recv_exact(self, client, n):
        """Reads exactly n bytes from the socket – waits for additional chunks if necessary."""
        buf = b""
        while len(buf) < n:
            chunk = client.recv(n - len(buf))
            if not chunk:
                # Connection has been closed.
                return None
            buf += chunk
        return buf

    def get_free_player_slot(self):
        """Returns the next free slot and reserves it."""
        with self.lock:
            for i in range(2):
                if self.clients[i] is None:
                    self.clients[i] = "reserved"
                    return i
        return None

    def start(self):
        """Starts the server and creates a new thread when a new connection comes in."""
        while True:
            # Waits until a new connection is available.
            client, addr = self.server.accept()
            print("Verbunden:", addr)

            player_id = self.get_free_player_slot()

            if player_id is None:
                print("Server voll – Verbindung abgelehnt.")
                client.close()
                continue

            # Use a lock to ensure that two threads do not execute this code block at the same time.
            with self.lock:
                self.clients[player_id] = client

            if self.clients[0] and self.clients[1]:
                self.game_started = True
                self.broadcast_start()

            thread = threading.Thread(
                target=self.handle_client,
                args=(client, player_id),
                daemon=True,
            )
            thread.start()

    def broadcast_start(self):
        """Send game_start to all connected clients. Then they show the level"""
        data = {
            "type": "game_start",
            "level_id": 4
        }

        for c in self.clients:
            if c and c != "reserved":
                self.send(c, data)

    def handle_client(self, client, player_id):
        """Runs in a separate thread for each connected client. It is called when a new thread is created."""
        try:
            self.send(client, {
                "type": "init",
                "player_id": player_id + 1   # 0 -> 1,  1 -> 2
            })

            while True:
                # Receives data every frame from the client socket.
                data = self.receive(client)

                # If None, the connection is not working.
                if data is None:
                    break

                if data.get("type") == "update":
                    # save own data
                    self.players[player_id] = data["data"]

                    other_id = 1 - player_id

                    # Send own state to the other client (direct update)
                    with self.lock:
                        other_client = self.clients[other_id]

                    if other_client and other_client != "reserved":
                        self.send(other_client, {
                            "type": "state",
                            "data": self.players[player_id]
                        })

                    # Send other client state back to the sender
                    self.send(client, {
                        "type": "state",
                        "data": self.players[other_id]
                    })

        except Exception as e:
            print(f"[CLIENT ERROR] player_id={player_id}: {e}")

        finally:
            print(f"Client getrennt: player_id={player_id}")
            with self.lock:
                self.clients[player_id] = None
            client.close()


# if __name__ == "__main__":
#     server = Server()
#     server.start()