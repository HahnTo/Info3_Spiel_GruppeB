from abc import ABC, abstractmethod

class AbstractMenu(ABC):

    BGCOLOR = (216,161,123)

    def __init__(self, screen):
        self.screen = screen
        self.buttons = []

    @abstractmethod
    def create_buttons(self):
        pass


    def draw(self):
        self.screen.fill(self.BGCOLOR)
        for button in self.buttons:
            button.draw(self.screen)

        

