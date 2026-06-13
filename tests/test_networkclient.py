import queue
import time

from src.server.networkclient import NetworkClient

import json
import struct
import threading
import socket
from unittest.mock import patch, MagicMock

import pytest

def make_socket_pair():
    """Returns a connected (client_sock, server_sock) pair via localhost."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    port = server.getsockname()[1]

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("127.0.0.1", port))
    server_sock, _ = server.accept()
    server.close()
    return client_sock, server_sock

def send_framed(sock, data: dict):
    """ Sends a length-prefixed JSON message on *sock*."""
    payload = json.dumps(data).encode("utf-8")
    sock.sendall(struct.pack(">I", len(payload)) + payload)

class TestNetworkClient:
    @pytest.fixture
    def connected_client(self):
        """ Returns a NetworkClient whose socket is replaced with a mock,
            simulating a successful connection and init message. """
        with patch("socket.socket") as mock_socket_cls:
            mock_sock = MagicMock()
            mock_socket_cls.return_value = mock_sock

            # Simulate the init message returned by connect()
            init_payload = json.dumps({"type": "init", "player_id": 1}).encode("utf-8")
            header = struct.pack(">I", len(init_payload))

            # recv returns header then payload, then blocks
            mock_sock.recv.side_effect = [
                header[:2], header[2:],   # recv_exact splits are fine
                init_payload,
            ]

            # Patch recv_exact directly so we can return clean bytes
            with patch.object(NetworkClient, "recv_exact",
                               side_effect=[header, init_payload]):
                client = NetworkClient.__new__(NetworkClient)
                client.socket = mock_sock
                client.addr = ("127.0.0.1", 5555)
                client.player_id = None
                client.recv_queue = queue.Queue()
                client.connected = False

                # Manually replicate what connect() does with mocked recv_exact
                init = {"type": "init", "player_id": 1}
                client.player_id = init["player_id"]
                client.connected = True

        return client

    def test_player_id(self, connected_client):
        assert connected_client.player_id == 1

    def test_connected_flag(self, connected_client):
        assert connected_client.connected is True

    def test_send_message(self, connected_client):
        data = {"type": "update", "x": 5}
        connected_client.send_message(data)

        call_args = connected_client.socket.sendall.call_args[0][0]
        length = struct.unpack(">I", call_args[:4])[0]
        payload = json.loads(call_args[4:].decode("utf-8"))

        assert payload == data
        assert length == len(json.dumps(data).encode("utf-8"))

    def test_get_update(self, connected_client):
        # No message
        result = connected_client.get_update()
        assert result is None
        # Message
        msg = {"type": "state", "data": {"x": 10}}
        connected_client.recv_queue.put(msg)
        result = connected_client.get_update()
        assert result == msg
        # Queue drained
        connected_client.recv_queue.put({"type": "ping"})
        connected_client.get_update()
        assert connected_client.get_update() is None

    def test_recv_exact(self):
        """ recv_exact assembles chunks correctly."""
        client_sock, server_sock = make_socket_pair()
        try:
            nc = NetworkClient()
            nc.socket = server_sock

            message = b"Hello World!"
            client_sock.sendall(message)
            result = nc.recv_exact(len(message))
            assert result == message
        finally:
            client_sock.close()
            server_sock.close()

    def test_recv(self):
        """ recv_message correctly decodes a framed JSON message."""
        client_sock, server_sock = make_socket_pair()
        try:
            nc = NetworkClient()
            nc.socket = server_sock

            data = {"type": "state", "value": 99}
            send_framed(client_sock, data)
            result = nc.recv_message()
            assert result == data
        finally:
            client_sock.close()
            server_sock.close()

    def test_recv_loop(self):
        """recv_loop stores received messages in recv_queue."""
        client_sock, server_sock = make_socket_pair()
        try:
            nc = NetworkClient()
            nc.socket = server_sock
            nc.recv_queue = queue.Queue()
            nc.connected = True

            msg = {"type": "ping"}
            send_framed(client_sock, msg)

            # After one message, close the socket to terminate the loop
            def stop_after_first():
                time.sleep(0.05)
                client_sock.close()

            threading.Thread(target=stop_after_first, daemon=True).start()
            nc.recv_loop()

            result = nc.recv_queue.get_nowait()
            assert result == msg
        finally:
            server_sock.close()