import pygame



class Button:

    

    def __init__(self, text, size, position):
        
        self.text = text
        self.size = size
        self.position = position


    def draw(self, screen):
        FONT = pygame.font.SysFont('Arial',self.size)
        text_surf = FONT.render(self.text, False, (255,255,255))
        self.text_rect = text_surf.get_rect(center = self.position)
        screen.blit(text_surf, self.text_rect)

    
    def is_pressed(self):
        
        mouse_pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(mouse_pos):  
            if pygame.mouse.get_pressed()[0]: return True
        else : return False

    #def is_pressed(self):
        #mouse_pos = pygame.mouse.get_pos()
        #return self.text_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]