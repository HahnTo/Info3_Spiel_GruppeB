import math
import threading
import pygame

from src.button import Button
from src.inputhandler import InputHandler
from src.states.state import State
from src.config import WIDTH, HEIGHT, MENU_BGCOLOR, get_local_ip


class WaitingState(State):
    """ Shown while waiting for the second client."""

    # How long to show the error message before going back (in seconds)
    ERROR_DISPLAY_TIME = 3.0

    def __init__(self, screen, game_state_manager, game_controller):
        """ Initialise the waiting screen. """
        super().__init__(screen, game_state_manager, game_controller)

        self.waiting_for_connection = True
        self.waiting_for_start = False
        self.lock = threading.Lock()

        self.elapsed = 0.0
        self.error_timer = 0.0

        self.input_handler = InputHandler()
        self.selected_index = 0
        self.buttons = []
        self.create_buttons()

        self.is_host = self.game_controller.network_client.player_id == 1

    def create_buttons(self):
        """ Adds buttons to the menu."""
        self.buttons.append(Button('Level 1', 48, (WIDTH/2, HEIGHT/2 - 50), lambda: self.game_controller.start_online(4)))

    def update(self, dt):
        """ Updates the screen every Frame and waits for a message from the server. """
        self.elapsed += dt

        msg = self.game_controller.network_client.get_update()

        if msg:
            if msg.get("type") == "connected":
                self.waiting_for_connection = False
                self.waiting_for_start = True
            elif msg.get("type") == "game_start":
                if not self.is_host:  # only the joiner should start this
                    self.game_controller.start_online(4)
                    return

    def draw(self):
        """ Draw the Spinner and text.
            It is variable to show text for the host or the joiner. """
        font_title = pygame.font.SysFont("Courier New", 36, bold=True)
        font_ip = pygame.font.SysFont("Courier New", 22, bold=True)

        self.screen.blit(self.image,(0,0))

        cx, cy = WIDTH / 2, HEIGHT / 2

        if self.waiting_for_connection:
            self.draw_spinner(cx, cy - 60, (0, 200, 255))

            title = font_title.render("Warte auf zweiten Spieler …", True, (0,0,0))
            self.screen.blit(title, title.get_rect(center=(cx, cy - 220)))

            # Print the ip if the joiner needs it.
            ip = get_local_ip()
            ip_surf = font_ip.render(f"Deine IP: {ip}", True, (0,0,0))
            self.screen.blit(ip_surf, ip_surf.get_rect(center=(cx, cy - 140)))
        elif self.waiting_for_start:
            title1 = font_title.render("Zwei Spieler sind verbunden", True, (0,0,0))
            self.screen.blit(title1, title1.get_rect(center=(cx, cy - 140)))

            if self.is_host:
                # Only the Host can start the Game
                title2 = font_title.render("Starte jetzt das Spiel", True, (0,0,0))
                self.screen.blit(title2, title2.get_rect(center=(cx, cy - 200)))
                for i, button in enumerate(self.buttons):
                    button.selected = (i == self.selected_index)
                for button in self.buttons:
                    button.draw(self.screen)
            else:
                # Joiner waits
                title2 = font_title.render("Warte auf Host …", True, (0,0,0))
                self.screen.blit(title2, title2.get_rect(center=(cx, cy- 200)))


        pygame.display.flip()

    def draw_spinner(self, cx, cy, color):
        """Draws an arc-based spinner that rotates over time."""
        t      = self.elapsed
        radius = 38
        n_dots = 10

        for i in range(n_dots):
            angle  = (t * 3 + i * (2 * math.pi / n_dots)) % (2 * math.pi)
            # fade: dots at the 'tail' are dimmer
            alpha  = int(40 + 215 * (i / n_dots))
            dot_r  = int(radius * math.cos(angle))
            dot_x  = cx + int(radius * math.cos(angle))
            dot_y  = cy + int(radius * math.sin(angle))
            size   = max(2, int(5 * (i / n_dots)))
            c      = tuple(int(c * alpha / 255) for c in color)
            pygame.draw.circle(self.screen, c, (dot_x, dot_y), size)

    def handle_event(self, event):
        """ Handles the menu input."""
        if self.is_host:
            self.input_handler.handle_menu_input(self, event)