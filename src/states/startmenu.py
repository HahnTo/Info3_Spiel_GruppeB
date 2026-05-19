import pygame

from src.button import Button

from src.states.state import State


# from menu import AbstractMenu
# import pygame

class StartMenu(State):
    """ Creates the end menu that appears after the game."""
    BGCOLOR = (216, 161, 123)

    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)

        self.buttons = []
        self.create_buttons()

    def run(self, dt):
        self.listen_for_buttons()
        self.update(dt)
        self.draw()

    def create_buttons(self):
        """ Adds buttons to the menu."""
        self.buttons.append(Button('Starte das Spiel', 48, (300, 300), lambda: self.start_game()))

    def start_game(self):
        self.game_state_manager.set_state('level')

    def update(self, dt):
        pass

    def draw(self):
        """ Draws the menu with all buttons."""
        self.screen.fill(self.BGCOLOR)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def listen_for_buttons(self):
        for button in self.buttons:
            button.is_pressed()