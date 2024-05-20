import os
import pygame
import math
from Buildings import Plantation, PowerPlant, Cabins, Barracks, AbyssalOreRefinery, DefensiveDome
from Buildings import BuildingFactory
from Player import mplayer

next_hexagon_id = 0


def hexagon_points(center, size):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        x = center[0] + size * math.cos(angle_rad)
        y = center[1] + size * math.sin(angle_rad)
        points.append((x, y))
    return points


def hexagon_update_action(func):
    """Decorator to log and send updates about hexagon changes based on the hexagon ID."""

    def wrapper(self, hexagon_id, selected, *args, **kwargs):
        # Call the actual function which might modify the hexagon
        result = func(self, hexagon_id, selected, *args, **kwargs)

        # After change - commit changes to server
        if selected:
            building_type = type(selected).__name__.lower().replace(' ', '_')
            building_stage = selected.building_stage + 1
            mplayer.commit_building(hexagon_id, building_type, building_stage)
            print(f"Sent update to server for Hexagon ID {hexagon_id}: {building_type}, Level: {building_stage}")

        return result

    return wrapper

def hexagon_downgrade_action(func):
    """Decorator to log and send updates about hexagon changes based on the hexagon ID."""

    def wrapper(self, hexagon_id, selected, *args, **kwargs):
        # Call the actual function which might modify the hexagon
        result = func(self, hexagon_id, selected, *args, **kwargs)

        # After change - commit changes to server
        if selected:
            if selected.building_stage > 0 :
                building_type = type(selected).__name__.lower().replace(' ', '_')
                building_stage = selected.building_stage - 1
                mplayer.commit_building(hexagon_id, building_type, building_stage)
                print(f"Sent update to server for Hexagon ID {hexagon_id}: {building_type}, Level: {building_stage}")

        return result

    return wrapper


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
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            print(f"{self.label} button clicked")
            if self.label == "Exit":
                quit()
            return True
        return False


class TopBar:
    def __init__(self, screen_width):
        self.buttons = []
        self.button_height = 40
        self.resource_height = 20
        self.total_height = self.button_height + self.resource_height
        self.screen_width = screen_width

    def draw(self, screen, mplayer):
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, self.screen_width, self.total_height))
        for button in self.buttons:
            button.draw(screen)
        resource_text = f"Food: {mplayer.food} Steel: {mplayer.steel} Energy: {mplayer.energy}"
        font = pygame.font.Font(None, 24)
        text_surface = font.render(resource_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, self.button_height + 25))

    def add_button(self, button):
        self.buttons.append(button)

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                if button.is_clicked(event):
                    return button.label
        return None


class Hexagon:
    def __init__(self, center, size, color=(100, 100, 100), building=None):
        global next_hexagon_id
        self.center = center
        self.id = next_hexagon_id
        next_hexagon_id += 1
        self.size = size
        self.color = color
        self.points = hexagon_points(center, size)
        self.clicked = False
        self.building = building

    def draw(self, screen):
        pygame.draw.polygon(screen, (200, 0, 0) if self.clicked else self.color, self.points)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if any(min(p[i] <= event.pos[i % 2] <= max(p[i] for p in self.points) for i in range(2)) for p in
                   self.points):
                self.clicked = not self.clicked
                return True
        return False


