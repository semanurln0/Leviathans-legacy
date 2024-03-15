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

    def __init__(self, x, y, w, h, passive_rgb, active_rgb, text=''):
        self.FONT = pygame.font.Font(None, 30)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.passive_rgb = passive_rgb
        self.active_rgb = active_rgb
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.active_rgb if self.active else self.passive_rgb
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class TextBox2(Sprite):
    # UI class for any window

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        # function arguments:
        #    center_position - tuple (x, y)
        #    text - string of text to write
        #    font_size - int
        #    bg_rgb (background colour) - tuple (r, g, b)
        #    text_rgb (text colour) - tuple (r, g, b)
        #    action - the gamestate change associated with this button
        self.clicked_over = False

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
        return self.images[1] if self.clicked_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.clicked_over else self.rects[0]

    def update(self, mouse_pos, mouse_up, event):
        # Handles mouse selection, specifically hover and clicking
        if self.rect.collidepoint(mouse_pos):
            self.clicked_over = True
            if event == pygame.MOUSEBUTTONDOWN:
                return self.action
        else:
            self.clicked_over = False

    def draw(self, surface):
        # Draws UI element
        surface.blit(self.image, self.rect)