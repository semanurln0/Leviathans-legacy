# ***Leviethans legacy***

## A python idle game with online capabilites 

## Created by Mesut Erkin Özokutgen, Nedas Alijošius and Sema Nur Alan

---
### Screenshots of app

1. [Main menu](Leviathans_legacy/ProgramImages/mainmenu.png)
2. [Main game screen](Leviathans_legacy/ProgramImages/maingamescreen.png)
3. [Building interface initial](Leviathans_legacy/ProgramImages/buildingwithplaceholdericons.png)
4. [Building interface with built building](Leviathans_legacy/ProgramImages/building.png)
5. [Server terminal with connection](Leviathans_legacy/ProgramImages/server.png)
---

## 1. **Introduction**

  *  ### What is the purpose of Leviathans legacy?
        * The game is a deep underwater themed city building game. It is similiar to Trajan online, however it features a hexagonal city bulding board, which allows for more interesting game mechanics

  *  ### How to run the program?

        * Running the program is simple, first `server.py` has to be executed, it is by default the internal ip of the computer
        * Then you have to run `main.py`. 

  *  ### How to use the legacy of the leviathan
  
        * To play the game, first you have to login.
          * To test features, you can login with username `Internedas` and password `123`
        * Then a main game screen appears, where you can currently click on hexagons to build, demolish, upgrade buildings.

---

## 2. **Analysis**

### Implementation of OOP principles

* #### Polymorphism
  * Method Overriding: Derived classes from Buildings may override methods to change or extend the behavior of the base class methods. For example, if a special type of building needs a different method for `upgrade()`, it can override this method to implement the specific upgrade logic.
```python
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

    def set_attributes(self, build_cost, build_time, upgrade_possible, buyable, building_stage,
                       increase_rate_of_build_time):
        self.build_cost = build_cost
        self.build_time = build_time
        self.upgrade_possible = upgrade_possible
        self.buyable = buyable
        self.building_stage = building_stage
        self.increase_rate_of_build_time = increase_rate_of_build_time
```
```python
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
```
* #### Abstraction
  * AbstractBuilding Class: The AbstractBuilding abstract class provides a clear abstraction layer that defines the common interface for all building types. This class uses abstract methods (`build()`, `upgrade()`, `demolish()`, `print_info()`) to specify what operations must be implemented, allowing the details of those operations to be defined in derived classes.
```python
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
```
   
* #### Inheritance
  * Building classes (Plantation, PowerPlant, etc.) inherit from a base Buildings class, sharing common properties like building cost, upgrade times, and methods for upgrading or demolishing.
  InputBoxPass inherits from InputBox, reusing functionality for event handling and rendering while adding password-specific behavior.
   
```python
class AbyssalOreRefinery(Buildings):
   def __init__(self):
       super().__init__("SimpleBuilding.png")
       self.build_cost = 70
       self.build_time = 80
       self.ore_processing_rate = 15
```
* #### Encapsulation
  * LoginInfo, Player, Building, and Hexagon classes encapsulate their data with private attributes (using the double underscore or through normal convention) and provide methods to operate on this data.
  LoginInfo uses `__username` and `__password` to hide details about login credentials, providing methods to set and retrieve these values.
```python
class LoginInfo:
   def __init__(self):
       self.__username = None
       self.__password = None

   def set_login_info(self, username, password):
       self.__username = username
       self.__password = password

   def get_login_user(self):
       return self.__username

   def get_login_pass(self):
       return self.__password
   ```

### Utilized design patterns

 *  #### Factory
       BuildingFactory is a classic example of the Factory pattern, where a separate BuildingFactory class is responsible for creating instances of Buildings based on a type identifier. This encapsulates object creation and allows the introduction of new building types without modifying the factory.
  ```python
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
  ```