class Popup:
    def __init__(self, screen, rect, bg_color=(200, 200, 200)):
        """Initialize the Popup with a specified screen, rectangle dimensions, and background color."""
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
        """Draw the Popup with its options and interactive buttons."""
        if not self.visible:
            return

        pygame.draw.rect(self.screen, self.bg_color, self.rect)

        # Draw the building information or options list
        y_offset = 40
        image_size = (30, 30)  # Desired size of the small images

        if self.selected_hexagon and self.selected_hexagon.building:
            building = self.selected_hexagon.building
            remaining_time = building.get_remaining_upgrade_time()
            time_text = f"Time left for upgrade: {remaining_time}s" if remaining_time > 0 else "Upgrade complete or available!"
            text_surface = self.font.render(time_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 100))
            text_surface = self.font.render(f"{building.__class__.__name__} - Stage: {building.building_stage}", True, (0, 0, 0))
            self.screen.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))

            # Draw the upgrade and demolish buttons
            upgrade_text = "Upgrade" if building.upgrade_possible else "Max Level"
            upgrade_button = self.font.render(upgrade_text, True, (255, 255, 255))
            pygame.draw.rect(self.screen, (0, 200, 0), self.upgrade_button_rect)
            self.screen.blit(upgrade_button, (self.upgrade_button_rect.x + 5, self.upgrade_button_rect.y + 5))

            demolish_button = self.font.render("Demolish", True, (255, 255, 255))
            pygame.draw.rect(self.screen, (200, 0, 0), self.demolish_button_rect)
            self.screen.blit(demolish_button, (self.demolish_button_rect.x + 5, self.demolish_button_rect.y + 5))
        else:
            # Display available building options with their small images
            for index, option in enumerate(self.options):
                y_option = self.rect.y + y_offset + index * 40
                text_surface = self.font.render(option['name'], True, (0, 0, 0))
                self.screen.blit(text_surface, (self.rect.x + 50, y_option))

                # Draw the small image next to the name
                image = pygame.transform.scale(option['image'], image_size)
                self.screen.blit(image, (self.rect.x + 10, y_option))

        # Draw the close button
        close_text = self.font.render('X', True, (255, 255, 255))
        pygame.draw.rect(self.screen, (255, 0, 0), self.close_button_rect)
        self.screen.blit(close_text, (self.close_button_rect.x + 5, self.close_button_rect.y + 5))

    def handle_event(self, event):
        """Process events and perform actions like closing the popup, upgrading or demolishing buildings."""
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                self.visible = False
                return True

            if self.selected_hexagon and self.selected_hexagon.building:
                # Check if upgrade or demolish buttons were clicked
                if self.upgrade_button_rect.collidepoint(event.pos) and self.selected_hexagon.building.upgrade_possible:
                    self.log_building_change(self.selected_hexagon.id, self.selected_hexagon.building)
                    self.selected_hexagon.building.upgrade()
                    return True

                if self.demolish_button_rect.collidepoint(event.pos):
                    if self.selected_hexagon.building.building_stage > 0:
                        self.log_building_downgrade(self.selected_hexagon.id, self.selected_hexagon.building)
                        self.selected_hexagon.building.demolish()
                    else:
                        self.selected_hexagon.building = None
                    self.visible = False
                    return True

            if self.content.startswith("Choose a building:"):
                index = (event.pos[1] - (self.rect.y + 40)) // 40
                if 0 <= index < len(self.options):
                    building_type = self.options[index]['name'].replace(' ', '_').lower()
                    building = self.factory.create_building(building_type)
                    self.selected_hexagon.building = building
                    self.update_content(building)
                    return True
        return False

    @hexagon_update_action
    def log_building_change(self, hexagon_index, selected):
        """Log building changes to the server. This method is a placeholder for actual server communication logic."""
        print(f"{selected} logged for hexagon {hexagon_index}.")
    @hexagon_downgrade_action
    def log_building_downgrade(self, hexagon_index, selected):
        """Log building changes to the server. This method is a placeholder for actual server communication logic."""
        print(f"{selected} logged for hexagon {hexagon_index}.")

    def set_building_options(self, options):
        """Set the list of available building options, each with an image."""
        self.options = options

    def update_content(self, building=None):
        """Update the content of the popup based on the selected building or list available options."""
        if building:
            self.content = f"{type(building).__name__}: Stage {building.building_stage}"
        else:
            self.content = "Choose a building:"
        self.visible = True

    def update(self):
        """Update the popup content and draw it if visible."""
        if self.visible and self.selected_hexagon and self.selected_hexagon.building:
            self.selected_hexagon.building.check_upgrade()
        self.draw()


