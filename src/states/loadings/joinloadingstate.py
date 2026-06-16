import math
import threading
import pygame

from src.states.state import State
from src.server.networkclient import NetworkClient
from src.config import WIDTH, HEIGHT


class JoinLoadingState(State):
    """ Shown while trying to connect to a multiplayer server.
    Runs the TCP handshake in a background thread so the screen stays animated. """

    # How long to show the error message before going back (in seconds)
    ERROR_DISPLAY_TIME = 3.0

    def __init__(self, screen, game_state_manager, game_controller, ip_address):
        """ Initialize the Loading screen.
            Because it's a State, the run method is always running in the background from the game controller"""

        super().__init__(screen, game_state_manager, game_controller)

        self.ip_address = ip_address

        # connection states
        self.status = "connecting"   # "connecting" | "success" | "failed"
        self.lock = threading.Lock()

        self.elapsed = 0.0
        self.error_timer = 0.0

        # Start connecting in background
        threading.Thread(target=self.connect, daemon=True).start()


    def connect(self):
        """ Try to connect to the Server.
            If successfully, the status is changed and the update function works with it."""

        try:
            client = NetworkClient(self.ip_address)
            if client.player_id is not None:
                # hand the ready client over to the game controller
                self.game_controller.network_client = client
                with self.lock:
                    self.status = "success"
            else:
                print("Test failed")
                with self.lock:
                    self.status = "failed"
        except Exception as e:
            with self.lock:
                self.status = "failed"
            print(f"Fehler beim Verbinden: {e}")


    def update(self, dt):
        """ Updates the screen every frame"""

        self.elapsed += dt

        if self.status == "success":
            # now wait for other client
            self.game_controller.go_to_waiting_state()
            return

        # Automatically returns to the multiplayer menu after 3 seconds.
        if self.status == "failed":
            self.error_timer += dt
            if self.error_timer >= self.ERROR_DISPLAY_TIME:
                self.game_state_manager.set_state("multiplayer_menu")


    def draw(self):
        """ Draw the Spinner and text."""

        font_title = pygame.font.SysFont("Courier New", 36, bold=True)
        font_sub = pygame.font.SysFont("Courier New", 22)
        font_ip = pygame.font.SysFont("Courier New", 22)

        self.screen.blit(self.image,(0,0))

        cx = WIDTH / 2
        cy = HEIGHT / 2

        if self.status == "connecting":
            self.draw_spinner(cx, cy - 60, (0, 200, 255))

            title = font_title.render("VERBINDE …", True, (0,0,0))
            self.screen.blit(title, title.get_rect(center=(cx, cy - 220)))

            ip_surf = font_ip.render(f"Server: {self.ip_address}", True, (0,0,0))
            self.screen.blit(ip_surf, ip_surf.get_rect(center=(cx, cy - 140)))

        elif self.status == "failed":
            err = font_title.render("VERBINDUNG FEHLGESCHLAGEN", True, (255, 20, 20))
            self.screen.blit(err, err.get_rect(center=(cx, cy - 100)))

            hint = font_sub.render("Zurück zum Menü …", True, (0,0,0))
            self.screen.blit(hint, hint.get_rect(center=(cx, cy - 30)))

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
            dot_x  = cx + int(radius * math.cos(angle))
            dot_y  = cy + int(radius * math.sin(angle))
            size   = max(2, int(5 * (i / n_dots)))
            c      = tuple(int(c * alpha / 255) for c in color)
            pygame.draw.circle(self.screen, c, (dot_x, dot_y), size)


    def handle_event(self, event):
        """ You can close the screen with esc"""

        # Allow ESC to cancel
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_state_manager.set_state("multiplayer_menu")