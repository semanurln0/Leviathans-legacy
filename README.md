# ***Leviethans legacy***

## A python idle game with online capabilites 

## Created by Mesut Erkin Özokutgen, Nedas Alijošius and Sema Nur Alan

---

## 1. **Introduction**

  *  ### What is the purpose of Leviathans legacy?
        * The game is a deep underwater themed idle city building game, similiar to Trajan online with a civilization hexagonal twist

  *  ### How to run the program?

        * Running the program is simple, first server.py has to be executed, it is by default the internal ip of the computer
        * The second part is running main.py. 

  *  ### How to use the legacy of the leviathan
  
        * To play the game, first have to login.
          * To test features, you can login with username "Internedas" and password "123" 
        * Then a main game screen appears, where you can currently click on hexagons to build, demolish, upgrade buildings.

---

## 2. **Analysis**

 *  ### Implementation of OOP principles

      *  #### Polymorphism
            Method Overriding: Derived classes from Buildings may override methods to change or extend the behavior of the base class methods. For example, if a special type of building needs a different method for upgrade(), it can override this method to implement the specific upgrade logic.
      *  #### Abstraction
            AbstractBuilding Class: The AbstractBuilding abstract class provides a clear abstraction layer that defines the common interface for all building types. This class uses abstract methods (build(), upgrade(), demolish(), print_info()) to specify what operations must be implemented, allowing the details of those operations to be defined in derived classes.
      *  #### Inheritance
            Building classes (Plantation, PowerPlant, etc.) inherit from a base Buildings class, sharing common properties like building cost, upgrade times, and methods for upgrading or demolishing.
            InputBoxPass inherits from InputBox, reusing functionality for event handling and rendering while adding password-specific behavior.
      *  #### Encapsulation
            LoginInfo, Player, Building, and Hexagon classes encapsulate their data with private attributes (using the double underscore or through normal convention) and provide methods to operate on this data.
            LoginInfo uses __username and __password to hide details about login credentials, providing methods to set and retrieve these values.
 *  ### Utilized design patterns

      *  #### Factory
            BuildingFactory is a classic example of the Factory pattern, where a separate BuildingFactory class is responsible for creating instances of Buildings based on a type identifier. This encapsulates object creation and allows the introduction of new building types without modifying the factory.
      *  #### Decorator
            The hexagon_update_action decorator exemplifies the Decorator pattern. It acts as a wrapper around the update method of the Hexagon class, augmenting its functionality without altering the original code.he hexagon_update_action decorator plays a crucial role in maintaining data synchronization between the game client and the server. By sending building updates, it keeps the server informed about changes happening in the game world. 

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
