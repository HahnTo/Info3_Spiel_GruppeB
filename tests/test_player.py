import pygame
import pytest
from pygame import Vector2

from src.player import Player


# Dummy GameController for update function in Player
class DummyGC:
    def handle_horizontal_collision(self, player):
        pass

    def handle_vertical_collision(self, player):
        pass


# Every time Player is called in this file, a new instance of this player is automatically created
@pytest.fixture
def player():
    pygame.init()
    return Player(
        start_x=100,
        start_y=200,
        color=(255, 0, 0),
        player_id = 1,
        is_local = True
    )


def test_player_initialization(player):
    assert player.rect.x == 100
    assert player.rect.y == 200

    assert player.position == Vector2(100, 200)

    assert player.velocity == Vector2(0, 0)

    assert player.is_alive is True
    assert player.on_ground is False
    assert player.facing_right is True


def test_move_right(player):
    player.move(1)

    assert player.velocity.x == player.MOVE_SPEED
    assert player.facing_right is True


def test_move_left(player):
    player.move(-1)

    assert player.velocity.x == -player.MOVE_SPEED
    assert player.facing_right is False



def test_jump_when_on_ground(player):
    player.on_ground = True

    player.jump()

    assert player.velocity.y == player.JUMP_HEIGHT
    assert player.on_ground is False


def test_jump_when_not_on_ground(player):
    player.on_ground = False

    player.jump()

    assert player.velocity.y == 0


def test_update(player):
    gc = DummyGC()

    player.move(1)

    old_x = player.position.x

    player.update(1, gc)

    assert player.velocity.x == 0
    assert player.position.x == old_x + player.MOVE_SPEED


# # Sollte sich nicht bewegen können
# def test_die(player):
#     player.die()
#
#     player.on_ground = True
#     player.jump()
#     player.move(1)
#
#     assert player.is_alive is False
#     assert player.velocity == Vector2(0, 0)


def test_respawn(player):
    player.position = Vector2(500, 500)
    player.rect.x = 500
    player.rect.y = 500

    player.velocity = Vector2(10, 10)

    player.is_alive = False
    player.facing_right = False

    player.respawn()

    assert player.is_alive is True
    assert player.facing_right is True

    assert player.rect.x == player.start_x
    assert player.rect.y == player.start_y

    assert player.position == Vector2(player.start_x, player.start_y)

    assert player.velocity == Vector2(0, 0)