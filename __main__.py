# 11th grade Spring Semester game
# (c) Jason Zheng 2024


#imports
import bosses
from time import sleep
from random import randint 
#Edit the debug symbols file to make the game enter different debug modes
from debug_symbols import *
from functions import * 
from fightengine import *
#Functions


#grab the variables needed and print a basic title screen
#Setting up classes
#TODO add weapons class and edit attack atributes to be a weapons list
class Gladiator:    
    def __init__(self, name, health, potions):
        self.name = name
        self.health = health
        self.potions = potions
         
class Player(Gladiator):
    def __init__(self, name, health, weapons, potions):
        self.weapons = weapons
        Gladiator.__init__(self, name, health, potions)        

class Boss(Gladiator):
    def __init__(self, name, health, attack, potions):
        self.attack = attack
        Gladiator.__init__(self, name, health, potions)
class Weapon:
    cooldownTimer = 0
    def __init__(self, name, attackName, attack, cooldown):
        self.name = name
        self.attackName = attackName
        self.attack = attack
        self.cooldown = cooldown

class Potion:
    def __init__(self, name, description, length, defenseEffectiveness = 0, attackEffectiveness = 0, healthBoost = 0):
        self.name = name
        self.description = description
        self.length = length
        self.defenseEffectiveness = defenseEffectiveness
        self.attackEffectiveness = attackEffectiveness
        self.healthBoost = healthBoost 

#Main function
def main():
    print("Welcome to Jason's Horrible Fighting Game.")
    #Quick check to bypass some title screen stuff and enter debugging
    if debug == True:
        Name = "Testuser"
        slow_print("Game in Debug Mode", 0.001)
    else:
        Name = str(input("To continue, please enter your name ->"))
    fist = Weapon("Fist", "hit", 7, 0)
    player = Player(Name, 100, [fist], {})
    
    if fightEngineDebug == True: 
        gun = Weapon("OP GUN", "shot", 100, 4)
        sword = Weapon("Wooden Sword", "swung at", 10, 2)
        testpotion = Potion("Dev defense potion", "Increases defense by 50 percent for 1 turn", 1, 50, 0)
        testpotion2 = Potion("OP Defense potion", "Dev stuff", 5, 100, 0)
        player.weapons.append(gun)
        player.weapons.append(sword)   
        player.potions[testpotion] = 5 
        player.potions[testpotion2] = 8
        #thechoice = playerPotionAsk(player.potions)
        #print(thechoice.name)
        print(player.name)
        print(player.health)
        print(player.weapons)
        Thug = Boss("Thug", 50, 10, [])
        isDead, player.health = fightEngine(player,Thug)
        print (isDead)
        print (player.health)

    if fightEngineDemo == True:
        sword = Weapon("Wooden Sword", "swung at", 10, 2)
        bow = Weapon("Bow", "shot", 20, 4)
        player.weapons.append(sword)
        player.weapons.append(bow)
        defensePot = Potion("Defense Potion", "Increases your defense by 40%", 3, 40,)
        offensePot = Potion("Offense Potion", "Increases the damage your attacks do for 5 turns by 20%", 6,0,20)
        healthPot = Potion("Health Potion", "Increases your health by 27 over 3 turns", 3, 0, 0, 9)
        player.potions[defensePot] = 5
        player.potions[offensePot] = 5
        player.potions[healthPot] = 10
        isDead = False
        battles = 0
        while isDead == False:
            Glad = Boss("Gladiator", 50, 10, [])
            SpikeGlad = Boss("Scary Gladiator", 25, 50, [])
            GladBoss = Boss("Big Gladiator", 100, 25, [])
            Glads = [Glad, GladBoss, SpikeGlad]
            ChosenGlad = Glads[randint(0,2)]
            isDead, player.health = fightEngine(player, ChosenGlad)
            battles += 1
            if battles >= 10:
                slow_print("You won the game! The game has switched to endless mode and you can continue to play to see how long you last!")
main()