# Hier sollten alle Inputs behandelt werden. Eventuell auch custom keybindings

import pygame


class InputHandler:
    """ Converts keyboard input into actions."""

    # Später über JSON Datei laden und speichern für custom Bindings
    # Two bindings for both local players
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
        Initializes the input handler.
        Sets the default bindings
        """
        self.key_bindings = self.BINDINGS
        # Später: self.key_bindings = self.load_bindings(path)


    def set_custom_binding(self, action, key):
        """ Set own keybindings. """
        pass

    def get_input(self, players):
        """ Handles the keyboard input. """

        # Get all pressed keys
        keys = pygame.key.get_pressed()
        for player in players.sprites():
            # Different player_id values for different keybindings
            if player.player_id == 1:

                left = keys[self.key_bindings["left1"]]
                right = keys[self.key_bindings["right1"]]

                direction = 0

                # If both buttons are pressed, the direction remains at 0 so that no movement occurs
                if left and not right:
                    direction = -1
                elif not left and right:
                    direction = 1

                player.move(direction)

                if keys[self.key_bindings["jump1"]]:
                    player.jump()

            elif player.player_id == 2:
                left = keys[self.key_bindings["left2"]]
                right = keys[self.key_bindings["right2"]]

                direction = 0

                # If both buttons are pressed, the direction remains at 0 so that no movement occurs
                if left and not right:
                    direction = -1
                elif not left and right:
                    direction = 1

                player.move(direction)

                if keys[self.key_bindings["jump2"]]:
                    player.jump()
    
    def get_menuinput(self, gc):
        """ Handles the input in the menus. """
        # Noch ist es nur mit einem Klick geregelt.


        # keys = pygame.key.get_pressed()
        #
        # if keys[self.key_bindings["jump"]]:
        #     gc.playing = True
        #     return True
        # return False

    def save_bindings(self, filepath: str = "config/keybindings.json"):
        """
        Saves the new keybindings.

        TODO:
            - Keybindings vermutlich in JSON Format abspeichern und dann per load_bindings laden.
        """
        pass

    def load_bindings(self, filepath):
        """ Loads the saved keybindings from a JSON file. """
        pass