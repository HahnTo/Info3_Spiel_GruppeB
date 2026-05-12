import pygame
from pygame import Vector2
from typing import Literal



class Player(pygame.sprite.Sprite):
    """
    Erstellt die Spieler in Mole Escape.
    Die Physik, Input und Bewegung wird hier implementiert.
    """

    # Größe des Spielers
    WIDTH = 30
    HEIGHT = 40

    # Physik
    GRAVITY = 0.8
    MOVE_SPEED = 5.0
    JUMP_HEIGHT = -12.0 # Muss negativ sein, weil bei PyGames das Fenster oben links bei (0, 0) anfängt, also y ins negative geht.
    DUCK_HEIGHT = HEIGHT * 0.8


    player_id = 1

    def __init__(self, start_x, start_y, color):
        """
        Initialisiert den Spieler.

        Setzt Startpunkt und Farbe bei erstem Level.
        Bis die Texturen fertig sind, werden einfache Farben verwendet.
        """
        super().__init__()

        self.start_x = start_x
        self.start_y = start_y

        self.player_id = Player.player_id
        Player.player_id += 1

        # Das Rechteck und die Farbe für den Player
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = self.image.get_rect(topleft=(self.WIDTH, self.HEIGHT))
        self.image.fill(color)

        # Setzt den Player auf seinen Spawn
        self.rect.x = start_x
        self.rect.y = start_y
        # self.position ist die echte Position, self.rect.x und y sind nur für Kollision und zeichnen notwendig
        self.position = Vector2(start_x, start_y)


        # velocity ist die Geschwindigkeit des Spielers in X- und Y-Richtung, wird pro Frame auf die aktuelle Position addiert.
        self.velocity = Vector2(0,0)

        # States
        self.on_ground = False
        self.is_duck = False
        self.is_alive = True
        self.facing_right = True # Wird später für die Texturen und Interaktion mit Gegenständen o.ä. gebraucht.


    def move(self, direction: Literal[-1, 1]):
        """
        Bewegt den Spieler beim Aufruf der Funktion.
        direction: links = -1, rechts = 1
        """

        if not self.is_alive:
            return

        # Multiplikation mit direction, um velocity.x positiv oder negativ zu erhalten
        self.velocity.x = direction * self.MOVE_SPEED

        if direction == 1:
            self.facing_right = True
        else:
            self.facing_right = False


    def jump(self):
        """
        Der Spieler springt, wenn er auf dem Boden ist
        """

        if not self.is_alive:
            return

        if self.on_ground:
            self.velocity.y = self.JUMP_HEIGHT
            self.on_ground = False

    def update(self, dt, gc):
        """
                Position des Spielers updaten
        """

        if not self.is_alive:
            return

        # Die Fallgeschwindigkeit(velocity.y) wird jeden Frame leicht erhöht, dadurch entsteht die "Physik"
        if not self.on_ground:
            self.velocity.y += self.GRAVITY

        # Horizontale Bewegung
        self.position.x += self.velocity.x
        self.rect.x = int(self.position.x)
        gc.check_horizontal_collision(self)

        # Vertikale Bewegung
        self.position.y += self.velocity.y
        self.rect.y = int(self.position.y)

        self.on_ground = False
        gc.check_vertical_collision(self)

        # Bewegung in x Richtung zurücksetzen

        self.velocity.x = 0


    def die(self):
        """
        Setzt Spieler tot.
        """
        self.is_alive = False
        self.velocity = Vector2((0,0))


    def respawn(self):
        """
        Spieler wird zurückgesetzt und auf den Spawn teleportiert.
        """
        self.is_alive = True
        self.facing_right = True
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.position = Vector2(self.start_x, self.start_y)
        self.velocity.x = 0
        self.velocity.y = 0
