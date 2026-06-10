import pygame

from src.button import Button
from src.inputhandler import InputHandler
from src.states.state import State
from src.config import WIDTH, HEIGHT, MENU_BGCOLOR

class LevelChooser(State):
    """ Creates the end menu that appears after the game."""

    def __init__(self, screen, game_state_manager, game_controller):
        super().__init__(screen, game_state_manager, game_controller)

        self.input_handler = InputHandler()
        self.selected_index = 0
        self.buttons = []
        self.create_buttons()

    def run(self, dt):
        self.update(dt)
        self.draw()

    def create_buttons(self):
        """ Adds buttons to the menu."""
        # self.buttons.append(Button('Lokales Spiel', 48, (WIDTH/2, HEIGHT/2 - 100), lambda: self.game_controller.start_local()))
        self.buttons.append(Button('Level 1', 48, (WIDTH/2, HEIGHT/2 - 100), lambda: self.game_controller.start_local(1)))
        self.buttons.append(Button('Level 2', 48, (WIDTH/2, HEIGHT/2), lambda: self.game_controller.start_local(2)))
        self.buttons.append(Button('Level 3', 48, (WIDTH/2, HEIGHT/2 + 100), lambda: self.game_controller.start_local(3)))

    def start_local_game(self):
        self.game_controller.set_game_mode('local')
        self.game_state_manager.set_state('level')

    def update(self, dt):
        pass

    def draw(self):
        """ Draws the menu with all buttons."""
        self.screen.fill(MENU_BGCOLOR)

        for i, button in enumerate(self.buttons):
            button.selected = (i == self.selected_index)

        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        """Handles the Menu Input"""
        self.input_handler.handle_menu_input(self, event)