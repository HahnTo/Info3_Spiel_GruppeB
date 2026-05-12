import pygame



class Button:
    """ Creats a button which reacts to the function is_pressed() """

    def __init__(self, text, font_size, position):
        self.text = text
        self.font_size = font_size
        self.position = position

        self.text_rect = None


    def draw(self, screen):
        """ Draws the button on the screen """
        font = pygame.font.SysFont('Arial',self.font_size)
        text_surf = font.render(self.text, False, (255,255,255))
        self.text_rect = text_surf.get_rect(center = self.position)
        screen.blit(text_surf, self.text_rect)

    
    def is_pressed(self):
        """ Checks if the button is pressed.
            Returns True or False.
        """
        
        mouse_pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        else :
            return False