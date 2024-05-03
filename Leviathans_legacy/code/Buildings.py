import os
import pygame
from Player import mplayer  # This assumes you have a player class that includes a 'steel' attribute
import time
from abc import ABC, abstractmethod


class AbstractBuilding(ABC):
    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def upgrade(self):
        pass

    @abstractmethod
    def demolish(self):
        pass

    @abstractmethod
    def print_info(self):
        pass


class Buildings(AbstractBuilding):
    def __init__(self, image_filename="SimpleBuilding.png"):
        self.build_cost = 10
        self.build_time = 1
        self.upgrade_possible = True
        self.buyable = True
        self.building_stage = 0
        self.increase_rate_of_price = 1
        self.increase_rate_of_build_time = 1.5
        self.base_image_path = "sprites"
        self.image_filename = image_filename
        self.image = self.load_image()
        self.upgrade_end_time = None

    def load_image(self):
        """Load an image based on the current stage."""
        full_path = os.path.join(os.path.dirname(__file__), '..', self.base_image_path, self.image_filename)
        try:
            return pygame.image.load(full_path)
        except pygame.error as e:
            print(f"Unable to load image at {full_path}. Error: {e}")
            raise SystemExit(e)

    def build(self):
        if mplayer.steel >= self.build_cost and self.upgrade_possible and self.buyable and self.building_stage == 0:
            mplayer.steel -= self.build_cost
            self.building_stage = 1
            self.increase_of_price()
            # pygame.time.set_timer(pygame.USEREVENT, self.build_time * 1000)
            self.buyable = False

    def check_upgrade(self):
        if self.upgrade_end_time and time.time() >= self.upgrade_end_time:
            self.upgrade_end_time = None
            print("Upgrade complete!")

    def get_remaining_upgrade_time(self):
        if self.upgrade_end_time:
            return max(0, int(self.upgrade_end_time - time.time()))
        return 0

    def upgrade(self):
        if self.upgrade_possible and mplayer.steel >= self.build_cost:
            if self.upgrade_end_time == 0 or self.upgrade_end_time == None:
                mplayer.steel -= self.build_cost
                self.building_stage += 1
                self.increase_of_price()
                self.build_time *= self.increase_rate_of_build_time
                self.upgrade_end_time = time.time() + self.build_time

    def demolish(self):
        if self.building_stage > 0:
            self.building_stage -= 1

    def print_info(self):
        print(f"Build Cost: {self.build_cost}, Player Steel: {mplayer.steel}")

    def set_attributes(self, build_cost, build_time, upgrade_possible, buyable, building_stage,
                       increase_rate_of_build_time):
        self.build_cost = build_cost
        self.build_time = build_time
        self.upgrade_possible = upgrade_possible
        self.buyable = buyable
        self.building_stage = building_stage
        self.increase_rate_of_build_time = increase_rate_of_build_time

    def increase_of_price(self):
        self.build_cost += self.increase_rate_of_price

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

    def set_attributes(self, build_cost, build_time, upgrade_possible, buyable, building_stage,
                       increase_rate_of_build_time, production_rate):
        self.build_cost = build_cost
        self.build_time = build_time
        self.upgrade_possible = upgrade_possible
        self.buyable = buyable
        self.building_stage = building_stage
        self.increase_rate_of_build_time = increase_rate_of_build_time
        self.production_rate = production_rate


class PowerPlant(Buildings):
    def __init__(self):
        super().__init__("SimpleBuilding.png")
        self.build_cost = 40
        self.build_time = 45
        self.energy_output = 100

    def set_attributes(self, build_cost, build_time, upgrade_possible, buyable, building_stage,
                       increase_rate_of_build_time, energy_output):
        self.build_cost = build_cost
        self.build_time = build_time
        self.upgrade_possible = upgrade_possible
        self.buyable = buyable
        self.building_stage = building_stage
        self.increase_rate_of_build_time = increase_rate_of_build_time
        self.energy_output = energy_output


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

    def set_attributes(self, build_cost, build_time, upgrade_possible, buyable, building_stage,
                       increase_rate_of_build_time, ore_processing_rate):
        self.build_cost = build_cost
        self.build_time = build_time
        self.upgrade_possible = upgrade_possible
        self.buyable = buyable
        self.building_stage = building_stage
        self.increase_rate_of_build_time = increase_rate_of_build_time
        self.ore_processing_rate = ore_processing_rate


class DefensiveDome(Buildings):
    def __init__(self):
        super().__init__("SimpleBuilding.png")
        self.build_cost = 100
        self.build_time = 90
        self.defense_capability = 200

    def set_attributes(self, build_cost, build_time, upgrade_possible, buyable, building_stage,
                       increase_rate_of_build_time, defense_capability):
        self.build_cost = build_cost
        self.build_time = build_time
        self.upgrade_possible = upgrade_possible
        self.buyable = buyable
        self.building_stage = building_stage
        self.increase_rate_of_build_time = increase_rate_of_build_time
        self.defense_capability = defense_capability


class BuildingFactory:
    def create_building(self, building_type):
        """Factory method to create buildings based on the type."""
        if building_type == 'plantation':
            return Plantation()
        elif building_type == 'power_plant':
            return PowerPlant()
        elif building_type == 'cabins':
            return Cabins()
        elif building_type == 'barracks':
            return Barracks()
        elif building_type == 'abyssal_ore_refinery':
            return AbyssalOreRefinery()
        elif building_type == 'defensive_dome':
            return DefensiveDome()
        else:
            raise ValueError(f"Unknown building type {building_type}")
