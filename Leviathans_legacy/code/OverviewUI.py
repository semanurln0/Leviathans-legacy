import os
import pygame

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
        
        # Grid settings for building placeholders
        self.square_size = 50
        self.spacing = self.square_size  # Space between squares
        self.grid_columns = 5
        self.grid_rows = 5  # Adjusted to 5x5 for a center piece
        self.building_slots = []  # Store rectangles for building slots
        
        # Calculate the total grid width and height
        total_grid_width = (self.square_size + self.spacing) * self.grid_columns - self.spacing
        total_grid_height = (self.square_size + self.spacing) * self.grid_rows - self.spacing
        
        # Calculate the starting x and y positions to center the grid
        start_x = (self.screen.get_width() - total_grid_width) // 2
        start_y = (self.screen.get_height() - total_grid_height) // 2
        
        # Initialize grid positions
        for row in range(self.grid_rows):
            for col in range(self.grid_columns):
                x = start_x + col * (self.square_size + self.spacing)
                y = start_y + row * (self.square_size + self.spacing)
                rect = pygame.Rect(x, y, self.square_size, self.square_size)
                self.building_slots.append({'rect': rect, 'clicked': False})

        # Top bar initialization
        self.top_bar = TopBar(self.screen.get_width())
        button_labels = ['Account', 'World Map', 'Leaderboard', 'Settings', 'Help']
        button_colors = [(100, 100, 200), (100, 200, 100), (200, 100, 100), (100, 200, 200), (200, 200, 100)]
        button_width = 100
        button_height = 40
        button_margin = 20
        x_start = (self.screen.get_width() - (button_width + button_margin) * len(button_labels) + button_margin) // 2

        for i, label in enumerate(button_labels):
            rect = pygame.Rect(x_start + i * (button_width + button_margin), button_margin, button_width, button_height)
            button = Button(label, rect, button_colors[i])
            self.top_bar.add_button(button)

    def handle_events(self, events):
        self.top_bar.handle_events(events)
        for event in events:
            for slot in self.building_slots:
                if event.type == pygame.MOUSEBUTTONDOWN and slot['rect'].collidepoint(event.pos):
                    slot['clicked'] = not slot['clicked']  # Toggle clicked state
                    print(f"Clicked on slot at {slot['rect'].topleft}")

    def draw(self):
        # Draw the background
        self.screen.blit(self.background, (0, 0))
        
        # Draw top bar and buttons
        self.top_bar.draw(self.screen)
        
        # Draw squares for building slots
        for slot in self.building_slots:
            color = (200, 0, 0) if slot['clicked'] else (100, 100, 100)
            pygame.draw.rect(self.screen, color, slot['rect'])

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
test_overview_ui()

