import pygame

from src.button import Button
from src.states.state import State
from src.inputhandler import InputHandler
from src.config import WIDTH, HEIGHT, MENU_BGCOLOR

class EndMenu(State):
    """ Creates the end menu that appears after the game."""

    def __init__(self, screen, game_state_manager, game_controller):
        super().__init__(screen, game_state_manager, game_controller)

        self.level_id = None
        self.input_handler = InputHandler()
        self.selected_index = 0
        self.buttons = []
        self.create_buttons()

    def set_level_id(self, level_id):
        self.level_id = level_id

    def run(self, dt):
        self.update(dt)
        self.draw()

    def create_buttons(self):
        """ Adds buttons to the menu."""
        self.buttons.append(Button('Start Menu', 48, (WIDTH/2, HEIGHT/2), lambda: self.go_to_start()))
        self.buttons.append(Button('Neustart', 48, (WIDTH/2, HEIGHT/2 + 100), lambda: self.restart_game()))

    def go_to_start(self):
        """Set the game state to start"""
        self.game_state_manager.set_state('start_menu')

    def restart_game(self):
        """Set the game state to level"""
        self.game_state_manager.set_state('level')

    def update(self, dt):
        pass

    def draw(self):
        """ Draws the menu with all buttons."""
        self.screen.fill(MENU_BGCOLOR)

        level_font = pygame.font.Font(None, 60)
        title_font = pygame.font.Font(None, 72)
        score_font = pygame.font.Font(None, 46)

        # Texte rendern
        level_text = level_font.render(
            f"Level {self.level_id}", True, (255, 255, 255)
        )
        congrats_text = title_font.render(
            "Herzlichen Glückwunsch!", True, (255, 255, 255)
        )
        score_text = score_font.render(
            f"Dein Score: 0", True, (255, 255, 255)
        )

        # Zentriert platzieren
        level_rect = level_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 300))
        congrats_rect = congrats_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 200))
        score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 130))

        self.screen.blit(level_text, level_rect)
        self.screen.blit(congrats_text, congrats_rect)
        self.screen.blit(score_text, score_rect)

        for i, button in enumerate(self.buttons):
            button.selected = (i == self.selected_index)

        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        """Handles the Menu Input"""
        self.input_handler.handle_menu_input(self, event)