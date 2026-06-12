# Soll die Platformen aus einer JSON oder ähnlichem laden, wenn ein neues Level erstellt wird.
import pygame
import pytmx

from src.config import ASSETS_DIR
from src.player import Player
from src.states.state import State
from src.levelloader import LevelLoader

WIDTH = 1080
HEIGHT = 720

BACKGROUND_COLOR = (0, 255, 0)

# Level 1: easy
# Level 2: mid
# Level 3: hard
# Level 4: server

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
            self.remote_id = 3 - self.local_id      # # It returns 1 or 2 when 3 is subtracted
        else:
            self.local_id = None
            self.remote_id = None

        self.level_id = level_id
        map_location = ASSETS_DIR / f"maps/map_{level_id}.tmx"

        self.game_controller = game_controller
        self.loader = LevelLoader(map_location, self)

        # Initialise all sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        self.create_players()
        self.load_map()

    def load_map(self):
        """ Load the map from the Level loader"""
        self.loader.load()

    def create_players(self):
        """ Create the players with their spawnpoint and physics"""
        if self.is_online:
            # If local_id == 1, the player with ID 1 is the local player
            player1 = Player(30, HEIGHT - 20, 'burlywood4', 1, self.local_id == 1)
            player1.add(self.all_sprites, self.players)

            player2 = Player(60, HEIGHT - 20, 'burlywood', 2, self.local_id == 2)
            player2.add(self.all_sprites, self.players)
        else:
            player1 = Player(20, HEIGHT - 400, 'burlywood4', 1, True)
            player1.add(self.all_sprites, self.players)

            player2 = Player(60, HEIGHT - 20, 'burlywood', 2, True)
            player2.add(self.all_sprites, self.players)

    def get_player(self, player_id):
        """Returns the player with the given player_id."""
        for player in self.players.sprites():
            if player.player_id == player_id:
                return player
        return None

    def update(self, dt):
        """ Update all sprites.
            Player sprites need the game controller as an additional parameter
        """
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

    def sync_network(self):
        """Sends local player state to the server and applies received remote updates"""
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
                self.game_controller.restart_online()
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
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_tiles()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self, dt):
        """ Overrides and extends the base method to synchronize the data from the server on every frame."""
        self.update(dt)
        self.sync_network()
        self.draw()