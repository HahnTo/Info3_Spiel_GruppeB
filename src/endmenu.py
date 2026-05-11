
from button import Button
#from menu import AbstractMenu
#import pygame

class EndMenu:

    BGCOLOR = (216,161,123)
    
    def __init__(self, screen):

        self.screen = screen
        self.buttons = []
        self.create_buttons()
    


    def create_buttons(self):
        self.buttons.append(Button('Neustart',48, (300,300)))
        self.buttons.append(Button('End Game',48, (200,300)))


    
    def draw(self):
        self.screen.fill(self.BGCOLOR)
        for button in self.buttons:
            button.draw(self.screen)
        
  

    