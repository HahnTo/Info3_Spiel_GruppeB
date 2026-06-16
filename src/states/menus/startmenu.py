import pygame

from src.button import Button
from src.inputhandler import InputHandler
from src.states.state import State
from src.config import WIDTH, HEIGHT

class StartMenu(State):
    """ Creates the start menu that appears after starting the application."""

    def __init__(self, screen, game_state_manager, game_controller):
        """ Initialises the Menu"""
        super().__init__(screen, game_state_manager, game_controller)

        self.input_handler = InputHandler()
        self.selected_index = 0
        self.buttons = []
        self.create_buttons()
        self.start_caption = pygame.image.load(GRAPHICS_DIR/"map"/"monster_jump.png")


    def create_buttons(self):
        """ Adds buttons to the menu."""
        self.buttons.append(Button('Lokales Spiel', 48, (WIDTH/2, HEIGHT/2 - 100), lambda: self.game_state_manager.set_state('level_chooser')))
        self.buttons.append(Button('Multiplayer', 48, (WIDTH/2, HEIGHT/2), lambda: self.game_state_manager.set_state('multiplayer_menu')))
        self.buttons.append(Button('Spiel verlassen', 48, (WIDTH/2, HEIGHT/2 + 200), lambda: self.game_controller.shutdown()))

    def draw(self):
        """ Draws the menu with all buttons."""
        self.screen.blit(self.image,(0,0))
        self.screen.blit(self.start_caption,(72,50))

        for i, button in enumerate(self.buttons):
            button.selected = (i == self.selected_index)

        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        """Handles the Menu Input"""
        self.input_handler.handle_menu_input(self, event)