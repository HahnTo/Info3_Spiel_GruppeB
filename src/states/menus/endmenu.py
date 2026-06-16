import pygame

from src.button import Button
from src.states.state import State
from src.inputhandler import InputHandler
from src.config import WIDTH, HEIGHT

class EndMenu(State):
    """ Creates the end menu that appears after the game."""

    def __init__(self, screen, game_state_manager, game_controller):
        """ Initialises the end menu screen."""
        super().__init__(screen, game_state_manager, game_controller)

        self.level_id = None
        self.input_handler = InputHandler()
        self.selected_index = 0
        self.buttons = []

        self.timer = 0.0

    def build_menu(self, level_id, timer):
        """ Creates Level id and buttons. """
        self.level_id = level_id
        self.timer = timer
        self.create_buttons()

    def create_buttons(self):
        """ Create buttons depending on the game mode."""
        self.buttons = []
        self.selected_index = 0
        is_online = self.game_controller.game_mode == 'online'

        if is_online:
            is_host = (self.game_controller.network_client and
                       self.game_controller.network_client.player_id == 1)
            if is_host:
                self.buttons.append(Button(
                    'Nochmal spielen', 48, (WIDTH / 2, HEIGHT / 2),
                    lambda: self.game_controller.restart_online()
                ))
            else:
                # The joiner only sees the text and not the restart button, they wait for the host.
                pass
            self.buttons.append(Button(
                'Server verlassen', 48, (WIDTH / 2, HEIGHT / 2 + 100),
                lambda: self.game_controller.disconnect()
            ))
        else:
            self.buttons.append(Button(
                'Neustart', 48, (WIDTH / 2, HEIGHT / 2),
                lambda: self.game_state_manager.set_state('level')
            ))
            self.buttons.append(Button(
                'Start Menu', 48, (WIDTH / 2, HEIGHT / 2 + 100),
                lambda: self.game_state_manager.set_state('start_menu')
            ))

    def update(self, dt):
        """ Waits for a message from the server. """
        if self.game_controller.game_mode == 'online' and self.game_controller.network_client:
            msg = self.game_controller.network_client.get_update()
            if msg and msg.get("type") == "restart":
                self.game_controller.restart_online(send=False)

    def draw(self):
        """ Draws the menu with all buttons."""
        self.screen.blit(self.image,(0,0))

        level_font = pygame.font.Font(None, 60)
        title_font = pygame.font.Font(None, 72)
        score_font = pygame.font.Font(None, 46)

        level_text = level_font.render(
            f"Level {self.level_id}", True, (255, 255, 255)
        )
        congrats_text = title_font.render(
            "Herzlichen Glückwunsch!", True, (255, 255, 255)
        )

        minutes = int(self.timer // 60)
        seconds = int(self.timer % 60)

        time_string = f"{minutes:02}:{seconds:02}"

        score_text = score_font.render(
            f"Eure Zeit: {time_string}", True, (255, 255, 255)
        )

        level_rect = level_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 300))
        congrats_rect = congrats_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 200))
        score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 130))

        self.screen.blit(level_text, level_rect)
        self.screen.blit(congrats_text, congrats_rect)
        self.screen.blit(score_text, score_rect)

        is_online = self.game_controller.game_mode == 'online'
        is_host = (self.game_controller.network_client and
                   self.game_controller.network_client.player_id == 1)

        if is_online and not is_host:
            hint_font = pygame.font.Font(None, 40)
            hint = hint_font.render("Warte auf Host …", True, (180, 180, 180))
            self.screen.blit(hint, hint.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

        # Draw buttons (only the host has the restart button)
        for i, button in enumerate(self.buttons):
            button.selected = (i == self.selected_index)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        """Handles the Menu Input"""
        self.input_handler.handle_menu_input(self, event)