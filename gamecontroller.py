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


        self.playing = None
        self.running = True


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
                if self.playing:
                    self.playing = False
                self.running = False

        self.input_handler.get_input(self.players.sprites()[0])

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)

        # Lädt das komplette Display neu
        pygame.display.flip()


    def update(self, dt):
        for sprite in self.all_sprites:
            if sprite in self.players:
                sprite.update(dt, self.obstacles)   # Es müssen obstacles für die Kollission übergeben werden.
            else:
                sprite.update(dt)



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

        obstacle2 = Obstacle((0, 0, 255), 100, 20, 300, 540)
        obstacle2.add(self.all_sprites, self.obstacles)

        obstacle3 = Obstacle((0, 0, 255), 100, 20, 300, 450)
        obstacle3.add(self.all_sprites, self.obstacles)

        player1 = Player(1, 100, 100, (255, 255, 255))
        player1.add(self.all_sprites, self.players)

        # Gameloop mit allen update ... Funktionen
        while self.playing:
            # Delta Time wird verwendet, um flüssige und konstante Bewegungen bei Objekten sicherzustellen
            self.dt = self.clock.tick(FPS) / 1000

            self.events()
            self.update(self.dt)
            self.draw()

            
            
            


gc = GameController()

gc.play()


