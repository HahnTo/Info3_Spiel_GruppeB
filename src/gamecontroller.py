import threading
import pygame

from src.config import WIDTH, HEIGHT, TITLE, FPS
from src.inputhandler import InputHandler
from src.gamestatemanager import GameStateManager
from src.server.networkclient import NetworkClient
from src.server.server import Server
from src.states.loadings.joinloadingstate import JoinLoadingState
from src.states.loadings.waitingstate import WaitingState
from src.states.menus.endmenu import EndMenu
from src.states.level import Level
from src.states.menus.levechoosermenu import LevelChooserMenu
from src.states.menus.multiplayermenu import MultiplayerMenu
from src.states.menus.startmenu import StartMenu


class GameController:
    """initializes the game and creates the game loop"""



    def __init__(self):

        pygame.init()
        pygame.font.init()

        # initializes the window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        # the tick speed is set to 60 in the game loop to limit the frame rate to 60 FPS
        self.clock = pygame.time.Clock()
        self.dt = 0

        #sets a short pause when a player dies
        self.pause_timer = 0.0
        self.pause_duration = 1.5
        self.is_paused = False
        self.pause_callback = None

        # local or online mode
        self.game_mode = ''
        # Only initialize a network client if the mode is online.
        self.network_client = None
        self.server = None

        self.game_state_manager = GameStateManager('start_menu')

        self.start_menu = StartMenu(self.screen, self.game_state_manager, self)
        self.level_chooser = LevelChooserMenu(self.screen, self.game_state_manager, self)
        self.multiplayer_menu = MultiplayerMenu(self.screen, self.game_state_manager, self)
        self.waiting_state = None
        self.join_loading_state = None

        # only initialize once it is known whether the game runs online or locally
        self.level = None
        self.end_menu = EndMenu(self.screen, self.game_state_manager, self)

        #create a dictionary for the different gamestates
        self.states = {
            'start_menu': self.start_menu,
            'level_chooser': self.level_chooser,
            'level': self.level ,
            'end_menu': self.end_menu,
            'multiplayer_menu':  self.multiplayer_menu,
            'waiting_for_client': self.waiting_state,
            'join_loading': self.join_loading_state
        }

        self.input_handler = InputHandler()


    def start_local(self, level_id):
        """ starts the local game"""

        self.game_mode = 'local'
        self.level = Level(self.screen, self.game_state_manager, self, level_id)
        self.states['level'] = self.level
        self.game_state_manager.set_state('level')


    def start_online(self, level_id):
        """ starts the online game """

        self.network_client.send({"type": "game_start"})
        self.level = Level(self.screen, self.game_state_manager, self, level_id, self.network_client)
        self.states['level'] = self.level
        self.game_state_manager.set_state('level')


    def start_host(self):
        """ starts the server and shows the waiting screen till the other client connects"""

        self.game_mode = 'online'
        self.start_server()
        self.network_client = NetworkClient()
        self.go_to_waiting_state()


    def start_join(self, ip_address):
        """ called when the player wants to join a server.
            Shows the loading screen while the connection is established in a background thread"""

        self.game_mode = 'online'
        self.join_loading_state = JoinLoadingState(self.screen, self.game_state_manager, self, ip_address)
        self.states['join_loading'] = self.join_loading_state
        self.game_state_manager.set_state('join_loading')


    def go_to_waiting_state(self):
        """ shows the waiting screen"""

        self.waiting_state = WaitingState(self.screen, self.game_state_manager, self)
        self.states['waiting_for_client'] = self.waiting_state
        self.game_state_manager.set_state('waiting_for_client')


    def restart_game(self):
        """ restarts the game. Decides between local and online restart"""

        self.is_paused = False
        if self.game_mode == 'online':
            self.restart_online()
        else:
            self.level.reset()
            self.game_state_manager.set_state('level')


    def restart_online(self, send=True):
        """ restarts the online game and sends the message to the other client """

        if send:
            self.network_client.send({"type": "restart"})
        self.clear_network_queue()
        self.level.reset()
        self.game_state_manager.set_state('level')


    def clear_network_queue(self):
        """empties the recv_queue so old game_over/state packages don't immediately
        terminate the new level instance"""

        if self.network_client:
            while self.network_client.get_update() is not None:
                pass


    def start_server(self):
        """ starts the Server with a new thread"""

        self.server = Server()

        threading.Thread(
            target=self.server.start,
            daemon=True
        ).start()


    def disconnect(self):
        """ closes the connection of the network_client and shuts down the Server.
            Resets the state to start_menu"""

        if self.network_client:
            try:
                self.network_client.socket.close()
            except Exception as e:
                print(f"Fehler beim Disconnect: {e}")
            self.network_client = None

        if self.server:
            self.server.shutdown()  # ← neu
            self.server = None

        self.game_mode = 'local'
        self.game_state_manager.set_state('start_menu')


    def events(self):
        """reacts to all pygame.events, like keyboard input and closing the window"""

        for event in pygame.event.get():
            # Ends the script if window gets closed
            if event.type == pygame.QUIT:
                self.shutdown()

            self.states[self.game_state_manager.get_state()].handle_event(event)

        # if it is running in online mode, the local ID is required
        if self.game_state_manager.get_state() == 'level' and not self.level.is_menu_paused:
            if self.game_mode == 'local':
                self.input_handler.get_input(self.level.players, self.game_mode)
            else:
                self.input_handler.get_input(self.level.players, self.game_mode, self.level.local_id)


    def handle_horizontal_collision(self, player):
        """ Handles horizontal collisions.
            If the player is coming from the left, their position is set to the right side of the object.
            If the player is coming from the right, their position is set to the left side of the object."""

        # Get all objects that are colliding with each other
        collider_group = pygame.sprite.spritecollide(player, self.level.obstacles, False)

        for obstacle in collider_group:
            # If the obstacle is the goal, set playing to false. The game loop will then jump to the end menu.
            if obstacle.is_goal:
                if self.both_players_in_goal():
                    self.trigger_goal()

            # If the obstacle is deadly, trigger the death und restart the level.
            elif obstacle.is_deadly:
                self.trigger_death()

            #if the obstacle is movable, update its rects position to that of the player
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

            # if the obstacle is a button, check which other obstacles have the same id and move them
            elif obstacle.is_button:
                print("Button gedrückt")
                button = obstacle
                for other in self.level.obstacles:
                    if button.button_id == other.button_id and not other.is_button:
                        other.move(200)
                        print("button gefunden")

            #if the obstacle is a default platform, set the players rects position to that of the obstacles
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

         #check if moving obstacles collide with other obstacles so they stop moving when being pushed against a wall
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
            If the player is coming from below, their position is set to the bottom of the object."""

        # Get all objects that are colliding with each other, same collisions as horizontal collision
        collider_group = pygame.sprite.spritecollide(player, self.level.obstacles, False)
        for obstacle in collider_group:
            if obstacle.is_goal:
                if self.both_players_in_goal():
                    self.trigger_goal()
            elif obstacle.is_deadly:
                self.trigger_death()
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


    def both_players_in_goal(self):
        """ Returns true if both players are colliding with goal obstacles. Otherwise, it returns false"""

        goal_rects = [o.rect for o in self.level.obstacles if o.is_goal]

        if len(goal_rects) == 1:
            return all(
                any(p.rect.colliderect(g) for g in goal_rects)
                for p in self.level.players
            )
        elif len(goal_rects) == 2:
            p1, p2 = self.level.players
            g1, g2 = goal_rects

            return (
                    (p1.rect.colliderect(g1) and p2.rect.colliderect(g2))
                    or
                    (p1.rect.colliderect(g2) and p2.rect.colliderect(g1))
            )
        else:
            return False


    def trigger_goal(self, send_to_server=True):
        """ Called when any player reaches the goal."""

        self.level.stop_timer()
        self.end_menu.build_menu(self.level.level_id, self.level.timer)
        if send_to_server and self.network_client is not None:
            self.network_client.send({"type": "game_over"})
        self.game_state_manager.set_state('end_menu')


    def trigger_death(self, send_to_server=True):
        """ Starts the pause after the collision and sends the message to the other client. """

        if send_to_server and self.network_client is not None:
            self.network_client.send({"type": "died"})
        self.start_pause_after_death(callback=self.restart_game)


    def start_pause_after_death(self, callback=None):
        """ Starts a short pause."""

        if self.is_paused:  # only one at a time
            return
        self.pause_timer = 0.0
        self.is_paused = True
        self.pause_callback = callback


    def run(self):
        """ This is the main function.
            It runs the game loop.
            It switches between different game states."""

        # Game loop with the different game states. In each frame, events are checked and all elements are updated.
        while True:
            # Delta time ensures that movement and timers stay consistent regardless of the frame rate.
            self.dt = self.clock.tick(FPS) / 1000

            # Handle all events
            self.events()

            current_state = self.game_state_manager.get_state()
            first_entry = self.game_state_manager.is_first_entry()

            # If it's the first entry in the level, it needs to be reset
            if current_state == 'level' and first_entry:
                self.level.reset()
                self.game_state_manager.set_first_entry(False)

            # Checks if the pause is active
            if self.is_paused:
                self.pause_timer += self.dt
                if self.pause_timer >= self.pause_duration:
                    self.is_paused = False
                    if self.pause_callback:
                        self.pause_callback()
            # Always run the current state.
            self.states[self.game_state_manager.get_state()].run(self.dt)


    def shutdown(self):
        """ Closes all connections and quit the game. """

        if self.network_client:
            try:
                self.network_client.socket.close()
            except Exception as e:
                print(f"Fehler beim Disconnect: {e}")
            self.network_client = None

        if self.server:
            self.server.shutdown()
            self.server = None

        pygame.quit()
        exit()


if __name__ == "__main__":
    gc = GameController()
    gc.run()


