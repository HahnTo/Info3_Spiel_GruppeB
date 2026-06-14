import pytmx
import pygame

from config import GRAPHICS_DIR
from src.obstacle import Obstacle

class LevelLoader:
    """ Loads the map from tmx files and converts it to the actual obstacles. """

    def __init__(self,path,level):
        self.tmx = pytmx.load_pygame(path)
        self.level = level

    def load(self):
        """ Generates the obstacles from the tmx objects.
            Sets all different flags which where set in the Tiled editor. """
        print("Map wird geladen")
        for obj in self.tmx.objects:
            print(obj)
            obj_type = obj.properties.get("obj_type")
            if obj_type is None:
                continue

            if obj_type == "solid":
                button_id = obj.properties.get("button_id")
                obstacle = Obstacle(
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    False,
                    False,
                    False,
                    button_id,
                    image = pygame.Surface([obj.width, obj.height])
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)
                obstacle.image.set_alpha(0)

            # GOAL
            elif obj_type == "goal":
                obstacle = Obstacle(
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    is_goal=True,
                    image = pygame.Surface([obj.width, obj.height])
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)

            # MOVABLE
            elif obj_type == "movable":
                obstacle = Obstacle(
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    False,
                    True,
                    False,
                    image = pygame.image.load(GRAPHICS_DIR/"map"/"Block_3.png").convert_alpha()
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)
                obstacle.image.set_colorkey((255,255,255))

            # BUTTON
            elif obj_type == "button":
                button_id = obj.properties.get("button_id")

                obstacle = Obstacle(
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    False,
                    False,
                    True,
                    button_id,
                    image = pygame.Surface([obj.width, obj.height])
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)


            # Deadly obstacle
            elif obj_type == "deadly":
                obstacle = Obstacle(
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    False,
                    False,
                    False,
                    None,
                    True,
                    image = pygame.Surface([obj.width, obj.height])
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)