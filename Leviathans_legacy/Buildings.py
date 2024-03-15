import pygame
from pygame import freetype
from Player import player1
import UIElements



class Buildings:
    def __init__ (self):
        self.__BuildCost=10                   # Basic Parameters which a building should have 
        self.__BuildTime=0 
        self.__UpgradePossible= True 
        self.__Buyable=True
        self.__BuildingsStage=0
        self.__IncreaseRateOfPrice=1
        self.__image_path =0
        

    def Build(self):
        if player1.steel >= self.__BuildCost and self.__UpgradePossible == True and self.__Buyable == True and self.__BuildingsStage == 0 :
            player1.steel -= self.__BuildCost  # Building the Building For now its simplely adding stage to +1 we can improve for future sup classes
            self.__BuildingsStage=1 
            self.__IncreaseOfPrice(self.__BuildCost)
            

    def Upgrade(self):
        if player1.steel >= self.__BuildCost and self.__UpgradePossible == True and self.__Buyable == True and self.__BuildingsStage >= 0 :
            player1.steel -= self.__BuildCost  # Upgrading the Building For now its simplely adding stage to +1 we can improve for future sup classes
            self.__BuildingsStage=1 
            self.__IncreaseOfPrice(self.__BuildCost)

    def Demolish(self):      # if needs to destroy any building for future
        if  self.__BuildingsStage > 0 :
            self.__BuildingsStage -=1

    def Print_Info(self) :      #basicly For checking we can delete this any time
        print(self.__BuildCost,player1.steel)

    def Setter(self,BuildCost,BuildTime,Upgradepossible,buyable,BuildingsStage) :
        self.__BuildCost=BuildCost                  # Parameter Setter its good usage for future  
        self.__BuildTime=BuildTime
        self.__UpgradePossible= Upgradepossible
        self.__Buyable=buyable
        self.__BuildingsStage=BuildingsStage

    def __IncreaseOfPrice (self,__BuildCost):   #ofcourse Price for increasing should Increase with time
        self.__BuildCost += self.__IncreaseRateOfPrice 
        return self.__BuildCost 
    
    def SetImage(self, image_path):
        self.__image_path = image_path

    def GetImage(self):                         #not working correctly  I give up I need little sleep
        return self.__image_path
     
  
    
#pygame.display.set_caption("Building Images")  
#building_image = pygame.image.load(building1.GetImage()).convert_alpha()
#screen.blit(building_image, (100, 100))  # Display the building image



     

 
    



         

    
