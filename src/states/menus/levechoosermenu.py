import pygame

from src.button import Button
from src.inputhandler import InputHandler
from src.states.state import State
from src.config import WIDTH, HEIGHT, MENU_BGCOLOR

class LevelChooserMenu(State):
    """ Creates the Level Chooser Menu that appears for Level selection."""

    def __init__(self, screen, game_state_manager, game_controller):
        """ Initialises the Menu"""
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
        self.buttons.append(Button('Level 1', 48, (WIDTH/2, HEIGHT/2 - 150), lambda: self.game_controller.start_local(1)))
        self.buttons.append(Button('Level 2', 48, (WIDTH/2, HEIGHT/2 - 50), lambda: self.game_controller.start_local(2)))
        self.buttons.append(Button('Level 3', 48, (WIDTH/2, HEIGHT/2 + 50), lambda: self.game_controller.start_local(3)))
        self.buttons.append(Button('Zurück', 40, (WIDTH/2, HEIGHT/2 + 200), lambda: self.game_state_manager.set_state('start_menu')))

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