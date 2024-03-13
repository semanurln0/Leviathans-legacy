import pygame
import pygame.freetype
from pygame.sprite import Sprite
from enum import Enum
from pygame.sprite import RenderUpdates

pygame.init()

BLUE = (26, 79, 101)
WHITE = (200, 200, 200)
RED = (100, 0, 0)
GREEN = (0, 100, 0)


class Player:
    # Our player info
    def __init__(self, score=0, lives=0, current_level=0):
        self.score = score
        self.lives = lives
        self.current_level = current_level


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

    def update(self, mouse_pos, mouse_up):
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


def main():
    game_state = GameState(0)
    pygame.init()

    info = pygame.display.Info()
    w = info.current_w
    h = info.current_h - 50
    screen = pygame.display.set_mode((w, h), pygame.SCALED | pygame.RESIZABLE)

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.MAIN_SCREEN:
            player = Player(0)
            game_state = play_level(screen, player)

        if game_state == GameState.NEXT_LEVEL:
            player.current_level += 1
            game_state = play_level(screen, player)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen):
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.MAIN_SCREEN,
    )
    quit_btn = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(start_btn, quit_btn)

    return game_loop(screen, buttons)


def play_level(screen, player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    nextlevel_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"Next level ({player.current_level + 1})",
        action=GameState.NEXT_LEVEL,
    )

    buttons = RenderUpdates(return_btn, nextlevel_btn)

    return game_loop(screen, buttons)


def game_loop(screen, buttons):
    # Handles screen
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.QUIT:
                return GameState.QUIT
        screen.fill(BLUE)


        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    MAIN_SCREEN = 1
    NEXT_LEVEL = 2


if __name__ == "__main__":
    main()
