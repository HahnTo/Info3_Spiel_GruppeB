import pygame

from src.button import Button

from src.states.state import State


#from menu import AbstractMenu
#import pygame

class EndMenu(State):
    """ Creates the end menu that appears after the game."""
    BGCOLOR = (216,161,123)
    
    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)

        self.buttons = []
        self.create_buttons()

    def run(self, dt):
        self.update(dt)
        self.draw()

    def create_buttons(self):
        """ Adds buttons to the menu."""
        self.buttons.append(Button('Neustart',48, (300,300)))

    def update(self, dt):
        pass

    def draw(self):
        """ Draws the menu with all buttons."""
        self.screen.fill(self.BGCOLOR)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()
        
  

    