import pygame

class Obstacle(pygame.sprite.Sprite):
    """ Creates Obstacle to build the map. """
    

    def __init__(self, width, height,x_pos, y_pos, is_goal=False, is_movable= False, is_button = False,button_id = None, is_deadly=None, image = None):
        """ Initialize the obstacle with its physics and flags. """

        super().__init__()
        self.is_movable = is_movable
        self.is_deadly = is_deadly
        self.x_pos = x_pos
        self.x_start = x_pos
        self.y_pos = y_pos
        self.y_start = y_pos

        # Buttons and related obstacles get the same id
        self.is_button = is_button
        self.button_id = button_id
        self.is_goal = is_goal
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)


    def move(self,range):
        """moves obstacles that can be moved with a button"""

        range_y = range
        if self.y_pos - self.y_start <= range_y:
            self.y_pos += 5
        self.rect.topleft = (self.x_pos, self.y_pos)


    def move_up(self):
        """moves obstacles back down if the button is no longer pressed"""

        if self.y_pos > self.y_start:
            self.y_pos -= 5
        self.rect.topleft = (self.x_pos, self.y_pos)


    def update(self):
        """calls the move_up function"""

        if self.button_id is not None and not self.is_button:
            self.move_up()


    def draw(self,screen):
        """draws the obstacle"""

        screen.blit(self.image,self.rect)


    def reset(self):
        """ Resets the obstacle to its start position."""

        self.x_pos = self.x_start
        self.y_pos = self.y_start
        self.rect.topleft = (self.x_pos, self.y_pos)