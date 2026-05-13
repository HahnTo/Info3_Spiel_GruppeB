import pygame



class Button:
    """ Creats a button which reacts to the function is_pressed() """

    def __init__(self, text, font_size, position):
        self.text = text
        self.font_size = font_size
        self.position = position

        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.text_surf = self.font.render(self.text, False, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.position)

    def draw(self, screen):
        """ Draws the button on the screen """
        screen.blit(self.text_surf, self.text_rect)

    
    def is_pressed(self):
        """ Checks if the button is pressed.
            Returns True or False.
        """
        
        mouse_pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        else :
            return False