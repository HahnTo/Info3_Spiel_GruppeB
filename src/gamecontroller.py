import pygame

from inputhandler import InputHandler
from level import Level
from player import Player
from obstacle import Obstacle
from button import Button
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
    """Initialisiert das Spiel und erstellt den Game-Loop"""


    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption(TITLE)

        # Clock wartet immer bestimmte Zeit, bis der nächste Frame geladen wird und gibt die Delta Time zurück
        self.clock = pygame.time.Clock()
        self.dt = 0


        # Alle verschiedenen Sprite Gruppen initialisieren
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()


        self.playing = True
        self.menu = None


        self.input_handler = InputHandler()




    def events(self):
        for event in pygame.event.get():
            # Checkt, ob das Fenster geschlossen wird
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                

        self.input_handler.get_input(self.players.sprites()[0])

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)

        # Lädt das komplette Display neu
        pygame.display.flip()


    def update(self, dt):
        for sprite in self.all_sprites:
            if not sprite in self.players:
                sprite.update(dt)
            else:
                sprite.update(dt, self)


    def check_horizontal_collision(self, player):
        #Name passt nicht so ganz weil mehr gemacht wird als Kollision checken, Player Movement wird beeinflusst
        #Wahrscheinlich Kollision und Movement Beeinflussung seperat, maybe Movement Beeinflussung dann im Player
        collider_group = pygame.sprite.spritecollide(player, self.obstacles, False)
        for obstacle in collider_group:
            if obstacle.is_goal:
                self.playing = False
            else:
                if player.velocity.x < 0:     # Bewegt sich nach links, also muss er an dem rechten Ende vo, Obstacle stehen bleiben.
                    player.rect.left = obstacle.rect.right
                    player.position.x = player.rect.x
                    player.velocity.x = 0
                elif player.velocity.x > 0:   # Bewegt sich nach rechts
                    player.rect.right = obstacle.rect.left
                    player.position.x = player.rect.x
                    player.velocity.x = 0


    def check_vertical_collision(self, player):

        collider_group = pygame.sprite.spritecollide(player, self.obstacles, False)
        for obstacle in collider_group:
            if obstacle.is_goal:
                self.playing = False
            else:
                if player.velocity.y < 0:
                    player.rect.top = obstacle.rect.bottom
                    player.position.y = player.rect.y
                    player.velocity.y = 0

                elif player.velocity.y > 0:
                    player.rect.bottom = obstacle.rect.top
                    player.on_ground = True
                    player.position.y = player.rect.y
                    player.velocity.y = 0

  
    def run(self):
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


        player1 = Player(1, 20, HEIGHT-20, (255, 255, 255))
        player1.add(self.all_sprites, self.players)

        end_menu = EndMenu(self.screen)

        # Gameloop mit allen update ... Funktionen
        #Gamestates benutzen statt if else
        while True:
            # Delta Time wird verwendet, um flüssige und konstante Bewegungen bei Objekten sicherzustellen
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.playing:
                self.update(self.dt)
                self.draw()
            else:
                end_menu.draw()
                pygame.display.flip()
                if  end_menu.buttons[0].is_pressed():
                    self.playing = True
                    player1.respawn()



            
            
            


gc = GameController()

gc.run()


