import os
import pygame
import math
from random import choice
from Buildings import Plantation, PowerPlant, Cabins, Barracks, AbyssalOreRefinery, DefensiveDome  # Ensure these are defined

def hexagon_points(center, size):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        x = center[0] + size * math.cos(angle_rad)
        y = center[1] + size * math.sin(angle_rad)
        points.append((x, y))
    return points

class Hexagon:
    def __init__(self, center, size, color=(100, 100, 100), building=None):
        self.center = center
        self.size = size
        self.color = color
        self.points = hexagon_points(center, size)
        self.clicked = False
        self.building = building

    def draw(self, screen):
        color = (200, 0, 0) if self.clicked else self.color
        pygame.draw.polygon(screen, color, self.points)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if any(min(p[i] <= event.pos[i % 2] <= max(p[i] for p in self.points) for i in range(2)) for p in self.points):
                self.clicked = not self.clicked
                return True
        return False

class Popup:
    def __init__(self, screen, rect, bg_color=(200, 200, 200)):
        self.screen = screen
        self.rect = rect
        self.bg_color = bg_color
        self.font = pygame.font.Font(None, 24)
        self.visible = False
        self.content = ""
        self.options = []  # This will store building options
        self.selected_hexagon = None
        self.close_button_rect = pygame.Rect(self.rect.right - 30, self.rect.top, 30, 30)

    def set_building_options(self, options):
        # This method sets the building options available for creation
        self.options = options

    def update_content(self, building=None):
        if building:
            self.content = f"{type(building).__name__}: Stage {building.building_stage}"
        else:
            self.content = "Choose a building:"
        self.visible = True

    def draw(self):
        if self.visible:
            pygame.draw.rect(self.screen, self.bg_color, self.rect)
            if self.content.startswith("Choose a building:"):
                y_offset = 40
                for option in self.options:
                    text_surface = self.font.render(option['name'], True, (0, 0, 0))
                    image = pygame.transform.scale(option['image'], (50, 50))
                    self.screen.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
                    self.screen.blit(image, (self.rect.x + 150, self.rect.y + y_offset))
                    y_offset += 60
            else:
                text_surface = self.font.render(self.content, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
                self.screen.blit(text_surface, text_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.close_button_rect)
            close_text = self.font.render('X', True, (255, 255, 255))
            close_text_rect = close_text.get_rect(center=self.close_button_rect.center)
            self.screen.blit(close_text, close_text_rect)

    def handle_event(self, event):
        if not self.visible:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                self.visible = False
                return True
            if self.content.startswith("Choose a building:") and not self.selected_hexagon.building:
                index = (event.pos[1] - (self.rect.y + 40)) // 60
                if 0 <= index < len(self.options):
                    selected_building = self.options[index]['create']()  # Create building instance
                    self.selected_hexagon.building = selected_building  # Assign to hexagon
                    self.visible = False
                    return True
        return False


class OverviewUI:
    def __init__(self, screen, background_filename):
        pygame.init()
        self.screen = screen
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_path = os.path.join(base_dir, '..', 'sprites', background_filename)
        try:
            self.background = pygame.image.load(self.background_path)
        except pygame.error as e:
            print(f"Unable to load image at {self.background_path}. Error: {e}")
            raise SystemExit(e)
        self.popup = Popup(screen, pygame.Rect(150, 100, 500, 200))
        self.hexagons = self.initialize_hexagons(screen.get_width(), screen.get_height())

    def initialize_hexagons(self, screen_width, screen_height):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sprites_dir = os.path.join(base_dir, '..', 'sprites')  # Directory for sprites
        hexagons = []
        hex_size = 40
        hex_width = 2 * hex_size
        hex_height = math.sqrt(3) * hex_size
        grid_width = 3 * hex_width
        grid_height = 3 * hex_height
        start_x = (screen_width - grid_width) / 2
        start_y = (screen_height - grid_height) / 2

        building_options = [
            {'name': 'Plantation', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'), 'create': Plantation},
            {'name': 'Power Plant', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'), 'create': PowerPlant},
            {'name': 'Cabins', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'), 'create': Cabins},
            {'name': 'Barracks', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'), 'create': Barracks},
            {'name': 'Abyssal Ore Refinery', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'), 'create': AbyssalOreRefinery},
            {'name': 'Defensive Dome', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'), 'create': DefensiveDome}
        ]
        self.popup.set_building_options(building_options)

        for row in range(3):
            for col in range(3):
                x = start_x + col * hex_width * 0.75
                y = start_y + row * hex_height
                if col % 2 == 1:
                    y += hex_height / 2
                hexagon = Hexagon((x, y), hex_size)  # Start without a building
                hexagons.append(hexagon)
        return hexagons
    def load_image(self, directory, filename):
        path = os.path.join(directory, filename)
        try:
            return pygame.image.load(path)
        except pygame.error as e:
            print(f"Unable to load image at {path}. Error: {e}")
            raise SystemExit(e)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.popup.handle_event(event):  # Handle popup events first
                continue  # Skip other interactions if popup was interacted with
            for hexagon in self.hexagons:
                if hexagon.is_clicked(event):
                    if hexagon.building:
                        self.popup.update_content(hexagon.building)
                    else:
                        self.popup.update_content()
                    self.popup.selected_hexagon = hexagon  # Store reference to the hexagon for later interactions
                    self.popup.visible = True  # Show popup
                    break


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for hexagon in self.hexagons:
            hexagon.draw(self.screen)
        self.popup.draw()

def test_overview_ui():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Overview UI")
    ui = OverviewUI(screen, 'BackgroundPlaceHolder.png')

    running = True
    while running:
        events = pygame.event.get()
        ui.handle_events(events)
        ui.draw()
        pygame.display.flip()

    pygame.quit()

test_overview_ui()

