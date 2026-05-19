import pygame

from src.button import Button

from src.states.state import State

from src.inputhandler import InputHandler


class EndMenu(State):
    """ Creates the end menu that appears after the game."""
    BGCOLOR = (216,161,123)
    
    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)

        self.input_handler = InputHandler()
        self.selected_index = 0
        self.buttons = []
        self.create_buttons()

    def run(self, dt):
        self.update(dt)
        self.draw()

    def create_buttons(self):
        """ Adds buttons to the menu."""
        self.buttons.append(Button('Start Menu', 48, (300, 400), lambda: self.go_to_start()))
        self.buttons.append(Button('Neustart', 48, (300,300), lambda: self.restart_game()))

    def go_to_start(self):
        """Set the game state to start"""
        self.game_state_manager.set_state('start')

    def restart_game(self):
        """Set the game state to level"""
        self.game_state_manager.set_state('level')

    def update(self, dt):
        pass

    def draw(self):
        """ Draws the menu with all buttons."""
        self.screen.fill(self.BGCOLOR)

        for i, button in enumerate(self.buttons):
            button.selected = (i == self.selected_index)

        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        """Handles the Menu Input"""
        self.input_handler.handle_menu_input(self, event)