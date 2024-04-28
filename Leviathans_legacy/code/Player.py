import pygame
import pygame.freetype
import socket


class Player:
    # Our player info
    def __init__(self, client=None, username=None, password=None):
        self.food = 10000
        self.steel = 10000
        self.energy = 0
        self.soldiers = 0
        self.client = client
        self.__username = username
        self.__password = password

    def get_player_info(self):
        p_stats = []
        try:
            request = "info"
            self.client.send(request.encode("utf-8")[:1024])
            received = self.client.recv(1024).decode("utf-8")
            print(received)
            p_stats = received.split(" ")
            self.food = int(p_stats[0])
            self.steel = int(p_stats[1])
            self.energy = int(p_stats[2])
        except Exception as e:
            print(e)
            self.client = connect_to_server()
            username = self.__username
            password = self.__password
            request = "login" + " " + username + " " + password
            self.client.send(request.encode("utf-8")[:1024])
            response = self.client.recv(1024).decode("utf-8")
            request = "info"
            self.client.send(request.encode("utf-8")[:1024])
            received = self.client.recv(1024).decode("utf-8")
            print(received)
            p_stats = received.split(" ")
            self.food = int(p_stats[0])
            self.steel = int(p_stats[1])
            self.energy = int(p_stats[2])
        finally:
            return p_stats
        # sets player stats and returns an array of all stats

    def get_buildings(self):
        request = "info_buildings"
        self.client.send(request.encode("utf-8")[:1024])
        received = self.client.recv(1024).decode("utf-8")
        p_stats = received.split(" . ")
        p_stats = p_stats.pop(len(p_stats)-1)
        return p_stats
        # returns array of buildings and their data in the form
        # (1, 1, 'plantation', 1), (1, 2, 'cabins', 1)

    def show_food(self):
        return self.get_player_info()[0]

    def show_steel(self):
        pass
        return self.get_player_info()[1]

    def show_energy(self):
        pass
        return self.get_player_info()[2]

    def set_parameters(self, client, username, password):
        self.client = client
        self.__username = username
        self.__password = password

    def commit_building(self, hexagon_no, building_id, building_level):
        request = "add_building" + " " + str(hexagon_no) + " " + str(building_id) + " " + str(building_level)
        self.client.send(request.encode("utf-8")[:1024])
        # Add building to db, requires following data (pos in hex array, building_name, level of building)


mplayer = Player()


def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8000
    Connected = True
    tries = 0
    while Connected:
        try:
            client.connect((server_ip, server_port))
            print(f"Connected to {server_ip} using {server_port}")
            Connected = False
        except ConnectionRefusedError:
            print("Connection failed")
            tries += 1
            if tries == 5:
                pygame.quit()
            pygame.time.wait(1000)
    return client


def check_connection(client):
    try:
        data = client.recv(1024)
        if not data: raise ConnectionAbortedError
    except ConnectionAbortedError:
        print("Connection aborted, reconnecting")
