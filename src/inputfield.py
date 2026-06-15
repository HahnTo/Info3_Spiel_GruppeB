import pygame

from src.inputhandler import InputHandler


class InputField:
    """ Textfield for input. """

    def __init__(self, label, font_size, position, placeholder=""):
        """ Initializes the input field with its components """
        self.label = label
        self.font_size = font_size
        self.position = position
        self.placeholder = placeholder

        self.value = ""
        self.editing = True

        self.font = pygame.font.SysFont("Arial", font_size)
        self.cursor_visible = True
        self.cursor_timer = 0

        self.input_handler = InputHandler()

    def handle_event(self, event):
        """ If it is in editing mode, it delegates the event to the input handler."""
        if not self.editing:
            return

        self.input_handler.handle_input_field(self, event)

    def get_value(self):
        """ Returns the final value if editing is over. """
        if not self.editing: return self.value

        return ""

    def draw(self, screen):
        """ Draws the complete field. """
        border_color = (0, 200, 255)

        # Field label
        label_surf = self.font.render(self.label, False, (255, 255, 255))
        label_rect = label_surf.get_rect(center=(self.position[0],
                                                  self.position[1] - 50))
        screen.blit(label_surf, label_rect)

        # text box
        box_rect = pygame.Rect(0, 0, 270, self.font_size + 16)
        box_rect.center = self.position
        pygame.draw.rect(screen, (40, 40, 40), box_rect, border_radius=6)
        pygame.draw.rect(screen, border_color, box_rect, 2, border_radius=6)

        # Text or placeholder
        display_text = self.value
        if not display_text and not self.editing:
            display_text = self.placeholder
            text_color = (100, 100, 100)
        else:
            text_color = (255, 255, 255)

        # Curser
        self.update_cursor()
        if self.editing and self.cursor_visible:
            display_text += "|"

        text_surf = self.font.render(display_text, False, text_color)
        text_rect = text_surf.get_rect(midleft=(box_rect.left + 10,
                                                 box_rect.centery))
        screen.blit(text_surf, text_rect)

    def update_cursor(self):
        """ Makes the cursor blink ca every half second"""
        if self.editing:
            self.cursor_timer += 1
            if self.cursor_timer >= 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
        else:
            self.cursor_visible = True
            self.cursor_timer = 0