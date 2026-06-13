import json
import struct
import threading
import socket
from unittest.mock import patch, MagicMock

import pytest

from src.server.server import Server


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
    """Sends a length-prefixed JSON message on *sock*."""
    payload = json.dumps(data).encode("utf-8")
    sock.sendall(struct.pack(">I", len(payload)) + payload)


class TestServer:
    @pytest.fixture
    def server(self):
        """Creates a Server without actually calling start()."""
        with patch("socket.socket") as mock_socket_cls:
            mock_sock = MagicMock()
            mock_socket_cls.return_value = mock_sock
            server = Server(host="127.0.0.1", port=0)
            server.server = mock_sock
        return server

    def test_initial_clients_are_none(self, server):
        assert server.clients == [None, None]

    def test_initial_players_have_default_data(self, server):
        assert len(server.players) == 2
        for p in server.players:
            assert "x" in p
            assert "y" in p

    def test_get_free_player_slot_first_slot(self, server):
        slot = server.get_free_player_slot()
        assert slot == 0
        assert server.clients[0] == "reserved"
        slot = server.get_free_player_slot()
        assert slot == 1
        slot = server.get_free_player_slot()
        assert slot is None

    def test_send(self, server):
        client_sock = MagicMock()
        data = {"type": "test", "value": 42}
        server.send(client_sock, data)

        call_args = client_sock.sendall.call_args[0][0]
        length = struct.unpack(">I", call_args[:4])[0]
        payload = json.loads(call_args[4:].decode("utf-8"))

        assert payload == data
        assert length == len(json.dumps(data).encode("utf-8"))

    def test_recv_exact(self):
        """recv_exact via a real socket pair."""
        client_sock, server_sock = make_socket_pair()
        try:
            server = Server()
            server.lock = threading.Lock()

            message = b"Hello World!"
            client_sock.sendall(message)
            result = server.recv_exact(server_sock, len(message))
            assert result == message
        finally:
            client_sock.close()
            server_sock.close()

    def test_receive(self):
        """receive() correctly decodes a framed JSON message."""
        client_sock, server_sock = make_socket_pair()
        try:
            server = Server()
            server.lock = threading.Lock()

            data = {"type": "update", "data": {"x": 10}}
            send_framed(client_sock, data)
            result = server.receive(server_sock)
            assert result == data
        finally:
            client_sock.close()
            server_sock.close()

    def test_broadcast(self, server):
        mock_c1 = MagicMock()
        mock_c2 = MagicMock()
        server.clients = [mock_c1, mock_c2]
        server.broadcast_connected()
        # Both clients should have received a "connected" message
        for mock_c in [mock_c1, mock_c2]:
            call_args = mock_c.sendall.call_args[0][0]
            payload = json.loads(call_args[4:].decode("utf-8"))
            assert payload["type"] == "connected"

    def test_shutdown(self, server):
        mock_c1 = MagicMock()
        mock_c2 = MagicMock()
        server.clients = [mock_c1, mock_c2]
        server.shutdown()
        server.server.close.assert_called_once()
        mock_c1.close.assert_called_once()
        mock_c2.close.assert_called_once()
        assert server.clients == [None, None]