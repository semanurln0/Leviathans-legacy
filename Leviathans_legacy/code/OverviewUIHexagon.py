import os
import pygame
import math
from random import choice
from Buildings import Plantation, PowerPlant, Cabins, Barracks, AbyssalOreRefinery, \
    DefensiveDome  # Ensure these are defined
from Buildings import BuildingFactory
from Player import player1


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
        self.button_height = 40  # Height of buttons
        self.resource_height = 20  # Height for resource display
        self.total_height = self.button_height + self.resource_height
        self.screen_width = screen_width

    def draw(self, screen):
        # Draw the background for the top bar
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, self.screen_width, self.total_height))
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
        # Display resources below buttons
        resource_text = f"Food: {player1.food}  Steel: {player1.steel}  Energy: {player1.energy}"
        font = pygame.font.Font(None, 24)
        text_surface = font.render(resource_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, self.button_height + 25))  # Position the text just below the buttons

    def add_button(self, button):
        # Ensure buttons are placed within the button area
        button.rect.y = 10  # Adjust y-position of buttons if needed
        self.buttons.append(button)

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                if button.is_clicked(event):
                    pass


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
            if any(min(p[i] <= event.pos[i % 2] <= max(p[i] for p in self.points) for i in range(2)) for p in
                   self.points):
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
        self.options = []
        self.selected_hexagon = None
        self.close_button_rect = pygame.Rect(self.rect.right - 30, self.rect.top, 30, 30)
        self.upgrade_button_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 120, 100, 30)
        self.demolish_button_rect = pygame.Rect(self.rect.x + 120, self.rect.y + 120, 100, 30)
        self.factory = BuildingFactory()

    def draw(self):
        if not self.visible:
            return
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        y_offset = 40
        if self.selected_hexagon and self.selected_hexagon.building:
            building = self.selected_hexagon.building
            remaining_time = building.get_remaining_upgrade_time()
            time_text = f"Time left for upgrade: {remaining_time}s" if remaining_time > 0 else "Upgrade complete or available!"
            text_surface = self.font.render(time_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 100))
        if self.selected_hexagon and self.selected_hexagon.building:
            building = self.selected_hexagon.building
            text_surface = self.font.render(f"{building.__class__.__name__} - Stage: {building.building_stage}", True,
                                            (0, 0, 0))
            self.screen.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
            upgrade_text = "Upgrade" if building.upgrade_possible else "Max Level"
            upgrade_button = self.font.render(upgrade_text, True, (255, 255, 255))
            pygame.draw.rect(self.screen, (0, 200, 0), self.upgrade_button_rect)
            self.screen.blit(upgrade_button, (self.upgrade_button_rect.x + 5, self.upgrade_button_rect.y + 5))
            demolish_button = self.font.render("Demolish", True, (255, 255, 255))
            pygame.draw.rect(self.screen, (200, 0, 0), self.demolish_button_rect)
            self.screen.blit(demolish_button, (self.demolish_button_rect.x + 5, self.demolish_button_rect.y + 5))
        else:
            for option in self.options:
                text_surface = self.font.render(option['name'], True, (0, 0, 0))
                self.screen.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += 60

        close_text = self.font.render('X', True, (255, 255, 255))
        pygame.draw.rect(self.screen, (255, 0, 0), self.close_button_rect)
        self.screen.blit(close_text, (self.close_button_rect.x + 5, self.close_button_rect.y + 5))

    def handle_event(self, event):
        if not self.visible:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                self.visible = False
                return True
            if self.selected_hexagon and self.selected_hexagon.building:
                if self.upgrade_button_rect.collidepoint(event.pos) and self.selected_hexagon.building.upgrade_possible:
                    self.selected_hexagon.building.upgrade()
                    return True
                if self.demolish_button_rect.collidepoint(event.pos):
                    if self.selected_hexagon.building.building_stage > 0:
                        self.selected_hexagon.building.demolish()
                    else:
                        self.selected_hexagon.building = None
                    self.visible = False
                    return True
            if self.content.startswith("Choose a building:"):
                index = (event.pos[1] - (self.rect.y + 40)) // 30
                if 0 <= index < len(self.options):
                    building_type = self.options[index]['name'].replace(' ', '_').lower()
                    building = self.factory.create_building(building_type)
                    self.selected_hexagon.building = building
                    self.update_content(building)
                    return True
        return False

    def set_building_options(self, options):
        # Update to pass the actual type name expected by the factory
        self.options = options

    def update_content(self, building=None):
        if building:
            self.content = f"{type(building).__name__}: Stage {building.building_stage}"
        else:
            self.content = "Choose a building:"
        self.visible = True

    def update(self):
        # Call this method in the game loop to continuously update the popup
        if self.visible and self.selected_hexagon and self.selected_hexagon.building:
            self.selected_hexagon.building.check_upgrade()
            self.draw()