class OverviewUI:
    def __init__(self, screen, background_filename, mplayer):
        pygame.init()
        self.screen = screen
        self.mplayer = mplayer
        self.top_bar = TopBar(screen.get_width())
        self.initialize_buttons()
        self.background_filename = background_filename
        self.background = None
        self.load_background(screen.get_width(), screen.get_height())
        self.popup = Popup(screen, pygame.Rect(150, 100, 500, 400))
        self.hexagons = self.initialize_hexagons(screen.get_width(), screen.get_height())

    def initialize_buttons(self):
        labels = ['Account', 'World Map', 'Leaderboard', 'Settings', 'Help', 'Exit']
        for i, label in enumerate(labels):
            button = Button(label, pygame.Rect(10 + i * 110, 10, 100, 40), (0, 120, 150))
            self.top_bar.add_button(button)

    def initialize_hexagons(self, screen_width, screen_height):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sprites_dir = os.path.join(base_dir, '..', 'sprites')
        hexagons = []
        hex_size = 40
        spacing_factor = 1.4

        hex_width = 2 * hex_size * spacing_factor
        hex_height = math.sqrt(3) * hex_size * spacing_factor

        grid_width = 3 * hex_width * 0.75
        grid_height = 3 * hex_height

        start_x = (screen_width - grid_width) / 2
        start_y = (screen_height - grid_height) / 2

        building_options = [
            {'name': 'Plantation', 'image': self.load_image(sprites_dir, 'Plantation.png'), 'create': Plantation},
            {'name': 'powerplant', 'image': self.load_image(sprites_dir, 'PowerPlant.png'), 'create': PowerPlant},
            {'name': 'Cabins', 'image': self.load_image(sprites_dir, 'Cabins.png'), 'create': Cabins},
            {'name': 'Barracks', 'image': self.load_image(sprites_dir, 'Barracks.png'), 'create': Barracks},
            {'name': 'AbyssalOreRefinery', 'image': self.load_image(sprites_dir, 'AbyssalOreRefinery.png'),
             'create': AbyssalOreRefinery},
            {'name': 'DefensiveDome', 'image': self.load_image(sprites_dir, 'DefensiveDome.png'),
             'create': DefensiveDome}
        ]
        self.popup.set_building_options(building_options)

        for row in range(3):
            for col in range(3):
                x = start_x + col * hex_width * 0.75
                y = start_y + row * hex_height
                if col % 2 == 1:
                    y += hex_height / 2
                hexagon = Hexagon((x, y), hex_size)
                hexagons.append(hexagon)
        return hexagons

    def load_image(self, directory, filename):
        path = os.path.join(directory, filename)
        try:
            image = pygame.image.load(path)
            return pygame.transform.scale(image, (50, 50))
        except pygame.error as e:
            print(f"Unable to load image at {path}. Error: {e}")
            raise SystemExit(e)

    def load_background(self, width, height):
        """Load and scale the background image to the current screen size."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sprites_dir = os.path.join(base_dir, '..', 'sprites')
        path = os.path.join(sprites_dir, self.background_filename)
        try:
            image = pygame.image.load(path)
            self.background = pygame.transform.scale(image, (width, height))
        except pygame.error as e:
            print(f"Unable to load background image at {path}. Error: {e}")
            raise SystemExit(e)

    def handle_events(self, events):
        """Handle all events, including resizing."""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Process window resize events
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                self.top_bar.screen_width = width
                self.load_background(width, height)
                self.popup.rect = pygame.Rect(150, 100, 500, 400)  # Adjust the popup as necessary

            # Process events for the top bar first to handle any UI interactions
            self.top_bar.handle_events([event])

            # Process events for the popup if it's visible
            if self.popup.visible:
                if self.popup.handle_event(event):
                    continue  # Skip other interactions if the popup was interacted with

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

    def draw(self, mplayer):
        """Draw the entire game UI, including the background and all UI elements."""
        self.screen.blit(self.background, (0, 0))
        self.top_bar.draw(self.screen, mplayer)  # Ensure this is being called
        for hexagon in self.hexagons:
            hexagon.draw(self.screen)
        self.popup.draw()


    def get_building_in_hexes(self, mplayer):
        # Fetch data from the server, assuming data is formatted as 'id, building_type, stage'
        DataFromServer = mplayer.get_buildings()  # Example: ['1, plantation, 1', '']
        factory = BuildingFactory()  # Assume BuildingFactory can correctly interpret strings like 'plantation' to class instances.

        for data in DataFromServer:
            if data:  # Skip empty strings
                details = data.split(',')
                if len(details) == 4:  # Ensure that there are exactly 3 elements (id, building type, stage)
                    hex_id = int(details[1].strip())  # Convert ID and strip whitespace
                    building_type = details[2].strip()  # Strip whitespace from building type
                    building_stage = int(details[3].strip())  # Convert stage to integer

                    # Find the hexagon with the matching ID and set its building
                    for hexagon in self.hexagons:
                        if hexagon.id == hex_id:
                            hexagon.building = factory.create_building(building_type)
                            hexagon.building.building_stage = building_stage
                            break
                    else:
                        print(f"Invalid hexagon ID: {hex_id}")
                else:
                    print(f"Invalid building data format: {details}")


def overview_ui(mplayer):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Overview UI")
    ui = OverviewUI(screen, 'Hexagon.png', mplayer)
    ui.get_building_in_hexes(mplayer)
    clock = pygame.time.Clock()
    running = True
    data = mplayer.get_player_info()
    print(data)

    while running:
        events = pygame.event.get()
        ui.handle_events(events)
        ui.popup.update()
        ui.draw(mplayer)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Uncomment to run
# overview_ui(mplayer)
