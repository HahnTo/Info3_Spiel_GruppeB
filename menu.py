from abc import ABC, abstractmethod

class Menu(ABC):

    BGCOLOR = (216,161,123)

    @abstractmethod
    def draw(self, screen):
        screen.fill(self.BGCOLOR)
        
        

