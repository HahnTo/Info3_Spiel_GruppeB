# Hier sollten alle Inputs behandelt werden. Eventuell auch custom keybindings

import pygame


class InputHandler:
    """
    Setzt die Eingaben über die Tastatur in Aktionen um
    """

    # Später über JSON Datei laden und speichern für custom Bindings
    BINDINGS = {
        "left1": pygame.K_a,
        "right1": pygame.K_d,
        "jump1": pygame.K_w,
        "left2": pygame.K_LEFT,
        "right2": pygame.K_RIGHT,
        "jump2": pygame.K_UP
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

    def get_input(self, players):
        """
        Behandelt die Eingabe der Tastatur
        """
        keys = pygame.key.get_pressed()
        for player in players.sprites():
            if player.player_id == 1:
                if keys[self.key_bindings["left1"]]:
                    player.move(-1)
                if keys[self.key_bindings["right1"]]:
                    player.move(1)
                if keys[self.key_bindings["jump1"]]:
                    player.jump()
            else:
                if keys[self.key_bindings["left2"]]:
                    player.move(-1)
                if keys[self.key_bindings["right2"]]:
                    player.move(1)
                if keys[self.key_bindings["jump2"]]:
                    player.jump()
    
    def get_menuinput(self, gc):

        keys = pygame.key.get_pressed()

        if keys[self.key_bindings["jump"]]:
            gc.playing = True
            return True
        return False
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