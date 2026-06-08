import threading

import pygame

from obstacle import Obstacle
from src.inputhandler import InputHandler
from src.gamestatemanager import GameStateManager
from src.server.networkclient import NetworkClient
from src.server.server import Server
from src.states.joinloadingstate import JoinLoadingState
from src.states.menus.endmenu import EndMenu
from src.states.level import Level
from src.states.menus.multiplayermenu import MultiplayerMenu
from src.states.menus.startmenu import StartMenu

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


class GameController:
    """Initializes the game and creates the game loop"""


    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption(TITLE)

        # The tick speed is set to 60 in the game loop to limit the frame rate to 60 FPS
        self.clock = pygame.time.Clock()
        self.dt = 0

        # local or online mode
        self.game_mode = ''
        # Only initialize a network client if the mode is online.
        # self.network_client = NetworkClient() if self.game_mode == "online" else None
        self.network_client = None
        self.server = None

        self.game_state_manager = GameStateManager('start_menu')

        self.start_menu = StartMenu(self.screen, self.game_state_manager, self)
        self.multiplayer_menu = MultiplayerMenu(self.screen, self.game_state_manager, self)
        self.join_loading = None
        # self.level = Level(self.screen, self.game_state_manager, self, self.network_client)
        # Only initialize once it is known whether the game runs online or locally.
        self.level = None
        self.end_menu = EndMenu(self.screen, self.game_state_manager, self)

        self.states = {
            'start_menu': self.start_menu,
            'level': self.level ,
            'end_menu': self.end_menu,
            'multiplayer_menu':  self.multiplayer_menu,
            'join_loading': self.join_loading
        }

        self.input_handler = InputHandler()

    def start_local(self):
        self.game_mode = 'local'
        self.level = Level(self.screen, self.game_state_manager, self, None)
        self.states['level'] = self.level
        self.game_state_manager.set_state('level')


    def start_host(self):
        self.game_mode = 'online'
        self.start_server()
        self.network_client = NetworkClient()
        self.level = Level(self.screen, self.game_state_manager, self, self.network_client)
        self.states['level'] = self.level
        self.game_state_manager.set_state('level')

    def start_join(self, ip_address):
        """Called when the player wants to join an existing server.
        Shows the loading screen while the connection is established in a background thread."""
        self.game_mode = 'online'
        self.join_loading = JoinLoadingState(self.screen, self.game_state_manager, self, ip_address)
        self.states['join_loading'] = self.join_loading
        self.game_state_manager.set_state('join_loading')

    def finish_join(self):
        """Called by JoinLoadingState once the NetworkClient is connected.
        Builds the Level with the ready client and switches to it """
        self.level = Level(self.screen, self.game_state_manager, self, self.network_client)
        self.states['level'] = self.level
        self.game_state_manager.set_state('level')

    def start_server(self):
        self.server = Server()

        threading.Thread(
            target=self.server.start,
            daemon=True
        ).start()

    def events(self):
        """Reacts to all pygame.events, like keyboard input and closing the Window"""
        for event in pygame.event.get():
            # Ends the script if window gets closed
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


            self.states[self.game_state_manager.get_state()].handle_event(event)

        # if self.game_state_manager.get_state() == 'end_menu':
        #     if self.end_menu.buttons[0].is_pressed():
        #         self.game_state_manager.set_state('level')
        #         for player in self.level.players.sprites():
        #             player.respawn()

        # If it is running in online mode, the local ID is required.
        if self.game_state_manager.get_state() == 'level':
            if self.game_mode == 'local':
                self.input_handler.get_input(self.level.players, self.game_mode)
            else:
                self.input_handler.get_input(self.level.players, self.game_mode, self.level.local_id)


    def handle_horizontal_collision(self, player):
        """ Handles horizontal collisions.
            If the player is coming from the left, their position is set to the right side of the object.
            If the player is coming from the right, their position is set to the left side of the object.
        """
        #Name passt nicht so ganz weil mehr gemacht wird als Kollision checken, Player Movement wird beeinflusst
        #Wahrscheinlich Kollision und Movement Beeinflussung seperat, maybe Movement Beeinflussung dann im Player

        # Get all objects that are colliding with each other
        collider_group = pygame.sprite.spritecollide(player, self.level.obstacles, False)
        obstacles = self.level.obstacles
        for obstacle in collider_group:
            # If the obstacle is the goal, set playing to false. The game loop will then jump to the end menu.
            if obstacle.is_goal:
                self.game_state_manager.set_state('end_menu')
            elif obstacle.is_movable:
                if player.velocity.x < 0:
                    obstacle.rect.right = player.rect.left
                    obstacle.x_pos = obstacle.rect.x
                    player.rect.left = obstacle.rect.right
                    player.position.x = player.rect.x
                elif player.velocity.x > 0:
                    obstacle.rect.left = player.rect.right
                    obstacle.x_pos = obstacle.rect.x
                    player.rect.right = obstacle.rect.left
                    player.position.x = player.rect.x
            elif obstacle.is_button:
                print("Button gedrückt")
                button = obstacle
                for other in self.level.obstacles:
                    if button.button_id == other.button_id and not other.is_button:
                        other.move(200)
                        print("button gefunden")


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
        collisions = pygame.sprite.groupcollide(self.level.obstacles, self.level.obstacles, False, False)
        for movable, colliders in collisions.items():
            if movable.is_movable:
                for wall in colliders:
                    if wall != movable and not wall.is_movable:
                        if player.velocity.x > 0:
                            movable.rect.right = wall.rect.left
                            movable.x_pos = movable.rect.x
                            player.rect.right = movable.rect.left
                            player.position.x = player.rect.x
                            player.velocity.x = 0

                        elif player.velocity.x < 0:
                            movable.rect.left = wall.rect.right
                            movable.x_pos = movable.rect.x
                            player.rect.left = movable.rect.right
                            player.position.x = player.rect.x
                            player.velocity.x = 0




    def handle_vertical_collision(self, player):
        """ Handles vertical collisions.
            If the player is coming from above, their position is set to the top of the object.
            If the player is coming from below, their position is set to the bottom of the object.
        """

        # Get all objects that are colliding with each other
        collider_group = pygame.sprite.spritecollide(player, self.level.obstacles, False)
        for obstacle in collider_group:
            if obstacle.is_goal:
                self.game_state_manager.set_state('end_menu')
            #elif obstacle.is_movable:
             #   pass
            elif obstacle.is_button:
                button = obstacle
                for other in self.level.obstacles:
                    if button.button_id == other.button_id and not other.is_button:
                        other.move(200)
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

        # Game loop with the different game states. In each frame, events are checked and all elements are updated.
        while True:
            # Delta time ensures that movement and timers stay consistent regardless of the frame rate.
            self.dt = self.clock.tick(FPS) / 1000

            # Handle all events
            self.events()

            current_state = self.game_state_manager.get_state()
            first_entry = self.game_state_manager.is_first_entry()

            # Einmalige Transition um player zurückzusetzten
            if current_state == 'level' and first_entry:
                for player in self.level.players.sprites():
                    player.respawn()
                self.game_state_manager.set_first_entry(False)
            self.states[self.game_state_manager.get_state()].run(self.dt)


if __name__ == "__main__":
    gc = GameController()
    gc.run()


