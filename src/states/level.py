# Soll die Platformen aus einer JSON oder ähnlichem laden, wenn ein neues Level erstellt wird.
import pygame

from obstacle import Obstacle
from player import Player
from states.state import State

WIDTH = 1080
HEIGHT = 720

BACKGROUND_COLOR = (0, 255, 0)


class Level(State):
    def __init__(self, screen, game_state_manager, game_controller):
        super().__init__(screen, game_state_manager)
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

        goal_obstacle2 = Obstacle((255, 0, 0), 50, 50, WIDTH -700, HEIGHT - 100, True)
        goal_obstacle2.add(self.all_sprites, self.obstacles)

        player1 = Player(20, HEIGHT - 20, 'burlywood4')
        player1.add(self.all_sprites, self.players)

        player2 = Player(60, HEIGHT - 20, 'burlywood')
        player2.add(self.all_sprites, self.players)


    def update(self, dt):
        """
            Update all sprites.
            Player sprites need the game controller as an additional parameter
        """
        self.obstacles.update()
        self.players.update(dt, self.game_controller)

    def draw(self):
        """ Draws all sprites."""
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)

        # After drawing the sprites, you need to flip it on the display
        pygame.display.flip()
