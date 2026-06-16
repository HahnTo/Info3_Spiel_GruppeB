from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.config import GRAPHICS_DIR
from src.states.level import Level


class TestLevel:


    @pytest.fixture
    def mock_gc(self):
        gc = MagicMock()
        gc.is_paused = False
        return gc

    @pytest.fixture
    def mock_gsm(self):
        return MagicMock()

    @pytest.fixture
    def screen(self):
        pygame.init()
        return pygame.display.set_mode((1080, 720))

    @pytest.fixture
    def level_local(self, screen, mock_gsm, mock_gc):
        """Creates a local Level with all heavy dependencies patched out."""
        with patch("src.states.level.LevelLoader") as mock_loader_cls:
            mock_loader = MagicMock()
            mock_loader_cls.return_value = mock_loader
            lv = Level(screen, mock_gsm, mock_gc, level_id=1, network_client=None)
        return lv

    @pytest.fixture
    def level_online(self, screen, mock_gsm, mock_gc):
        """Creates an online Level with a mocked NetworkClient."""
        mock_nc = MagicMock()
        mock_nc.player_id = 1
        with patch("src.states.level.LevelLoader") as mock_loader_cls:
            mock_loader = MagicMock()
            mock_loader_cls.return_value = mock_loader
            lv = Level(screen, mock_gsm, mock_gc, level_id=1, network_client=mock_nc)
        return lv

    def test_local_online(self, level_local, level_online):
        assert level_local.is_online is False
        assert level_online.is_online is True

    def test_local_ids(self, level_local):
        assert level_local.local_id is None
        assert level_local.remote_id is None

    def test_online_local_id_matches_network_client(self, level_online):
        assert level_online.local_id == 1

    def test_players(self, level_local):
        ids = {p.player_id for p in level_local.players.sprites()}
        assert ids == {1, 2}
        assert len(level_local.players.sprites()) == 2

    def test_get_player(self, level_local):
        player = level_local.get_player(1)
        assert player is not None
        assert player.player_id == 1
        assert level_local.get_player(99) is None

    def test_reset(self, level_local):
        for player in level_local.players.sprites():
            player.respawn = MagicMock()

        # MagicMock is not a pygame Sprite, so sprites() won't return it.
        # Use a real Obstacle and mock only its reset method.
        try:
            image = pygame.image.load(GRAPHICS_DIR / "map" / "movable.png").convert_alpha()
        except Exception as e:
            print(f"Fehler beim laden vom Bild: {e}")

        from src.obstacle import Obstacle
        obs = Obstacle(width=10, height=10, x_pos=0, y_pos=0, image=image)
        obs.reset = MagicMock()
        level_local.obstacles.add(obs)

        level_local.reset()

        for player in level_local.players.sprites():
            player.respawn.assert_called_once()
        obs.reset.assert_called_once()

    def test_sync_network_sends_local_player_data(self, level_online):
        local_player = level_online.get_player(level_online.local_id)
        local_player.get_data = MagicMock(return_value={"x": 5})
        # No messages from server
        level_online.network_client.get_update.return_value = None

        level_online.sync_network()

        level_online.network_client.send.assert_called_once_with({
            "type": "update",
            "data": {"x": 5}
        })

    def test_sync_network_applies_remote_state(self, level_online):
        remote_player = level_online.get_player(level_online.remote_id)
        remote_player.set_data = MagicMock()

        state_data = {"x": 100, "y": 200}
        level_online.network_client.get_update.side_effect = [
            {"type": "state", "data": state_data},
            None,
        ]
        level_online.get_player(level_online.local_id).get_data = MagicMock(return_value={})

        level_online.sync_network()

        remote_player.set_data.assert_called_once_with(state_data)

    def test_sync_network_triggers_game_over(self, level_online):
        level_online.network_client.get_update.side_effect = [
            {"type": "game_over"},
            None,
        ]
        level_online.get_player(level_online.local_id).get_data = MagicMock(return_value={})

        level_online.sync_network()

        level_online.game_controller.trigger_goal.assert_called_once_with(send_to_server=False)