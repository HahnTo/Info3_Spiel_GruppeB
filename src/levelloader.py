import pytmx
import pygame

from src.config import GRAPHICS_DIR
from src.obstacle import Obstacle

class LevelLoader:
    """ Loads the map from tmx files and converts it to the actual obstacles. """

    def __init__(self,path,level):
        try:
            self.tmx = pytmx.load_pygame(path)
        except Exception as e:
            print(f"Fehler beim laden der Map: {e}")

        self.level = level


    def load(self):
        """ Generates the obstacles from the tmx objects.
            Sets all different flags which where set in the Tiled editor
            and loads images for moving platforms since they cannot be
            loaded through the tiled editor. """


        for obj in self.tmx.objects:
            obj_type = obj.properties.get("obj_type")
            if obj_type is None:
                continue

            #solid -> default platforms and moving platforms if they have a button id
            if obj_type == "solid":
                button_id = obj.properties.get("button_id")
                if button_id is not None:
                    try:
                        image = pygame.image.load(GRAPHICS_DIR / "map" / "movable.png").convert_alpha()
                    except Exception as e:
                        print(f"Fehler beim laden vom Bild: {e}")
                else:
                    image = pygame.Surface([obj.width, obj.height])
                    image.set_alpha(0)
                obstacle = Obstacle(
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    False,
                    False,
                    False,
                    button_id,
                    image = image
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)


            # goal
            elif obj_type == "goal":
                try:
                    image = pygame.image.load(GRAPHICS_DIR / "map" / "Flagge_2.png").convert_alpha()
                except Exception as e:
                    print(f"Fehler beim laden vom Bild: {e}")

                scaled_image = pygame.transform.scale(image, (57, 51))
                scaled_image.set_colorkey((254, 254, 254))
                image = scaled_image

                obstacle_g = Obstacle(
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    is_goal=True,
                    image = image

                )
                obstacle_g.add(self.level.all_sprites, self.level.obstacles)


            # movable blocks
            elif obj_type == "movable":
                try:
                    image = pygame.image.load(GRAPHICS_DIR/"map"/"Block_3.png").convert_alpha()
                except Exception as e:
                    print(f"Fehler beim laden vom Bild: {e}")

                image.set_colorkey((255, 255, 255))
                obstacle = Obstacle(
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y,
                    False,
                    True,
                    False,
                    image = image
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)
                obstacle.image.set_colorkey((255,255,255))


            # button
            elif obj_type == "button":
                button_id = obj.properties.get("button_id")
                try:
                    image = pygame.image.load(GRAPHICS_DIR / "map" / "Button.png").convert_alpha()
                except Exception as e:
                    print(f"Fehler beim laden vom Bild: {e}")

                obstacle = Obstacle(
                    obj.width,
                    obj.height,
                    obj.x,
                    obj.y+28,
                    False,
                    False,
                    True,
                    button_id,
                    image = image
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)


            # deadly obstacle
            elif obj_type == "deadly":
                image = pygame.Surface([obj.width, obj.height])
                image.set_alpha(0)
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
                    image = image
                )
                obstacle.add(self.level.all_sprites, self.level.obstacles)