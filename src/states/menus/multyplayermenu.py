import pygame

from src.button import Button
from src.inputfield import InputField
from src.inputhandler import InputHandler
from src.states.state import State
from src.config import WIDTH, HEIGHT, MENU_BGCOLOR


class MultiplayerMenu(State):
    """ Creates the multiplayer menu."""

    def __init__(self, screen, game_state_manager, game_controller):
        super().__init__(screen, game_state_manager, game_controller)
        self.ip_address = ""

        self.input_handler = InputHandler()
        self.selected_index = 0
        self.buttons = []
        self.input_field = None
        self.create_buttons()

    def run(self, dt):
        self.update(dt)
        self.draw()

    def create_buttons(self):
        """ Adds buttons to the menu."""
        self.buttons.append(Button('Spiel beitreten', 48, (WIDTH/2, HEIGHT/2 - 100), lambda: self.create_input_field()))
        self.buttons.append(Button('Server hosten', 48, (WIDTH/2, HEIGHT/2 ), lambda: self.start_online_game()))
        self.buttons.append(Button('Zurück', 48, (WIDTH/2, HEIGHT/2 + 200), lambda: self.game_state_manager.go_to_prev_state()))

    def create_input_field(self):
        self.input_field = InputField("IP Adresse", 32, (WIDTH/2, HEIGHT/2 + 120), "xxx.xxx.xxx.xxx")

    def join_online_game(self):
        self.game_controller.set_game_mode('online', self.ip_address)
        self.game_state_manager.set_state('level')

    def start_online_game(self):
        self.game_controller.set_game_mode('online')
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
        if self.input_field:
            self.input_field.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        """ Handles the Menu Input
            If the input field is initialized, always handle its events until the IP address is returned.
            Then join the game using the given IP address.
        """
        if not self.input_field:
            self.input_handler.handle_menu_input(self, event)
        else:
            self.ip_address = self.input_field.get_value()
            if self.ip_address == "":
                self.input_field.handle_event(event)
            else:
                self.join_online_game()
