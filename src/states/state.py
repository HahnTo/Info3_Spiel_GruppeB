import pygame

from config import GRAPHICS_DIR


class State:
    """ The abstract class for all states. Implements the abstract methods"""

    def __init__(self, screen, game_state_manager, game_controller):
        self.screen = screen
        self.game_state_manager = game_state_manager
        self.game_controller = game_controller
        self.image = pygame.image.load(GRAPHICS_DIR / "map" / "title_screen.png")

    def run(self, dt):
        self.update(dt)
        self.draw()

    def update(self, dt):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass