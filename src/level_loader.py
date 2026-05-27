import pygame
import pytmx
from src.obstacle import Obstacle



class Level_loader:

    def __init__(self,path,level):
        self.tmx = pytmx.load_pygame(path)
        self.level = level

    def load(self):
        print("Map wird geladen")
        for obj in self.tmx.objects:
            print(obj)
            obj_type = obj.properties.get("obj_type")
            if obj_type is None:
                continue

            if obj_type == "solid":
                obstacle = Obstacle(
                    (0,0,255),
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)

                # GOAL
            elif obj_type == "goal":
                obstacle = Obstacle(
                    (255, 0, 0),
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    is_goal=True
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)

            # MOVABLE
            elif obj_type == "movable":
                obstacle = Obstacle(
                    (0, 0, 255),
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    False,
                    True
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)

            # BUTTON
            elif obj_type == "button":
                button_id = obj.properties.get("button_id")

                obstacle = Obstacle(
                    (0, 0, 0),
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    False,
                    False,
                    True,
                    button_id
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)