class OverviewUI:
    def __init__(self, screen, background_filename):
        pygame.init()
        self.screen = screen
        self.top_bar = TopBar(screen.get_width())
        self.initialize_buttons()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_path = os.path.join(base_dir, '..', 'sprites', background_filename)
        try:
            self.background = pygame.image.load(self.background_path)
        except pygame.error as e:
            print(f"Unable to load image at {self.background_path}. Error: {e}")
            raise SystemExit(e)
        self.popup = Popup(screen, pygame.Rect(150, 100, 500, 200))
        self.hexagons = self.initialize_hexagons(screen.get_width(), screen.get_height())

    def initialize_buttons(self):
        labels = ['Account', 'World Map', 'Leaderboard', 'Settings', 'Help']
        for i, label in enumerate(labels):
            button = Button(label, pygame.Rect(10 + i * 110, 10, 100, 40), (0, 120, 150))
            self.top_bar.add_button(button)

    def initialize_hexagons(self, screen_width, screen_height):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sprites_dir = os.path.join(base_dir, '..', 'sprites')  # Directory for sprites
        hexagons = []
        hex_size = 40  # The radius of a hexagon
        spacing_factor = 1.4  # Increase this factor to increase spacing

        # Calculate the full width and height of each hexagon including spacing
        hex_width = 2 * hex_size * spacing_factor
        hex_height = math.sqrt(3) * hex_size * spacing_factor

        # Calculate grid width and height based on hex dimensions
        grid_width = 3 * hex_width * 0.75  # Adjusting horizontal spacing
        grid_height = 3 * hex_height  # Adjusting vertical spacing

        start_x = (screen_width - grid_width) / 2
        start_y = (screen_height - grid_height) / 2

        building_options = [
            {'name': 'Plantation', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'), 'create': Plantation},
            {'name': 'Power Plant', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'), 'create': PowerPlant},
            {'name': 'Cabins', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'), 'create': Cabins},
            {'name': 'Barracks', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'), 'create': Barracks},
            {'name': 'Abyssal Ore Refinery', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'),
             'create': AbyssalOreRefinery},
            {'name': 'Defensive Dome', 'image': self.load_image(sprites_dir, 'SimpleBuilding.png'),
             'create': DefensiveDome}
        ]
        self.popup.set_building_options(building_options)

        for row in range(3):
            for col in range(3):
                x = start_x + col * hex_width * 0.75
                y = start_y + row * hex_height
                if col % 2 == 1:
                    y += hex_height / 2  # Offset for odd columns to align hexagons
                hexagon = Hexagon((x, y), hex_size)
                hexagons.append(hexagon)
        return hexagons

    def load_image(self, directory, filename):
        path = os.path.join(directory, filename)
        try:
            image = pygame.image.load(path)
            return pygame.transform.scale(image, (50, 50))  # Scale images for display in popup
        except pygame.error as e:
            print(f"Unable to load image at {path}. Error: {e}")
            raise SystemExit(e)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Process events for the top bar first to handle any UI interactions
            self.top_bar.handle_events([event])  # Pass a list with the current event only

            # Process events for the popup if it's visible
            if self.popup.visible:
                if self.popup.handle_event(event):
                    continue  # Skip other interactions if popup was interacted with

            # Process hexagon clicks only if the popup is not interacting
            for hexagon in self.hexagons:
                if hexagon.is_clicked(event):
                    self.popup.selected_hexagon = hexagon
                    self.popup.visible = True
                    if hexagon.building:
                        self.popup.update_content(hexagon.building)
                    else:
                        self.popup.update_content()
                    break

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.top_bar.draw(self.screen)  # Ensure this is being called
        for hexagon in self.hexagons:
            hexagon.draw(self.screen)
        self.popup.draw()


def test_overview_ui():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Overview UI")
    ui = OverviewUI(screen, 'BackgroundPlaceHolder.png')
    clock = pygame.time.Clock()

    running = True
    while running:
        events = pygame.event.get()
        ui.handle_events(events)
        ui.popup.update()
        ui.draw()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# test_overview_ui()
[]