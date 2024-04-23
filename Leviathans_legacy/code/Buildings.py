import os
import pygame
from Player import player1  # This assumes you have a player class that includes a 'steel' attribute

class Buildings:
    def __init__(self, image_filename="SimpleBuilding.png"):
        self.build_cost = 10
        self.build_time = 10
        self.upgrade_possible = True
        self.buyable = True
        self.building_stage = 0
        self.increase_rate_of_price = 1
        self.increase_rate_of_build_time = 1.5
        self.base_image_path = "sprites"
        self.image_filename = image_filename
        self.image = self.load_image()

    def load_image(self):
        """Load an image based on the current stage."""
        full_path = os.path.join(os.path.dirname(__file__), '..', self.base_image_path, self.image_filename)
        try:
            return pygame.image.load(full_path)
        except pygame.error as e:
            print(f"Unable to load image at {full_path}. Error: {e}")
            raise SystemExit(e)

    def build(self):
        if player1.steel >= self.build_cost and self.upgrade_possible and self.buyable and self.building_stage == 0:
            player1.steel -= self.build_cost
            self.building_stage = 1
            self.increase_of_price()
            pygame.time.set_timer(pygame.USEREVENT, self.build_time * 1000)
            self.increase_build_timer()
            self.buyable = False

    def upgrade(self):
        if player1.steel >= self.build_cost and self.upgrade_possible and self.buyable and self.building_stage >= 0:
            player1.steel -= self.build_cost
            self.building_stage += 1
            self.increase_of_price()
            pygame.time.set_timer(pygame.USEREVENT, self.build_time * 1000)
            self.increase_build_timer()

    def demolish(self):
        if self.building_stage > 0:
            self.building_stage -= 1

    def print_info(self):
        print(f"Build Cost: {self.build_cost}, Player Steel: {player1.steel}")

    def set_attributes(self, build_cost, build_time, upgrade_possible, buyable, building_stage, increase_rate_of_build_time):
        self.build_cost = build_cost
        self.build_time = build_time
        self.upgrade_possible = upgrade_possible
        self.buyable = buyable
        self.building_stage = building_stage
        self.increase_rate_of_build_time = increase_rate_of_build_time

    def increase_of_price(self):
        self.build_cost += self.increase_rate_of_price

    def increase_build_timer(self):
        self.build_time *= self.increase_rate_of_build_time

    def set_image(self, stage, image_filename):
        """Update image path for specific building stage and reload image."""
        self.image_paths[stage] = image_filename
        self.load_images()  # Reload images to reflect change

    def get_image(self):
        """Get the current image based on the building's stage."""
        return self.loaded_images.get(self.building_stage, self.loaded_images[0])

class Plantation(Buildings):
    def __init__(self):
        super().__init__("SimpleBuilding.png")
        self.build_cost = 20
        self.build_time = 30
        self.production_rate = 5

class PowerPlant(Buildings):
    def __init__(self):
        super().__init__("SimpleBuilding.png")
        self.build_cost = 40
        self.build_time = 45
        self.energy_output = 100

class Cabins(Buildings):
    def __init__(self):
        super().__init__("SimpleBuilding.png")
        self.build_cost = 30
        self.build_time = 20

class Barracks(Buildings):
    def __init__(self):
        super().__init__("SimpleBuilding.png")
        self.build_cost = 50
        self.build_time = 60

class AbyssalOreRefinery(Buildings):
    def __init__(self):
        super().__init__("SimpleBuilding.png")
        self.build_cost = 70
        self.build_time = 80
        self.ore_processing_rate = 15

class DefensiveDome(Buildings):
    def __init__(self):
        super().__init__("SimpleBuilding.png")
        self.build_cost = 100
        self.build_time = 90
        self.defense_capability = 200