*   #### Decorator
The hexagon_update_action decorator exemplifies the Decorator pattern. It acts as a wrapper around the update method of the Hexagon class, augmenting its functionality without altering the original code.he hexagon_update_action decorator plays a crucial role in maintaining data synchronization between the game client and the server. By sending building updates, it keeps the server informed about changes happening in the game world. 
```python
@hexagon_update_action
def log_building_change(self, hexagon_index, selected):
    self.hexagon_index = hexagon_index
    self.selected_item = selected
    """Log building changes to the server. This method is a placeholder for actual server communication logic."""
    print(f" {selected} logged for hexagon {hexagon_index}.")
```
### Database implementation

* #### Use of SQLite
  * A database was created for the game to store player information, such as resources and buildings. The implementation is quite simple, having a primary key of PlayerID, which has a one to many relationship with Buildings table for easy querying.
  * The database is widely implemented in manu functions of the program, like for getting player info on server side from database and then sending it to player.
```python
if break_up[0] == "login": # break_up is split received data
    querier.execute("SELECT * FROM Players WHERE PName = ?", (break_up[1],))
    data = querier.fetchone()
    if data is None:
        print('There is no profile named %s' % break_up[1])
        response = "rejected"
    else:
        print('Username %s found, pass is %s, given is %s' % (break_up[1], data[2], break_up[2]))
        if break_up[2] == data[2]:
            response = "accepted"
            username = data[1]
            pid = data[0]
        else:
            response = "rejected"
    client_socket.send(response.encode("utf-8")[:1024])
```

### Unit Testing Overview
Important note; We have 2 different Test file now. 
    1) test_game.py is just using our manual values without changing them so this one only test our game functions. /for this stage.
    2) test_game_random.py is testing all the functions with random values. If any value give error it give output and continue try same function with another value (max 3 try.). So this test for NEXT STAGES upgradefor our game.
--Unit testing is performed using the unittest framework in Python.
--Each test class is dedicated to testing specific functionalities of the codebase.
--Tests cover a wide range of scenarios, including object creation, UI updating, event handling, and method behaviors.
--Mocking is utilized to isolate and test individual components, ensuring reliable and independent test results.

```python
class TestHexagon(unittest.TestCase):

    def setUp(self):
        self.hexagon = Hexagon((100, 100), 50)

    def test_draw(self):
        # Test if draw method correctly draws the hexagon on the screen
        screen = MagicMock(name='Screen')
        self.hexagon.draw(screen)
        screen.draw.polygon.assert_called_once()

    def test_is_clicked(self):
        # Test if is_clicked method returns True when the hexagon is clicked
        event = MagicMock(name='Event')
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (100, 100)
        self.assertTrue(self.hexagon.is_clicked(event))
```
--Each test method is documented to describe the specific functionality being tested and the expected behavior.
--Assertions are used to validate expected outcomes, ensuring code correctness and reliability.
--Test suites are organized by functionality and executed using custom test runners to provide comprehensive test coverage.

## 3. **Results and conclusions**

## 3.1. **Results**

* The resulting program is stable and allows for the main functions, which were intended in our scope
* The server, to allow for multiple clients, support multithreading, giving a thread to each client, with its own erron handling, meaning if a socket connection raises an error, the server remains running and can be used again by another client or remain being used by a second client.
* A database is integrated into server and is used for all player information handling
* The main game screen with buildings allows for building, demolishing, upgrading of buildings, with buttons for various activities and dynamic display and generation of various features using pillars of OOP.
* The login screen is of limited sreen size, with resizing disabled and implemented text input boxes(The most difficult part of the project for Nedas).

## 3.2. **Conclusions**

* To conclude, this work has achieved its goal of creating a functional underwater themed idle building game with the implementation of a working client, server and database. 
* The final product incorporates all the principles of OOP, multiple design patterns and sophisticated error handling, where everything is made up of dynamic classes and methods with their separate purposes, but universal usability throughout. 
* For Leviathans legacy, there is also room for expansion, by creating more complex gameplay, account creation via internet or client and multiplayer features, like war and trade.
