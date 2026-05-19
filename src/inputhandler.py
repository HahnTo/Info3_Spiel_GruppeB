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

    def get_input(self, players, mode, local_player_id=1):
        """ Handles the keyboard input depending on mode."""

        for player in players.sprites():

            if mode == "online":
                if player.player_id != local_player_id:
                    # remote player is not controlled here
                    continue

                self._handle_player_input(player, mode, player.player_id)
                continue

            self._handle_player_input(player, mode, player.player_id)

    def _handle_player_input(self, player, mode, player_id):
        """Handles movement and jump for a single player."""
        # Get all pressed keys
        keys = pygame.key.get_pressed()

        # If it is running in online mode, only use binding 1. If it is running locally, both bindings are required.
        if player_id == 1 and mode == "local":
            left = keys[self.key_bindings["left1"]]
            right = keys[self.key_bindings["right1"]]
            jump = keys[self.key_bindings["jump1"]]

        elif player_id == 2 and mode == "local":
            left = keys[self.key_bindings["left2"]]
            right = keys[self.key_bindings["right2"]]
            jump = keys[self.key_bindings["jump2"]]

        elif mode == "online":
            left = keys[self.key_bindings["left1"]]
            right = keys[self.key_bindings["right1"]]
            jump = keys[self.key_bindings["jump1"]]
        else:
            return


        direction = 0
        # If both buttons are pressed, the direction remains at 0 so that no movement occurs
        if left and not right:
            direction = -1
        elif right and not left:
            direction = 1

        player.move(direction)

        # Jump
        if jump:
            player.jump()
    
    def handle_menu_input(self, menu, event):
        """ Handles the input in the menus. """

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                menu.selected_index = (menu.selected_index - 1) % len(menu.buttons)
            if event.key == pygame.K_DOWN:
                menu.selected_index = (menu.selected_index + 1) % len(menu.buttons)
            if event.key == pygame.K_RETURN:
                menu.buttons[menu.selected_index].on_click()

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