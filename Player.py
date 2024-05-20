import pygame
import pygame.freetype
Id=0

def IdCreater():
    global Id
    Id+=1
    return Id

class Player:
    # Our player info
    def __init__(self):
        self.food = 100
        self.steel = 100
        self.soldiers = 0
        self.Id=IdCreater()

player1= Player()
player2= Player()
Player3= Player()
print(player1.Id)
print(player2.Id)
print(Player3.Id)