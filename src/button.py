import pygame



class Button:
    """ Creats a button which reacts to the function is_pressed() """

    def __init__(self, text, font_size, position, event_function):
        self.text = text
        self.font_size = font_size
        self.position = position
        self.event_function = event_function

        self.selected = False
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.text_surf = self.font.render(self.text, False, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.position)

    def draw(self, screen):
        """ Draws the button on the screen. If the button is selected, he gets a border"""
        if self.selected:
            pygame.draw.rect(
                screen,
                (255, 215, 0),  # border color
                self.text_rect.inflate(20, 10),  #  Border slightly larger than the text_rect
                3  # Border width
            )
        screen.blit(self.text_surf, self.text_rect)

    
    def on_click(self):
        """ Returns the event function """
        self.event_function()