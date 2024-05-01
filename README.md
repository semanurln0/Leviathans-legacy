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

      *  #### Abstraction

      *  #### Inheritance
    
      *  #### Encapsulation

 *  ### Utilized design patterns

      *  #### Factory

      *  #### Decorator

---

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
