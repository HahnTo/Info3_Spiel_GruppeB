import pygame

from inputhandler import InputHandler
from player import Player
from obstacle import Obstacle
from endmenu import EndMenu

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

BACKGROUND_COLOR = (0, 255, 0)

class GameController:
    """Initializes the game and creates the game loop"""


    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption(TITLE)

        # The tick speed is set to 60 in the game loop to limit the frame rate to 60 FPS
        self.clock = pygame.time.Clock()
        self.dt = 0


        # Initialise all sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()


        self.playing = True
        self.menu = None


        self.input_handler = InputHandler()


    def events(self):
        """Reacts to all pygame.events, like keyboard input and closing the Window"""
        for event in pygame.event.get():
            # Ends the script if window gets closed
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.input_handler.get_input(self.players)

    def draw(self):
        """Draws the in-game screen"""
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)

        # After drawing the sprites, you need to flip it on the display
        pygame.display.flip()


    def update(self, dt):
        """
        Update all sprites.
        Player sprites need the game controller as an additional parameter
        """
        for sprite in self.all_sprites:
            if not sprite in self.players:
                sprite.update(dt)
            else:
                sprite.update(dt, self)


    def handle_horizontal_collision(self, player):
        """ Handles horizontal collisions.
            If the player is coming from the left, their position is set to the right side of the object.
            If the player is coming from the right, their position is set to the left side of the object.
        """
        #Name passt nicht so ganz weil mehr gemacht wird als Kollision checken, Player Movement wird beeinflusst
        #Wahrscheinlich Kollision und Movement Beeinflussung seperat, maybe Movement Beeinflussung dann im Player

        # Get all objects that are colliding with each other
        collider_group = pygame.sprite.spritecollide(player, self.obstacles, False)
        for obstacle in collider_group:
            # If the obstacle is the goal, set playing to false. The game loop will then jump to the end menu.
            if obstacle.is_goal:
                self.playing = False
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
        collider_group = pygame.sprite.spritecollide(player, self.obstacles, False)
        for obstacle in collider_group:
            if obstacle.is_goal:
                self.playing = False
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
        self.playing = True

        #auslagern in Level
        frame_wall_left = Obstacle((255, 0, 0), 10, HEIGHT, -10, 0)
        frame_wall_left.add(self.all_sprites, self.obstacles)

        frame_wall_right = Obstacle((255, 0, 0), 10, HEIGHT, WIDTH, 0)
        frame_wall_right.add(self.all_sprites, self.obstacles)

        frame_floor = Obstacle((0, 0, 255), WIDTH, 20, 0, HEIGHT-20)
        frame_floor.add(self.all_sprites, self.obstacles )

        platform1 = Obstacle((0, 0, 255), 200, HEIGHT-100, 300, HEIGHT-100)
        platform1.add(self.all_sprites, self.obstacles)

        platform2 = Obstacle((0, 0, 255), 20, 70, 500, HEIGHT-150)
        platform2.add(self.all_sprites, self.obstacles)

        platform3 = Obstacle((0, 0, 255), 200, HEIGHT-150, 500, HEIGHT-150)
        platform3.add(self.all_sprites, self.obstacles)

        platform4 = Obstacle((0, 0, 255), 20, 70, 700, HEIGHT-200)
        platform4.add(self.all_sprites, self.obstacles)

        platform5 = Obstacle((0, 0, 255), 400, HEIGHT-200, 700, HEIGHT-200)
        platform5.add(self.all_sprites, self.obstacles)

        platform6 = Obstacle((0, 0, 255), 20, 80, 300, HEIGHT-100)
        platform6.add(self.all_sprites, self.obstacles)

        platform7 = Obstacle((0, 0, 255), 80, 80, 850, HEIGHT-280)
        platform7.add(self.all_sprites, self.obstacles)

        platform8 = Obstacle((0, 0, 255), 20, 200, 650, HEIGHT-500)
        platform8.add(self.all_sprites, self.obstacles)

        platform9 = Obstacle((0, 0, 255), 40, 20, 670, HEIGHT-320)
        platform9.add(self.all_sprites, self.obstacles)

        platform10 = Obstacle((0, 0, 255), 30, 20, 670, HEIGHT-400)
        platform10.add(self.all_sprites, self.obstacles)

        platform11 = Obstacle((0, 0, 255), 400, 20, 800, HEIGHT-450)
        platform11.add(self.all_sprites, self.obstacles)

        platform12 = Obstacle((0, 0, 255), 200, 20, 0, HEIGHT-500)
        platform12.add(self.all_sprites, self.obstacles)

        platform13 = Obstacle((0, 0, 255), 300, 20, 350, HEIGHT-500)
        platform13.add(self.all_sprites, self.obstacles)

        platform14 = Obstacle((0, 0, 255), 400, 20, 800, HEIGHT-450)
        platform14.add(self.all_sprites, self.obstacles)



        goal_obstacle = Obstacle((255, 0, 0), 50, 50, 0, HEIGHT-550, True)
        goal_obstacle.add(self.all_sprites, self.obstacles)


        player1 = Player(20, HEIGHT-20, 'burlywood4')
        player1.add(self.all_sprites, self.players)

        player2 = Player(60, HEIGHT-20, 'burlywood')
        player2.add(self.all_sprites, self.players)

        end_menu = EndMenu(self.screen)

        # Gameloop mit allen update ... Funktionen
        #Gamestates benutzen statt if else
        # Game loop with the different game states. In each frame, events are checked and all elements are updated.
        while True:
            # Delta time ensures that movement and timers stay consistent regardless of the frame rate.
            self.dt = self.clock.tick(FPS) / 1000
            # Handle all events
            self.events()
            # If playing, update all sprites and draw them.
            if self.playing:
                self.update(self.dt)
                self.draw()
            # If not playing, show the end menu and wait for input.
            else:
                end_menu.draw()
                pygame.display.flip()
                if  end_menu.buttons[0].is_pressed():
                    self.playing = True
                    for player in self.players.sprites():
                        player.respawn()



            

            


gc = GameController()

gc.run()


