import math
import threading
import pygame

from src.button import Button
from src.inputhandler import InputHandler
from src.states.state import State
from src.server.networkclient import NetworkClient
from src.config import WIDTH, HEIGHT, MENU_BGCOLOR


class WaitForClientState(State):
    """
    Shown while waiting for the second client.
    """

    # How long to show the error message before going back (in seconds)
    ERROR_DISPLAY_TIME = 3.0

    def __init__(self, screen, game_state_manager, game_controller):
        super().__init__(screen, game_state_manager, game_controller)

        # --- connection state ---
        self.waiting_for_connection = True
        self.waiting_for_start = False
        self.lock = threading.Lock()

        # --- animation ---
        self.elapsed = 0.0
        self.error_timer = 0.0

        # --- fonts ---
        self.font_title  = pygame.font.SysFont("Courier New", 36, bold=True)
        self.font_sub    = pygame.font.SysFont("Courier New", 22)
        self.font_ip     = pygame.font.SysFont("Courier New", 18)

        self.input_handler = InputHandler()
        self.selected_index = 0
        self.buttons = []
        self.create_buttons()

        self.is_host = self.game_controller.network_client.player_id == 1

        # waiting in background
        # threading.Thread(target=self.listen, daemon=True).start()

    def run(self, dt):
        self.update(dt)
        self.draw()

    def create_buttons(self):
        """ Adds buttons to the menu."""
        # self.buttons.append(Button('Lokales Spiel', 48, (WIDTH/2, HEIGHT/2 - 100), lambda: self.game_controller.start_local()))
        self.buttons.append(Button('Level 1', 48, (WIDTH/2, HEIGHT/2 - 100), lambda: self.game_controller.start_online(4)))

    def update(self, dt):
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
        ACCENT  = (0, 200, 255)
        DIM     = (80, 80, 100)
        WHITE   = (230, 230, 240)
        RED     = (255, 80, 80)

        self.screen.fill(MENU_BGCOLOR)

        cx, cy = WIDTH // 2, HEIGHT // 2

        if self.waiting_for_connection:
            self._draw_spinner(cx, cy - 60, ACCENT)

            title = self.font_title.render("Warte auf zweiten Spieler …", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(cx, cy + 30)))
        elif self.waiting_for_start:
            title1 = self.font_title.render("Zwei Spieler sind verbunden", True, WHITE)
            self.screen.blit(title1, title1.get_rect(center=(cx, cy + 30)))

            if self.is_host:
                # Only the Host can start the Game
                title2 = self.font_title.render("Startet jetzt das Spiel", True, WHITE)
                self.screen.blit(title2, title2.get_rect(center=(cx, cy)))
                for i, button in enumerate(self.buttons):
                    button.selected = (i == self.selected_index)
                for button in self.buttons:
                    button.draw(self.screen)
            else:
                # Joiner waits
                title2 = self.font_title.render("Warte auf Host …", True, WHITE)
                self.screen.blit(title2, title2.get_rect(center=(cx, cy)))

        pygame.display.flip()

    def _draw_spinner(self, cx, cy, color):
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
        if self.is_host:
            self.input_handler.handle_menu_input(self, event)