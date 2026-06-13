import pytest

from src.gamestatemanager import GameStateManager


class TestGameStateManager:
    @pytest.fixture
    def gsm(self):
        return GameStateManager("start_menu")

    def test_initial_state(self, gsm):
        assert gsm.get_state() == "start_menu"
        assert gsm.prev_state is None
        assert gsm.is_first_entry() is True

    def test_set_state(self, gsm):
        gsm.set_state("level")
        assert gsm.get_state() == "level"
        assert gsm.prev_state == "start_menu"

    def test_set_state_resets_first_entry(self, gsm):
        gsm.set_first_entry(False)
        gsm.set_state("end_menu")
        assert gsm.is_first_entry() is True

    def test_prev_state(self, gsm):
        # join_loading should not overwrite prev_state
        gsm.set_state("level")
        gsm.set_state("join_loading")
        gsm.set_state("waiting_for_client")
        # prev_state must still be level, not join_loading or waiting_for_client
        assert gsm.prev_state == "level"