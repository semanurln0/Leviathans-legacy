import pygame
import pygame.freetype
import asyncio
from enum import Enum
from pygame.sprite import RenderUpdates
import UIElements

pygame.init()
# Colours
BLUE = (26, 79, 101)
WHITE = (200, 200, 200)
RED = (100, 0, 0)
GREEN = (0, 100, 0)


class Player:
    # Our player info
    def __init__(self):
        self.food = 0
        self.steel = 0
        self.soldiers = 0


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    MAIN_SCREEN = 1
    NEXT_LEVEL = 2


async def main():
    game_state = GameState(0)
    pygame.init()

    info = pygame.display.Info()
    w = info.current_w
    h = info.current_h - 50
    screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

    while True:
        await asyncio.sleep(0)

        if game_state == GameState.TITLE:
            game_state = title_screen(screen, game_state)

        if game_state == GameState.MAIN_SCREEN:
            game_state = play_level(screen, game_state)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen, game_state):
    title = UIElements.TextBox(
        center_position=(screen.get_width() / 2, 100),
        font_size=50,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Leviathans legacy",
    )
    start_btn = UIElements.UIElement(
        center_position=(screen.get_width() / 2, 200),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=game_state.MAIN_SCREEN,
    )
    quit_btn = UIElements.UIElement(
        center_position=(screen.get_width() / 2, 300),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=game_state.QUIT,
    )

    buttons = RenderUpdates(title, start_btn, quit_btn)
    pygame.display.flip()
    return game_loop(screen, buttons, game_state)


def play_level(screen, game_state):
    return_btn = UIElements.UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=game_state.TITLE,
    )

    nextlevel_btn = UIElements.UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Next level",
        action=game_state.QUIT,
    )

    buttons = RenderUpdates(return_btn, nextlevel_btn)

    return game_loop(screen, buttons, game_state)


def game_loop(screen, buttons, game_state):
    # Handles screen
    while True:
        return inputs(screen, buttons, game_state)


def inputs(screen, buttons, game_state):
    mouse_up = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return GameState.QUIT
        if event.type == pygame.VIDEORESIZE:
            pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_up = True
    screen.fill(BLUE)

    for button in buttons:
        ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
    buttons.draw(screen)
    pygame.display.flip()
    return game_state


asyncio.run(main())
