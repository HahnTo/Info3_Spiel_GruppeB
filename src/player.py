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

    # How fast the remote player glides toward the target position (0.1 = slow/smooth, 0.3 = fast/snappy)
    INTERP_ALPHA = 0.5
    # If the remote player is further away than this, teleport instead of interpolating (e.g. after respawn)
    SNAP_THRESHOLD = 50

    def __init__(self, start_x, start_y, color, player_id, is_remote):
        """
        Initializes the player.

        Sets the starting point and color.
        Until the textures are ready, simple colors are used.
        """
        super().__init__()

        self.start_x = start_x
        self.start_y = start_y

        self.player_id = player_id

        self.is_remote = is_remote
        # The target position received from the last network packet.
        self.network_target = Vector2(start_x, start_y)
        # The velocity received from the last network packet.
        # Used to extrapolate movement between packets.
        self.network_velocity = Vector2(0, 0)

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

        # Remote players are handled by update_remote(), not here
        if self.is_remote:
            self._update_remote()
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

    def _update_remote(self):
        """ Called every frame for the remote player instead of the normal physics update """

        # Extrapolation
        if self.on_ground:
            # On the ground: stop all vertical movement immediately.
            # Without this, gravity would accumulate every frame and push
            # net_target downward even though the player is standing still
            # → causes the up/down jitter you see on flat surfaces.
            self.network_velocity.y = 0
            self.network_target.y = self.position.y  # lock Y, only slide horizontally
            self.network_target.x += self.network_velocity.x
        else:
            # In the air: simulate gravity so jump arcs look correct
            # between packets, even without a new network update every frame.
            self.network_velocity.y += self.GRAVITY
            self.network_target.x += self.network_velocity.x
            self.network_target.y += self.network_velocity.y

        # Interpolation
        # Instead of jumping straight to net_target, we move a fraction of the
        # remaining distance each frame. This smooths out any jitter from uneven
        # packet timing.
        distance = self.network_target - self.position
        dist_len = distance.length()

        if dist_len > self.SNAP_THRESHOLD:
            # Too far away (e.g. after respawn) – teleport immediately.
            self.position.update(self.network_target)
        elif dist_len > 0.5:
            # Normal case – glide toward the target.
            self.position += distance * self.INTERP_ALPHA

        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

    def respawn(self):
        """ The player is reset and teleported to the spawn point. """
        self.is_alive = True
        self.facing_right = True
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.position = Vector2(self.start_x, self.start_y)
        self.velocity.x = 0
        self.velocity.y = 0

        # Also reset the network interpolation state so the remote player
        # doesn't glide in from the old position after a respawn.
        if self.is_remote:
            self.network_target = Vector2(self.start_x, self.start_y)
            self.network_velocity = Vector2(0, 0)

    def get_data(self):
        """Send player state to server."""
        return {
            "x": self.position.x,
            "y": self.position.y,
            "vx": self.velocity.x,
            "vy": self.velocity.y,
            "facing_right": self.facing_right,
            "on_ground": self.on_ground
        }

    # def set_data(self, data):
    #     """Apply network state to player."""
    #
    #     if not data:
    #         return
    #
    #     self.position.x = data["x"]
    #     self.position.y = data["y"]
    #
    #     self.velocity.x = data["vx"]
    #     self.velocity.y = data["vy"]
    #
    #     self.facing_right = data["facing_right"]
    #     self.on_ground = data["on_ground"]
    #
    #     # Sync rect with position
    #     self.rect.x = int(self.position.x)
    #     self.rect.y = int(self.position.y)

    def set_data(self, data):
        """ Apply a network state update to the remote player """

        if not data:
            return

        # Always update non-positional state immediately – these don't need smoothing.
        self.facing_right = data["facing_right"]
        self.on_ground = data["on_ground"]

        if self.is_remote:
            # Save the authoritative position as the new target.
            # _update_remote() will glide toward it over the next frames.
            self.network_target.x = data["x"]
            self.network_target.y = data["y"]

            # Save the velocity so extrapolation continues in the right direction
            # between packets.
            self.network_velocity.x = data["vx"]
            self.network_velocity.y = data["vy"]
        else:
            # Local player (should not normally receive set_data, but handle it cleanly).
            self.position.x = data["x"]
            self.position.y = data["y"]
            self.velocity.x = data["vx"]
            self.velocity.y = data["vy"]
            self.rect.x = int(self.position.x)
            self.rect.y = int(self.position.y)