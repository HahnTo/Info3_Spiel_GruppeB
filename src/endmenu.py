
from button import Button
#from menu import AbstractMenu
#import pygame

class EndMenu:
    """ Creates the end menu that appears after the game."""
    BGCOLOR = (216,161,123)
    
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.create_buttons()
    


    def create_buttons(self):
        """ Adds buttons to the menu."""
        self.buttons.append(Button('Neustart',48, (300,300)))
        


    
    def draw(self):
        """ Draws the menu with all buttons."""
        self.screen.fill(self.BGCOLOR)
        for button in self.buttons:
            button.draw(self.screen)
        
  

    