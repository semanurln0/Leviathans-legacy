import random
import math


class Army:
    def __init__(self, player):
        self.player = player
        self.soldiers = {
            1: {'name': 'AbyssalMarines', 'count': 0, 'cost': {'food': 100, 'steel': 50}, 'defense': 10},
            2: {'name': 'NautilusCommandos', 'count': 0, 'cost': {'food': 200, 'steel': 100}, 'defense': 20},
            3: {'name': 'DeepSeaStalkers', 'count': 0, 'cost': {'food': 300, 'steel': 150}, 'defense': 30},
            4: {'name': 'NautilusCruiser', 'count': 0, 'cost': {'food': 400, 'steel': 200}, 'defense': 40},
            5: {'name': 'MarianaMarauder', 'count': 0, 'cost': {'food': 500, 'steel': 250}, 'defense': 50},
            6: {'name': 'Kraken', 'count': 0, 'cost': {'food': 600, 'steel': 300}, 'defense': 60},
        }

    def add_soldier(self, unit_id, count):
        if unit_id in self.soldiers:
            cost = self.soldiers[unit_id]['cost']
            total_food_cost = cost['food'] * count
            total_steel_cost = cost['steel'] * count

            if self.player.food >= total_food_cost and self.player.steel >= total_steel_cost:
                self.player.food -= total_food_cost
                self.player.steel -= total_steel_cost
                self.soldiers[unit_id]['count'] += count
                print(f"Added {count} {self.soldiers[unit_id]['name']}(s). New count: {self.soldiers[unit_id]['count']}")
            else:
                print(f"Not enough resources to add soldiers.{self.soldiers[unit_id]['name']}")

    def remove_soldier(self, unit_id, count):
        if unit_id in self.soldiers and self.soldiers[unit_id]['count'] >= count:
            self.soldiers[unit_id]['count'] -= count
            print(f"Removed {count} {self.soldiers[unit_id]['name']}(s). New count: {self.soldiers[unit_id]['count']}")
        else:
            print("Not enough soldiers to remove.")

    def get_units_total_defense(self, unit_id):
        if unit_id in self.soldiers:
            return self.soldiers[unit_id]['count'] * self.soldiers[unit_id]['defense']
        return 0

    def send_army_info_to_server(self):
        army_info = {unit_id: data['count'] for unit_id, data in self.soldiers.items()}
        # Implement the actual server communication here
        print(f"Sending army info to server: {army_info}")

    def receive_army_info_from_server(self, army_info):
        for unit_id, count in army_info.items():
            if unit_id in self.soldiers:
                self.soldiers[unit_id]['count'] = count
        print(f"Received army info from server: {army_info}")


    def battle(self, enemy_army):
            while not self.is_defeated() and not enemy_army.is_defeated():
                attacker_id = random.choice(list(self.soldiers.keys()))
                defender_id = random.choice(list(enemy_army.soldiers.keys()))

                attacker = self.soldiers[attacker_id]['type']
                defender = enemy_army.soldiers[defender_id]['type']

                if self.soldiers[attacker_id]['count'] > 0 and enemy_army.soldiers[defender_id]['count'] > 0:
                    damage = max(0, attacker.attack_power - defender.defense)
                    units_lost = math.floor(damage / defender.health)
                    enemy_army.remove_soldier(defender_id, units_lost)
                    print(f"{attacker.name} attacked {defender.name}, dealing {damage} damage, causing {units_lost} units to be lost.")

                # Switch roles
                attacker_id = random.choice(list(enemy_army.soldiers.keys()))
                defender_id = random.choice(list(self.soldiers.keys()))

                attacker = enemy_army.soldiers[attacker_id]['type']
                defender = self.soldiers[defender_id]['type']

                if enemy_army.soldiers[attacker_id]['count'] > 0 and self.soldiers[defender_id]['count'] > 0:
                    damage = max(0, attacker.attack_power - defender.defense)
                    units_lost = math.floor(damage / defender.health)
                    self.remove_soldier(defender_id, units_lost)
                    print(f"{attacker.name} attacked {defender.name}, dealing {damage} damage, causing {units_lost} units to be lost.")

            if self.is_defeated():
                print("Our army has been defeated!")
            else:
                print("Enemy army has been defeated!")

