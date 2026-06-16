import pygame

from src.button import Button
from src.inputhandler import InputHandler
from src.config import WIDTH, HEIGHT


class PauseMenu:
    """ Overlay that is drawn on top of a frozen Level when Esc is pressed. """

    def __init__(self, screen, level, game_state_manager, game_controller):
        """ Initializes the pause menu overlay for a specific level instance. """

        self.screen = screen
        self.level = level
        self.game_state_manager = game_state_manager
        self.game_controller = game_controller

        self.input_handler = InputHandler()
        self.selected_index = 0
        self.buttons = []
        self.create_buttons()


    def create_buttons(self):
        """ Adds buttons to the menu. """

        self.buttons.append(Button(
            'Weiter', 48, (WIDTH / 2, HEIGHT / 2 - 60),
            lambda: self.level.resume()
        ))
        self.buttons.append(Button(
            'Neustart', 48, (WIDTH / 2, HEIGHT / 2 + 40),
            lambda: self.restart()
        ))
        self.buttons.append(Button(
            'Zum Hauptmenu', 40, (WIDTH / 2, HEIGHT / 2 + 140),
            lambda: self.game_state_manager.set_state('start_menu')
        ))


    def restart(self):
        """ Resumes the level and restart it. """

        self.level.resume()
        self.game_controller.restart_game()


    def draw(self):
        """ Draws a transparent overlay with the pause buttons on top of the frozen level. """

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # schwarz, 150/255 Transparenz
        self.screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont("Arial", 60, bold=True)
        title_text = title_font.render("Pause", True, (255, 255, 255))
        self.screen.blit(title_text, title_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 160)))

        for i, button in enumerate(self.buttons):
            button.selected = (i == self.selected_index)

        for button in self.buttons:
            button.draw(self.screen)


    def handle_event(self, event):
        """ Handles the menu input. Escape closes the pause menu again. """

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.level.resume()
            return

        self.input_handler.handle_menu_input(self, event)