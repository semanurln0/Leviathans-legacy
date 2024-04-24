import pygame
import pygame.freetype
import socket


class Player:
    # Our player info
    def __init__(self, client, username, password):
        self.food = 10000
        self.steel = 10000
        self.energy = 0
        self.soldiers = 0
        self.client = client
        self.__username = username
        self.__password = password

    def get_player_info(self):
        try:
            request = "info"
            self.client.send(request.encode("utf-8")[:1024])
            received = self.client.recv(1024).decode("utf-8")
            print(received)
            p_stats = received.split(" ")
            return p_stats
        except Exception as e:
            self.client = connect_to_server()
            username = self.__username
            password = self.__password
            request = "login" + " " + username + " " + password
            self.client.send(request.encode("utf-8")[:1024])
            request = "info"
            self.client.send(request.encode("utf-8")[:1024])
            received = self.client.recv(1024).decode("utf-8")
            print(received)
            p_stats = received.split(" ")
            return p_stats

    def show_food(self):
        return self.get_player_info()[0]

    def show_steel(self):
        pass
        return self.get_player_info()[1]

    def show_energy(self):
        pass
        return self.get_player_info()[2]


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
