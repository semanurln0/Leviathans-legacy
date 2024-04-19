import os
import pygame
import math


# Helper function to calculate hexagon vertices
def hexagon_points(center, size):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        x = center[0] + size * math.cos(angle_rad)
        y = center[1] + size * math.sin(angle_rad)
        points.append((x, y))
    return points


class Popup:
    def __init__(self, screen, rect, bg_color=(200, 200, 200), text="Popup"):
        self.screen = screen
        self.rect = rect
        self.bg_color = bg_color
        self.text = text
        self.font = pygame.font.Font(None, 24)
        self.visible = False

    def draw(self):
        if not self.visible:
            return
        # Draw the background of the popup
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        # Draw the text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)
        # Draw the exit button
        exit_button_rect = pygame.Rect(self.rect.right - 40, self.rect.top + 10, 30, 30)
        pygame.draw.rect(self.screen, (255, 0, 0), exit_button_rect)
        self.screen.blit(self.font.render('X', True, (255, 255, 255)), exit_button_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.visible:
            exit_button_rect = pygame.Rect(self.rect.right - 40, self.rect.top + 10, 30, 30)
            if exit_button_rect.collidepoint(event.pos):
                self.visible = False  # Close the popup
                return True
        return False

    def show(self):
        self.visible = True


class Hexagon:
    def __init__(self, center, size, color=(100, 100, 100)):
        self.center = center
        self.size = size
        self.color = color
        self.points = hexagon_points(center, size)
        self.clicked = False  # Keep track of clicked state

    def draw(self, screen):
        color = (200, 0, 0) if self.clicked else self.color
        pygame.draw.polygon(screen, color, self.points)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is within the bounding box for a preliminary check
            min_x = min([p[0] for p in self.points])
            max_x = max([p[0] for p in self.points])
            min_y = min([p[1] for p in self.points])
            max_y = max([p[1] for p in self.points])
            if min_x <= event.pos[0] <= max_x and min_y <= event.pos[1] <= max_y:
                # To accurately check if the point is inside the hexagon, a more complex point-in-polygon algorithm is needed.
                # For simplicity, we're using the bounding box which is not 100% accurate.
                self.clicked = not self.clicked
                return True
        return False


class Button:
    def __init__(self, label, rect, color):
        self.label = label
        self.rect = rect
        self.color = color
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        label_surface = self.font.render(self.label, True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=self.rect.center)
        screen.blit(label_surface, label_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print(f"{self.label} button clicked")
                return True
        return False


class TopBar:
    def __init__(self, screen_width):
        self.buttons = []
        self.height = 60
        self.screen_width = screen_width

    def add_button(self, button):
        self.buttons.append(button)

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, self.screen_width, self.height))
        for button in self.buttons:
            button.draw(screen)

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                if button.is_clicked(event):
                    # Placeholder for future functionality
                    pass


class OverviewUI:
    def __init__(self, screen, background_filename):
        pygame.init()
        self.screen = screen
        self.font = pygame.font.Font(None, 24)

        # Load and scale the background image
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_path = os.path.join(base_dir, '..', 'sprites', background_filename)
        try:
            self.background = pygame.image.load(self.background_path)
        except pygame.error as e:
            print(f"Unable to load image at {self.background_path}. Error: {e}")
            raise SystemExit(e)
        self.background = pygame.transform.scale(self.background, (800, 600))

        # Initialize the top bar and buttons
        self.top_bar = TopBar(self.screen.get_width())
        button_labels = ['Account', 'World Map', 'Leaderboard', 'Settings', 'Help']
        button_colors = [(100, 100, 200), (100, 200, 100), (200, 100, 100), (100, 200, 200), (200, 200, 100)]
        button_width = 100
        button_height = 40
        button_margin = 20
        x_start = (self.screen.get_width() - (button_width + button_margin) * len(button_labels) + button_margin) // 2

        # Initialize The Pop Ups 
        self.popup = Popup(screen, pygame.Rect(150, 100, 500, 300), text="Building Information")

        for i, label in enumerate(button_labels):
            rect = pygame.Rect(x_start + i * (button_width + button_margin), button_margin, button_width, button_height)
            button = Button(label, rect, button_colors[i])
            self.top_bar.add_button(button)

        # Hex grid settings
        self.hex_size = 50
        self.grid_columns = 5
        self.grid_rows = 5
        self.hexagons = []  # Store hexagons

        # Calculate the total grid width and height
        hex_width = self.hex_size * 2
        hex_height = math.sqrt(3) * self.hex_size
        grid_width = (hex_width * 3 / 4) * self.grid_columns + self.hex_size / 4
        grid_height = hex_height * self.grid_rows
        start_x = (self.screen.get_width() - grid_width) / 2 + self.hex_size
        start_y = (self.screen.get_height() - grid_height) / 2 + hex_height / 2

        # Initialize grid positions
        for row in range(self.grid_rows):
            for col in range(self.grid_columns):
                center_x = start_x + col * (hex_width * 3 / 4)
                center_y = start_y + row * hex_height
                if col % 2 == 1:
                    center_y += hex_height / 2
                hexagon = Hexagon((center_x, center_y), self.hex_size)
                self.hexagons.append(hexagon)

    def handle_events(self, events):
        self.top_bar.handle_events(events)
        for event in events:
            if self.popup.handle_event(event):
                continue  # Skip other interactions if popup is interacting
            for hexagon in self.hexagons:
                if hexagon.is_clicked(event):
                    print(f"Clicked on hexagon at {hexagon.center}")
                    self.popup.show()

    def draw(self):
        # Draw background, top bar, hexagons
        self.screen.blit(self.background, (0, 0))
        self.top_bar.draw(self.screen)
        for hexagon in self.hexagons:
            hexagon.draw(self.screen)
        self.popup.draw()  # Draw the popup
        pygame.display.flip()
        pygame.display.flip()


def test_overview_ui():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Overview UI")
    overview_ui = OverviewUI(screen, 'BackgroundPlaceHolder.png')

    running = True
    while running:
        events = pygame.event.get()
        overview_ui.handle_events(events)
        overview_ui.draw()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


# Uncomment to test
#test_overview_ui()
