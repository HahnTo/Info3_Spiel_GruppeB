

class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state
        # prev_state is used to check whether a new level is loading; if so, the players have to be respawned
        self.prev_state = None

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.prev_state = self.current_state
        self.current_state = state

