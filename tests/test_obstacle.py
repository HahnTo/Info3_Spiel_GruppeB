import pygame
import pytest

from src.config import GRAPHICS_DIR
from src.obstacle import Obstacle


@pytest.fixture(autouse=True)
def pygame_init():
    """Ensure pygame is initialized for all tests that need it."""
    pygame.init()   # Setup
    yield           # Tests
    pygame.quit()   # After tests


class TestObstacle:
    @pytest.fixture
    def basic_obstacle(self):
        image = pygame.Surface((50, 20))

        return Obstacle(width=50, height=20, x_pos=100, y_pos=200, image=image)

    @pytest.fixture
    def goal_obstacle(self):
        image = pygame.Surface((50, 20))

        return Obstacle(width=30, height=30, x_pos=0, y_pos=0, is_goal=True, image=image)

    @pytest.fixture
    def deadly_obstacle(self):
        image = pygame.Surface((50, 20))

        return Obstacle(width=30, height=10, x_pos=0, y_pos=0, is_deadly=True, image=image)

    @pytest.fixture
    def movable_obstacle(self):
        image = pygame.Surface((50, 20))

        return Obstacle(width=40, height=40, x_pos=50, y_pos=50, is_movable=True, image=image)

    @pytest.fixture
    def button_obstacle(self):
        image = pygame.Surface((50, 20))

        return Obstacle(width=20, height=20, x_pos=10, y_pos=10, is_button=True, button_id=42, image=image)


    def test_basic_obstacle(self, basic_obstacle):
        """ Tests if the position is right and all the flags are created right. """
        assert basic_obstacle.rect.x == 100
        assert basic_obstacle.rect.y == 200
        assert basic_obstacle.is_goal is False
        assert basic_obstacle.is_movable is False
        assert basic_obstacle.is_button is False
        assert basic_obstacle.is_deadly is None

    def test_flags(self, goal_obstacle, deadly_obstacle, movable_obstacle, button_obstacle):
        assert goal_obstacle.is_goal is True
        assert deadly_obstacle.is_deadly is True
        assert movable_obstacle.is_movable is True
        assert button_obstacle.is_button is True
        assert button_obstacle.button_id == 42

    def test_reset(self, basic_obstacle):
        basic_obstacle.y_pos = basic_obstacle.y_start + 50
        basic_obstacle.reset()
        assert basic_obstacle.y_pos == basic_obstacle.y_start
        assert basic_obstacle.rect.y == basic_obstacle.y_start