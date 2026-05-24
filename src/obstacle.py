import pygame

class Obstacle(pygame.sprite.Sprite):
    """ Creates Obstacle to build the map. """
    

    def __init__(self, color, width, height,x_pos, y_pos, is_goal=False, is_movable= False):
        super().__init__()
        self.is_movable = is_movable
        self.is_goal = is_goal
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)
        