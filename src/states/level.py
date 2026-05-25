# Soll die Platformen aus einer JSON oder ähnlichem laden, wenn ein neues Level erstellt wird.
import pygame

from src.obstacle import Obstacle
from src.player import Player
from src.states.state import State

WIDTH = 1080
HEIGHT = 720

BACKGROUND_COLOR = (0, 255, 0)


class Level(State):
    def __init__(self, screen, game_state_manager, game_controller, network_client=None):
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

        # # 20 updates per second are enough for smooth gameplay and prevent too many packets per second
        # self.network_update_interval = 1 / 20
        # self.network_update_timer = 0

        self.game_controller = game_controller

        # Initialise all sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        self.create_sprites()

    def create_sprites(self):
        frame_wall_left = Obstacle((255, 0, 0), 10, HEIGHT, -10, 0)
        frame_wall_left.add(self.all_sprites, self.obstacles)

        frame_wall_right = Obstacle((255, 0, 0), 10, HEIGHT, WIDTH, 0)
        frame_wall_right.add(self.all_sprites, self.obstacles)

        frame_floor = Obstacle((0, 0, 255), WIDTH, 20, 0, HEIGHT - 20)
        frame_floor.add(self.all_sprites, self.obstacles)

        platform1 = Obstacle((0, 0, 255), 200, HEIGHT - 100, 300, HEIGHT - 100)
        platform1.add(self.all_sprites, self.obstacles)

        platform2 = Obstacle((0, 0, 255), 20, 70, 500, HEIGHT - 150)
        platform2.add(self.all_sprites, self.obstacles)

        platform3 = Obstacle((0, 0, 255), 200, HEIGHT - 150, 500, HEIGHT - 150)
        platform3.add(self.all_sprites, self.obstacles)

        platform4 = Obstacle((0, 0, 255), 20, 70, 700, HEIGHT - 200)
        platform4.add(self.all_sprites, self.obstacles)

        platform5 = Obstacle((0, 0, 255), 400, HEIGHT - 200, 700, HEIGHT - 200)
        platform5.add(self.all_sprites, self.obstacles)

        platform6 = Obstacle((0, 0, 255), 20, 80, 300, HEIGHT - 100)
        platform6.add(self.all_sprites, self.obstacles)

        platform7 = Obstacle((0, 0, 255), 80, 80, 850, HEIGHT - 280)
        platform7.add(self.all_sprites, self.obstacles)

        platform8 = Obstacle((0, 0, 255), 20, 200, 650, HEIGHT - 500)
        platform8.add(self.all_sprites, self.obstacles)

        platform9 = Obstacle((0, 0, 255), 40, 20, 670, HEIGHT - 320)
        platform9.add(self.all_sprites, self.obstacles)

        platform10 = Obstacle((0, 0, 255), 30, 20, 670, HEIGHT - 400)
        platform10.add(self.all_sprites, self.obstacles)

        platform11 = Obstacle((0, 0, 255), 400, 20, 800, HEIGHT - 450)
        platform11.add(self.all_sprites, self.obstacles)

        platform12 = Obstacle((0, 0, 255), 200, 20, 0, HEIGHT - 500)
        platform12.add(self.all_sprites, self.obstacles)

        platform13 = Obstacle((0, 0, 255), 300, 20, 350, HEIGHT - 500)
        platform13.add(self.all_sprites, self.obstacles)

        platform14 = Obstacle((0, 0, 255), 400, 20, 800, HEIGHT - 450)
        platform14.add(self.all_sprites, self.obstacles)

        goal_obstacle = Obstacle((255, 0, 0), 50, 50, 0, HEIGHT - 550, True)
        goal_obstacle.add(self.all_sprites, self.obstacles)

        #goal_obstacle2 = Obstacle((255, 0, 0), 50, 50, WIDTH -700, HEIGHT - 100, True)
        #goal_obstacle2.add(self.all_sprites, self.obstacles)

        movable_block = Obstacle((0,0,255),30,50,130,HEIGHT-70,False,True)
        movable_block.add(self.all_sprites, self.obstacles)

        button_obstacle = Obstacle((0,0,0),20,20,400,HEIGHT -120,False,False,True,2)
        button_obstacle.add(self.all_sprites,self.obstacles)

        moving_obstacle = Obstacle((0,0,0),20,100,250,150,False,False,False,2)
        moving_obstacle.add(self.all_sprites, self.obstacles)

        if self.is_online:

            player1 = Player(20, HEIGHT - 20, 'burlywood4', 1, self.local_id == 1)  # If local_id == 1, the player with ID 1 is the local player.
            player1.add(self.all_sprites, self.players)

            player2 = Player(60, HEIGHT - 20, 'burlywood', 2, self.local_id == 2)
            player2.add(self.all_sprites, self.players)
        else:
            player1 = Player(20, HEIGHT - 20, 'burlywood4', 1, True)
            player1.add(self.all_sprites, self.players)

            player2 = Player(60, HEIGHT - 20, 'burlywood', 2, True)
            player2.add(self.all_sprites, self.players)

    def get_player(self, player_id):
        """Returns the player as a utility method."""
        for player in self.players.sprites():
            if player.player_id == player_id:
                return player
        return None

    def update(self, dt):
        """
            Update all sprites.
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

    def sync_network(self, dt):
        """Sends local player state to the server and applies received remote updates"""
        if not self.is_online:
            return

        local_player = self.get_player(self.local_id)
        remote_player = self.get_player(self.remote_id)

        # Limit update rate: send only one packet every 50ms (20x/s).
        # The game loop continues running at 60 FPS – only the network is throttled.
        # self.network_update_timer += dt
        # if self.network_update_timer >= self.network_update_interval:
        #     self.network_update_timer = 0
        if local_player:
            data = {
                "type": "update",
                "data": local_player.get_data()
            }
            self.network_client.send(data)

        update = self.network_client.get_update()

        if update and update.get("type") == "state" and remote_player:
            remote_player.set_data(update["data"])
            # # Client-side interpolation: the remote player moves between received positions instead of freezing.
            # # Continue using velocity from the last received state.
            # remote_player.position.x += remote_player.velocity.x
            # remote_player.position.y += remote_player.velocity.y
            # remote_player.rect.x = int(remote_player.position.x)
            # remote_player.rect.y = int(remote_player.position.y)

    def draw(self):
        """ Draws all sprites."""
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)

        # After drawing the sprites, you need to flip it on the display
        pygame.display.flip()

    def run(self, dt):
        """Overrides and extends the base method to synchronize the data from the server on every frame."""
        self.update(dt)
        self.sync_network(dt)
        self.draw()

    def handle_event(self, event):
        pass