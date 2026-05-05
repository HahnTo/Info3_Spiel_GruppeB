import pygame

from inputhandler import InputHandler
from level import Level
from player import Player
from obstacle import Obstacle

WIDTH = 1080
HEIGHT = 720

TITLE = "Mole Escape"

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

        self.levels = []

        # Alle verschiedenen Sprite Gruppen initialisieren
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()


        self.playing = True


        self.input_handler = InputHandler()



    def add_level(self, level):
        self.levels.append(level)

    def show_level(self, level=1):
        try:
            self.levels[level-1].load()
        except IndexError as e:
            print(e)
            print("Level nicht vorhanden")

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


    def play(self):
        self.playing = True
        self.add_level(Level(1))
        self.show_level(1)


        frame_wall_left = Obstacle((255, 0, 0), 10, HEIGHT, -10, 0)
        frame_wall_left.add(self.all_sprites, self.obstacles)

        frame_wall_right = Obstacle((255, 0, 0), 10, HEIGHT, WIDTH, 0)
        frame_wall_right.add(self.all_sprites, self.obstacles)

        frame_floor = Obstacle((255, 0, 255), WIDTH, 20, 0, HEIGHT-20)
        frame_floor.add(self.all_sprites, self.obstacles )

        obstacle2 = Obstacle((0, 0, 255), 100, 20, 300, HEIGHT-100)
        obstacle2.add(self.all_sprites, self.obstacles)

        goal_obstacle = Obstacle((255, 0, 0), 50, 50, WIDTH-50, HEIGHT-70, True)
        goal_obstacle.add(self.all_sprites, self.obstacles)


        player1 = Player(1, 100, 100, (255, 255, 255))
        player1.add(self.all_sprites, self.players)

        # Gameloop mit allen update ... Funktionen
        while True:
            # Delta Time wird verwendet, um flüssige und konstante Bewegungen bei Objekten sicherzustellen
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.playing:
                self.update(self.dt)
                self.draw()
            else:
                self.all_sprites.empty
                self.screen.fill(BACKGROUND_COLOR)
                pygame.display.flip()



            
            
            


gc = GameController()

gc.play()


