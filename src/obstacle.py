import pygame

class Obstacle(pygame.sprite.Sprite):
    """ Creates Obstacle to build the map. """
    

    def __init__(self, color, width, height,x_pos, y_pos, is_goal=False, is_movable= False, is_button = False,button_id = None):
        super().__init__()
        self.is_movable = is_movable
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.y_start = y_pos
        self.button_id = button_id #buttons und zugehörige obstacles bekommen id
        self.is_goal = is_goal
        self.is_button = is_button #buttonobstacles dann true
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)

    def move(self,range):
        range = range
        print("Obstacle bewegt sich runter")
        if self.y_pos - self.y_start <= range:
            self.y_pos += 5
        self.rect.topleft = (self.x_pos, self.y_pos)

    def move_up(self):
        print("Obstacle bewegt sich hoch")
        if self.y_pos > self.y_start:
            self.y_pos -= 5
        self.rect.topleft = (self.x_pos, self.y_pos)

    def update(self):
        if self.button_id is not None and not self.is_button:
            self.move_up()

    def draw(self,screen):
        screen.blit(self.image,self.rect)



        