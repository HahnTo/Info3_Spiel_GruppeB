

class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state
        # prev_state is used to check whether a new level is loading; if so, the players have to be respawned
        self.prev_state = None
        # first_enter is used to check whether this is the first entry into a new state.
        self.first_entry = True

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.prev_state = self.current_state
        self.current_state = state
        self.first_entry = True

    def get_prev_state(self):
        return self.prev_state

    def is_first_entry(self):
        return self.first_entry

    def set_first_entry(self, is_first):
        self.first_entry = is_first

    def go_to_prev_state(self):
        self.set_state(self.get_prev_state())