import pygame

from inputhandler import InputHandler
from src.gamestatemanager import GameStateManager
from src.states.endmenu import EndMenu
from src.states.level import Level

#mögliche Änderungen: Gamestates für Level, Startscreen und Endscreen,
#jede Klasse bekommt eigene Update und Render Funktion
#Hier im Gamecontroller dann nur noch Gamestates switchen und je nach State Update und Render Funktionen
#der jeweiligen Klasse aufrufen


WIDTH = 1080
HEIGHT = 720

TITLE = "Mole Escape"

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 48)

FPS = 60


class GameController:
    """Initializes the game and creates the game loop"""


    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption(TITLE)

        # The tick speed is set to 60 in the game loop to limit the frame rate to 60 FPS
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.game_state_manager = GameStateManager('level')

        self.level = Level(self.screen, self.game_state_manager, self)
        self.end_menu = EndMenu(self.screen, self.game_state_manager)

        self.states = {'level': self.level ,'end_menu': self.end_menu}


        self.input_handler = InputHandler()


    def events(self):
        """Reacts to all pygame.events, like keyboard input and closing the Window"""
        for event in pygame.event.get():
            # Ends the script if window gets closed
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if self.game_state_manager.get_state() == 'end_menu':
            if self.end_menu.buttons[0].is_pressed():
                    self.game_state_manager.set_state('level')
                    for player in self.level.players.sprites():
                        player.respawn()

        self.input_handler.get_input(self.level.players)


    def handle_horizontal_collision(self, player):
        """ Handles horizontal collisions.
            If the player is coming from the left, their position is set to the right side of the object.
            If the player is coming from the right, their position is set to the left side of the object.
        """
        #Name passt nicht so ganz weil mehr gemacht wird als Kollision checken, Player Movement wird beeinflusst
        #Wahrscheinlich Kollision und Movement Beeinflussung seperat, maybe Movement Beeinflussung dann im Player

        # Get all objects that are colliding with each other
        collider_group = pygame.sprite.spritecollide(player, self.level.obstacles, False)
        for obstacle in collider_group:
            # If the obstacle is the goal, set playing to false. The game loop will then jump to the end menu.
            if obstacle.is_goal:
                self.game_state_manager.set_state('end_menu')
            else:
                # It moves to the left, so it must stop at the right end of the obstacle.
                if player.velocity.x < 0:
                    player.rect.left = obstacle.rect.right
                    player.position.x = player.rect.x
                    player.velocity.x = 0
                # It moves to the right, so it must stop at the left end of the obstacle.
                elif player.velocity.x > 0:
                    player.rect.right = obstacle.rect.left
                    player.position.x = player.rect.x
                    player.velocity.x = 0


    def handle_vertical_collision(self, player):
        """ Handles vertical collisions.
            If the player is coming from above, their position is set to the top of the object.
            If the player is coming from below, their position is set to the bottom of the object.
        """

        # Get all objects that are colliding with each other
        collider_group = pygame.sprite.spritecollide(player, self.level.obstacles, False)
        for obstacle in collider_group:
            if obstacle.is_goal:
                self.game_state_manager.set_state('end_menu')
            else:
                # Since it's coming from below, it must stop at the bottom of the obstacle.
                if player.velocity.y < 0:
                    player.rect.top = obstacle.rect.bottom
                    player.position.y = player.rect.y
                    player.velocity.y = 0
                # Since it's coming from above, it must stop at the top of the obstacle.
                elif player.velocity.y > 0:
                    player.rect.bottom = obstacle.rect.top
                    player.on_ground = True
                    player.position.y = player.rect.y
                    player.velocity.y = 0


    def run(self):
        """ This is the main function.
            It initializes all objects and runs the game loop.
            It switches between different game states.
        """

        # Game loop with the different game states. In each frame, events are checked and all elements are updated.
        while True:
            # Delta time ensures that movement and timers stay consistent regardless of the frame rate.
            self.dt = self.clock.tick(FPS) / 1000

            # Handle all events
            self.events()

            self.states[self.game_state_manager.get_state()].run(self.dt)



if __name__ == "__main__":
    gc = GameController()
    gc.run()


