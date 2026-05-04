import pygame
from level import Level
from player import Player
from obstacle import Obstacle

WIDTH = 600
HEIGHT = 600

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

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)

        # Lädt das komplette Display neu
        pygame.display.flip()


    def update(self, dt):
        self.all_sprites.update(dt)
        


    def play(self):
        self.playing = True
        self.add_level(Level(1))
        self.show_level(1)

        player1 = Player(1, 100, 100, (255, 255, 255))
        player1.add(self.all_sprites, self.players)

        obstacle1 = Obstacle((255, 0, 255), 600, 20, 0, 580)
        obstacle1.add(self.all_sprites, self.obstacles )

        # Gameloop mit allen update ... Funktionen
        while self.playing:
            # Delta Time wird verwendet, um flüssige und konstante Bewegungen bei Objekten sicherzustellen
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update(self.dt)
            self.draw()
            


gc = GameController()

gc.play()


