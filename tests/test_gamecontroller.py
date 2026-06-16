from unittest.mock import patch, MagicMock

import pygame
import pytest

from src.gamecontroller import GameController


class TestGameController:
    @pytest.fixture
    def game_controller(self):
        """ Creates a GameController with pygame already initialized."""
        pygame.init()
        controller = GameController()
        yield controller
        pygame.quit()

    def test_initial_state(self, game_controller):
        assert game_controller.game_state_manager.get_state() == "start_menu"

    def test_start_pause(self, game_controller):
        game_controller.start_pause_after_death()
        assert game_controller.is_paused is True
        game_controller.start_pause_after_death()
        game_controller.pause_timer = 0.5
        game_controller.start_pause_after_death()
        # Timer should not have been reset
        assert game_controller.pause_timer == 0.5

    def test_start_local(self, game_controller):
        with patch.object(game_controller, "level", create=True), \
             patch("src.gamecontroller.Level") as mock_level_cls:
            mock_level = MagicMock()
            mock_level_cls.return_value = mock_level
            game_controller.start_local(1)
        assert game_controller.game_mode == "local"
        assert game_controller.game_state_manager.get_state() == "level"

    def test_trigger_goal(self, game_controller):
        with patch("src.gamecontroller.Level") as mock_level_cls:
            mock_level = MagicMock()
            mock_level.level_id = 1
            mock_level_cls.return_value = mock_level
            game_controller.start_local(1)

        game_controller.trigger_goal()
        assert game_controller.game_state_manager.get_state() == "end_menu"

    def test_trigger_death(self, game_controller):
        game_controller.trigger_death()
        assert game_controller.is_paused is True

    def test_disconnect(self, game_controller):
        mock_nc = MagicMock()
        game_controller.network_client = mock_nc
        mock_srv = MagicMock()
        game_controller.server = mock_srv

        game_controller.game_mode = "online"
        game_controller.game_state_manager.set_state("level")
        game_controller.disconnect()
        assert game_controller.game_mode == "local"
        assert game_controller.game_state_manager.get_state() == "start_menu"

        mock_nc.socket.close.assert_called_once()
        assert game_controller.network_client is None
        mock_srv.shutdown.assert_called_once()
        assert game_controller.server is None

    def test_clear_network_queue(self, game_controller):
        mock_nc = MagicMock()
        messages = [{"type": "state"}, {"type": "game_over"}, None]
        mock_nc.get_update.side_effect = messages
        game_controller.network_client = mock_nc
        game_controller.clear_network_queue()
        # Should have called get_update until None was returned
        assert mock_nc.get_update.call_count == 3