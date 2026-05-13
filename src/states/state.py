

class State:
    def __init__(self, screen, game_state_manager):
        self.screen = screen
        self.game_state_manager = game_state_manager

    def run(self, dt):
        self.update(dt)
        self.draw()

    def update(self, dt):
        pass

    def draw(self):
        pass