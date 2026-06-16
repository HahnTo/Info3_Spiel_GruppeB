
class GameStateManager:
    """sets the different gamestates"""

    def __init__(self, current_state):
        """initializes the gamestatemanager and sets the current state"""

        self.current_state = current_state
        # prev_state is used to check whether a new level is loading; if so, the players have to be respawned
        self.prev_state = None
        # first_enter is used to check whether this is the first entry into a new state.
        self.first_entry = True


    def get_state(self):
        """returns the current state"""

        return self.current_state


    def set_state(self, state):
        """ Sets a new state and stores the previous state.
            Do not store the join_loading state, because it should only be active while connecting to a server. """

        if self.current_state != 'join_loading':
            self.prev_state = self.current_state

        self.current_state = state
        self.first_entry = True


    def is_first_entry(self):
        """returns if a state was entered for the first time"""

        return self.first_entry


    def set_first_entry(self, is_first):
        """sets the first entry"""

        self.first_entry = is_first