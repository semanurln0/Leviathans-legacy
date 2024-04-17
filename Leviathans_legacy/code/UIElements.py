import time

import pygame
import pygame.freetype
from pygame.sprite import Sprite


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    # returns surface with text
    font = pygame.freetype.SysFont("Helvetica", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    # UI class for any window

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        # function arguments:
        #    center_position - tuple (x, y)
        #    text - string of text to write
        #    font_size - int
        #    bg_rgb (background colour) - tuple (r, g, b)
        #    text_rgb (text colour) - tuple (r, g, b)
        #    action - the gamestate change associated with this button
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up, event):
        # Handles mouse selection, specifically hover and clicking
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        # Draws UI element
        surface.blit(self.image, self.rect)


class TextBox(Sprite):
    # UI class for any window

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb):
        # function arguments:
        #    center_position - tuple (x, y)
        #    text - string of text to write
        #    font_size - int
        #    bg_rgb (background colour) - tuple (r, g, b)
        #    text_rgb (text colour) - tuple (r, g, b)
        #    action - the gamestate change associated with this button
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )
        self.images = [default_image]

        self.rects = [
            default_image.get_rect(center=center_position),
        ]

        super().__init__()

    @property
    def image(self):
        return self.images[0]

    @property
    def rect(self):
        return self.rects[0]

    def draw(self, surface):
        # Draws UI element
        surface.blit(self.image, self.rect)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = "White"
        self.txt_color = "White"
        self.text = text
        self.font_size = 16
        self.numb_font = pygame.font.SysFont("helvetica", 14)
        self.text_font = pygame.font.SysFont("helvetica", 20)
        self.txt_surface = self.text_font.render(text, True, self.txt_color)
        self.active = False
        self.score = 1
        # Cursor declare
        self.txt_rect = self.txt_surface.get_rect()
        self.cursor = pygame.Rect(self.txt_rect.topright, (2, self.txt_rect.height + 1))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    global leftover
                    leftover += self.score
                    self.score = 0
                    self.text = ''
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    # Cursor

                    self.txt_rect.size = self.txt_surface.get_size()
                    self.cursor.topleft = self.txt_rect.topright

                    # Limit characters           -20 for border width
                    if self.txt_surface.get_width() > self.rect.w - 15:
                        self.text = self.text[:-1]

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 10))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 1)
        # Blit the  cursor
        if time.time() % 1 > 0.5 and self.active:
            # bounding rectangle of the text
            text_rect = self.txt_surface.get_rect(topleft=(self.rect.x + 5, self.rect.y + 10))

            # set cursor position
            self.cursor.midleft = text_rect.midright

            pygame.draw.rect(screen, self.color, self.cursor)

    def update(self):
        # Re-render the text.
        self.txt_surface = self.text_font.render(self.text, True, self.color)