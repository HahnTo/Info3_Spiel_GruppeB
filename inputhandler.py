# Hier sollten alle Inputs behandelt werden. Eventuell auch custom keybindings

import pygame


class InputHandler:
    """
    Setzt die Eingaben über die Tastatur in Aktionen um
    """

    # Später über JSON Datei laden und speichern für custom Bindings
    BINDINGS = {
        "left": pygame.K_a,
        "right": pygame.K_d,
        "jump": pygame.K_w,
        "duck": pygame.K_s
    }

    def __init__(self):
        """
        Initialisiert den Input Handler.
        Setzt die default Bindings
        """
        self.key_bindings = self.BINDINGS
        # Später: self.key_bindings = self.load_bindings(path)


    def set_custom_binding(self, action, key):
        """
        Eigene Keybinds setzen
        """
        pass

    def get_input(self, player):
        """
        Behandelt die Eingabe der Tastatur
        """
        keys = pygame.key.get_pressed()

        if keys[self.key_bindings["left"]]: player.move(-1);
        if keys[self.key_bindings["right"]]: player.move(1);
        if keys[self.key_bindings["jump"]]: player.jump();

       # if keys[self.key_bindings["duck"]]: player.duck();
        else: player.stand_up()

    def save_bindings(self, filepath: str = "config/keybindings.json"):
        """
        Speichert die neu gesetzten Bindings.

        TODO:
            - Keybindings vermutlich in JSON Format abspeichern und dann per load_bindings laden.
        """
        pass

    def load_bindings(self, filepath):
        """
        Lädt die Keybindings von einer JSON Datei
        """
        pass