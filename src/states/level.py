# Soll die Platformen aus einer JSON oder ähnlichem laden, wenn ein neues Level erstellt wird.
import pygame
import pytmx

from src.config import ASSETS_DIR, HEIGHT, WIDTH, GRAPHICS_DIR
from src.player import Player
from src.states.menus.pausemenu import PauseMenu
from src.states.state import State
from src.levelloader import LevelLoader


BACKGROUND_COLOR = (50, 50, 50)

try:
    background_image = pygame.image.load(GRAPHICS_DIR / "map" / "Background.png")
except Exception as e:
    print(f"Fehler beim laden vom Bild: {e}")

class Level(State):
    """ Creates the Level to play in.
        It takes the tmx file which is created with Tiled.
        To load the graphics, we have implemented the Level Loader. """




    def __init__(self, screen, game_state_manager, game_controller, level_id, network_client=None):
        """ Initialise the Level and check if it's an online game."""

        super().__init__(screen, game_state_manager, game_controller)

        self.network_client = network_client
        # If network_client is not None, the game is running in online mode.
        self.is_online = self.network_client is not None

        if self.is_online:
            self.local_id = self.network_client.player_id
            # It returns 1 or 2 when 3 is subtracted
            self.remote_id = 3 - self.local_id
        else:
            self.local_id = None
            self.remote_id = None

        self.level_id = level_id
        map_location = ASSETS_DIR / f"maps/map_{level_id}.tmx"

        self.game_controller = game_controller
        self.loader = LevelLoader(map_location, self)

        self.is_menu_paused = False
        self.pause_menu = PauseMenu(self.screen, self, self.game_state_manager, self.game_controller)

        # Initialize all sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.players = pygame.sprite.Group()

        self.load_map()
        self.create_players()
        self.timer = 0.0
        self.timer_running = True


    def load_map(self):
        """ Load the map from the Level loader"""

        self.loader.load()


    def create_players(self):
        """ Create the players with their spawnpoint and physics"""

        if self.is_online:
            # If local_id == 1, the player with ID 1 is the local player
            player1 = Player(30, HEIGHT - 20, 1, self.local_id == 1)
            player1.add(self.all_sprites, self.players)

            player2 = Player(60, HEIGHT - 20, 2, self.local_id == 2)

            player2.add(self.all_sprites, self.players)
        else:
            player1 = Player(20, HEIGHT - 20, 1, True)
            player1.add(self.all_sprites, self.players)

            player2 = Player(60, HEIGHT - 20, 2, True)
            player2.add(self.all_sprites, self.players)


    def get_player(self, player_id):
        """Returns the player with the given player_id."""

        for player in self.players.sprites():
            if player.player_id == player_id:
                return player
        return None

    def update(self, dt):

        """ Update all sprites.
            Player sprites need the game controller as an additional parameter"""
        self.obstacles.update()
        if not self.is_online:
            # Update all Players
            self.players.update(dt, self.game_controller)
        else:
            # Only update local Player
            local_player = self.get_player(self.local_id)
            remote_player = self.get_player(self.remote_id)
            if local_player:
                local_player.update(dt, self.game_controller)
            if remote_player:
                remote_player.update(dt, self.game_controller)


    def pause(self, send_to_server=True):
        """ Freezes the level (no updates, no movement input) and shows the pause overlay on top. """

        if send_to_server and self.network_client is not None:
            self.network_client.send({"type": "open_pause"})
        self.is_menu_paused = True
        self.pause_menu.selected_index = 0


    def resume(self, send_to_server=True):
        """ Closes the pause overlay and unfreezes the level again. """

        if send_to_server and self.network_client is not None:
            self.network_client.send({"type": "close_pause"})
        self.is_menu_paused = False


    def reset(self):
        """ Reset all obstacles and players to their start position. Resets the Timer"""

        self.timer = 0.0
        self.timer_running = True

        for obstacle in self.obstacles.sprites():
            obstacle.reset()

        for player in self.players.sprites():
            player.respawn()


    def sync_network(self):
        """ Sends local player state to the server and applies received remote updates"""

        if not self.is_online:
            return

        local_player = self.get_player(self.local_id)
        remote_player = self.get_player(self.remote_id)

        if local_player:
            data = {
                "type": "update",
                "data": local_player.get_data()
            }
            self.network_client.send(data)

        # check for all different message types
        while True:
            msg = self.network_client.get_update()
            if msg is None:
                break
            if msg.get("type") == "state" and remote_player:
                remote_player.set_data(msg["data"])
            elif msg.get("type") == "game_over":
                self.game_controller.trigger_goal(send_to_server=False)
                return
            elif msg.get("type") == "restart":
                self.game_controller.restart_online(send=False)
                return
            elif msg.get("type") == "died":
                self.game_controller.trigger_death(send_to_server=False)
                return
            elif msg.get("type") == "open_pause":
                self.pause(send_to_server=False)
                return
            elif msg.get("type") == "close_pause":
                self.resume(send_to_server=False)
                return


    def draw_tiles(self):
        """ Draw all tiles from the tmx file"""

        tmx = self.loader.tmx

        for layer in tmx.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    image = tmx.get_tile_image_by_gid(gid)
                    if image:
                        self.screen.blit(
                            image,
                            (x * tmx.tilewidth, y * tmx.tileheight)
                        )


    def draw(self):
        """ Draws all sprites."""

        self.screen.blit(background_image,(0,0))
        self.draw_tiles()
        self.all_sprites.draw(self.screen)
        for player in self.players:
            pygame.draw.rect(self.screen, (255, 0, 0), player.rect, 2)
        self.draw_timer()

        if self.game_controller.is_paused:
            self.draw_dead()

        if self.is_menu_paused:
            self.pause_menu.draw()

        pygame.display.flip()


    def draw_dead(self):
        """ Transparent surface as an overlay"""

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # schwarz, 150/255 Transparenz
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Courier New", 36, bold=True)
        text1 = font.render("Ein Spieler ist gestorben!", True, (255, 255, 255))
        self.screen.blit(text1, text1.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 20)))

        text2 = font.render("Neuer Versuch ...", True, (200, 200, 200))
        self.screen.blit(text2, text2.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 30)))


    def draw_timer(self):
        """draws a timer to track time of run"""

        font = pygame.font.SysFont("Courier New", 36, bold=True)

        minutes = int(self.timer // 60)
        seconds = int(self.timer % 60)

        timer_string = f"{minutes:02}:{seconds:02}"

        text = font.render(timer_string,True,(255, 255, 255)
        )

        self.screen.blit(text, (20, 20))


    def stop_timer(self):
        """stops the timer"""

        self.timer_running = False


    def handle_event(self, event):
        """ While paused, all input goes to the pause menu overlay (Esc closes it again).
            While playing, Esc opens the pause overlay. """
        if self.is_menu_paused:
            self.pause_menu.handle_event(event)
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause()


    def run(self, dt):
        """ Overrides and extends the base method to synchronize the data from the server on every frame.
            While the pause overlay is open, gameplay is frozen. """
        if self.is_menu_paused:
            self.draw()
            self.sync_network()
            return

        if not self.game_controller.is_paused:
            if self.timer_running: self.timer += dt
            self.update(dt)
        self.sync_network()
        self.draw()