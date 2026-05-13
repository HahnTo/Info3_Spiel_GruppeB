import pygame
from pygame import Vector2
from typing import Literal



class Player(pygame.sprite.Sprite):
    """
    Creates the players in Mole Escape.
    The physics and movement are implemented here.
    """

    # Physics of the player
    WIDTH = 30
    HEIGHT = 40

    GRAVITY = 0.8
    MOVE_SPEED = 5.0
    # Must be negative, since the grid starts at (0, 0) in the top-left corner
    JUMP_HEIGHT = -12.0
    DUCK_HEIGHT = HEIGHT * 0.8

    # Static variable to assign an ID to each new Player
    player_id = 1

    def __init__(self, start_x, start_y, color):
        """
        Initializes the player.

        Sets the starting point and color.
        Until the textures are ready, simple colors are used.
        """
        super().__init__()

        self.start_x = start_x
        self.start_y = start_y

        self.player_id = Player.player_id
        Player.player_id += 1

        # Create the rect for the player
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = self.image.get_rect(topleft=(self.WIDTH, self.HEIGHT))
        self.image.fill(color)

        # Set the position to his spawn point
        self.rect.x = start_x
        self.rect.y = start_y
        self.position = Vector2(start_x, start_y)


        # The velocity is the player's speed in the x and y directions. It is added to the current position in every frame in the update function.
        self.velocity = Vector2(0,0)

        # States
        self.on_ground = False
        self.is_duck = False
        self.is_alive = True
        self.facing_right = True # Wird später für die Texturen und Interaktion mit Gegenständen o.ä. gebraucht.


    def move(self, direction: Literal[-1, 0, 1]):
        """
        Moves the player when the function is called.
        direction: -1 = left, 0 = stay in place, 1 = right
        """

        if not self.is_alive or direction == 0:
            return

        # Multiplikation mit direction, um velocity.x positiv oder negativ zu erhalten
        # Multiplying the SPEED by direction determines the sign, and thus the direction.
        self.velocity.x = direction * self.MOVE_SPEED

        if direction == 1:
            self.facing_right = True
        else:
            self.facing_right = False


    def jump(self):
        """ The player jumps when standing on the ground. """

        if not self.is_alive:
            return

        if self.on_ground:
            self.velocity.y = self.JUMP_HEIGHT
            self.on_ground = False

    def update(self, dt, gc):
        """ Update the player's position based on velocity and apply physics and collision handling. """

        if not self.is_alive:
            return

        # The vertical velocity is increased slightly every frame, which creates the physics of falling
        if not self.on_ground:
            self.velocity.y += self.GRAVITY

        # horizontal movement
        self.position.x += self.velocity.x
        self.rect.x = int(self.position.x)
        gc.handle_horizontal_collision(self)

        # vertikal movement
        self.position.y += self.velocity.y
        self.rect.y = int(self.position.y)

        self.on_ground = False
        gc.handle_vertical_collision(self)

        # Set the horizontal speed to zero to stop the player when the key is no longer pressed down
        self.velocity.x = 0


    def respawn(self):
        """ The player is reset and teleported to the spawn point. """
        self.is_alive = True
        self.facing_right = True
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.position = Vector2(self.start_x, self.start_y)
        self.velocity.x = 0
        self.velocity.y = 0
