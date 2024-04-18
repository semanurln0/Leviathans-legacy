import pygame
import pygame.freetype
from enum import Enum
from pygame.sprite import RenderUpdates
import UIElements
import socket

pygame.init()
# Colours
BLUE = (26, 79, 101)
WHITE = (200, 200, 200)
RED = (100, 0, 0)
GREEN = (0, 100, 0)
BLACK = (0, 0, 0)


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    MAIN_SCREEN = 1
    NEXT_LEVEL = 2


clock = pygame.time.Clock()


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8000
    # establish connection with server
    client.connect((server_ip, server_port))
    game_state = GameState(0)
    pygame.init()

    info = pygame.display.Info()
    w = info.current_w
    h = info.current_h - 50
    screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

    while True:
        pygame.key.set_repeat(200, 25)
        if game_state == GameState.TITLE:
            game_state = title_screen(screen, game_state)

        if game_state == GameState.MAIN_SCREEN:
            game_state = play_level(screen, game_state)

        if game_state == GameState.QUIT:
            client.close()
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
    login_box = UIElements.InputBox(115, 170, 250, 36, "Enter your username")

    buttons = RenderUpdates(title, start_btn, quit_btn)
    inputboxes = [login_box]
    return inputs(screen, buttons, inputboxes, game_state)


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
    inputboxes = []

    return inputs(screen, buttons, inputboxes, game_state)


def game_loop(screen, buttons, inputboxes, game_state):
    # Handles screen
    while True:
        return inputs(screen, buttons, inputboxes, game_state)


def inputs(screen, buttons, inputboxes, game_state):
    previous_state = game_state
    while True:
        screen.fill(BLUE)
        mouse_up = False
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up, event)
                if ui_action is not None:
                    return ui_action
            for box in inputboxes:
                box.handle_event(event)

        for box in inputboxes:
            box.update()

        for box in inputboxes:
            box.draw(screen)

        buttons.draw(screen)
        pygame.display.update()
        clock.tick(30)
        if previous_state == game_state:
            pass
        else:
            return game_state


main()
