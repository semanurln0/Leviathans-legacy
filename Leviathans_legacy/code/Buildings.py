import pygame
from pygame import freetype
from Player import player1
import UIElements



class Buildings:
    def __init__ (self):
        self.__BuildCost=10                   # Basic Parameters which a building should have
        self.__BuildTime=10
        self.__UpgradePossible= True
        self.__Buyable=True
        self.__BuildingsStage=0
        self.__IncreaseRateOfPrice=1
        self.__image_path =0
        self.__IncreaseRateOfBuildTime= 1.5

    def Build(self):
        if player1.steel >= self.__BuildCost and self.__UpgradePossible == True and self.__Buyable == True and self.__BuildingsStage == 0 :
            player1.steel -= self.__BuildCost  # Building the Building For now its simplely adding stage to +1 we can improve for future sup classes
            self.__BuildingsStage=1
            self.__IncreaseOfPrice(self.__BuildCost)
            pygame.time.set_timer(pygame.USEREVENT, self.__BuildTime * 1000)
            self.__IncreaseBuildTimer()


    def Upgrade(self):
        if player1.steel >= self.__BuildCost and self.__UpgradePossible == True and self.__Buyable == True and self.__BuildingsStage >= 0 :
            player1.steel -= self.__BuildCost  # Upgrading the Building For now its simplely adding stage to +1 we can improve for future sup classes
            self.__BuildingsStage=1
            self.__IncreaseOfPrice()
            pygame.time.set_timer(pygame.USEREVENT, self.__BuildTime * 1000)     # I am not sure if this will work We need to test it also may need edit 
            self.__IncreaseBuildTimer()
            

    def Demolish(self):      # if needs to destroy any building for future
        if  self.__BuildingsStage > 0 :
            self.__BuildingsStage -=1

    def Print_Info(self) :      #basicly For checking we can delete this any time
        print(self.__BuildCost,player1.steel)

    def Setter(self, BuildCost, BuildTime, Upgrade_Possible, buyable, BuildingsStage,IncreaseRateOfBuildTime) :
        self.__BuildCost=BuildCost                  # Parameter Setter its good usage for future
        self.__BuildTime=BuildTime
        self.__UpgradePossible= Upgrade_Possible
        self.__Buyable=buyable
        self.__BuildingsStage=BuildingsStage
        self.__IncreaseRateOfBuildTime=IncreaseRateOfBuildTime

    def __IncreaseOfPrice (self):   #ofcourse Price for increasing should Increase with time
        self.__BuildCost += self.__IncreaseRateOfPrice
        return self.__BuildCost

    def __IncreaseBuildTimer(self):
        self.__BuildTime = self.__BuildTime*self.__IncreaseRateOfBuildTime

    def SetImage(self, image_path):
        self.__image_path = image_path

    def GetImage(self):                         #not working correctly  I give up I need little sleep
        return self.__image_path



#pygame.display.set_caption("Building Images")
#building_image = pygame.image.load(building1.GetImage()).convert_alpha()
#screen.blit(building_image, (100, 100))  # Display the building image













