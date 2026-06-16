import pygame

class Spritesheet:
    def __init__(self,image):
        self.sheet = image


    def get_image(self, frame, width, height, scale, colour, crop_x=6, crop_w=20):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))

        # Crop: nur den mittleren Bereich behalten
        cropped = pygame.Surface((crop_w, height))
        cropped.blit(image, (0, 0), (crop_x, 0, crop_w, height))

        cropped = pygame.transform.scale(cropped, (crop_w * scale, height * scale))
        cropped.set_colorkey(colour)
        return cropped