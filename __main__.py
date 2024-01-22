# 11th grade Spring Semester game
# (c) Jason Zheng 2024


#imports
import bosses
from time import sleep
from random import randint 
#Edit the debug symbols file to make the game enter different debug modes
from debug_symbols import *

#Functions

#Modified input() that checks if the correct type is inputed in a certain range and reprompt if is not
def safer_input(statement, lower_extreme = 0, upper_extreme = 0):
    isInputSafe = False
    while isInputSafe != True:
        player_input = input(statement)
        #Check if the input can be turned into a int
        try:
            int(player_input)
        except:
            slow_print("Your input is invaild. Please try again\n")
        else:
            #Checks if either the lower extreme or the upper extreme as been changed and needs to be considered
            if lower_extreme == 0 and upper_extreme == 0:
                isInputSafe = True
            #If either the extremes have been changed, check for them
            elif int(player_input) >= lower_extreme and int(player_input) <= upper_extreme:
                isInputSafe = True
            else: slow_print("Your input is invaild. Please try again\n")
    return(int(player_input))

#Slowly print out something, letter by letter based on a inputed delay
def slow_print(statement, delay=0.05):

    #Check if it is a string
    if isinstance(statement, str) != True:
        print("Slow print received statment not in string format")
        return
    i = 0
    #While loop that prints each letter
    while i < len(statement):
        print(statement[i], end='',flush=True)
        if fastprint == False:
            sleep(delay)
        i += 1
    #One final print to create a new line
    print()

#Print the stats of a weapon
def weaponStats(weapon, turn_timer):
    print("The " + weapon.name)
    print("Attack: {0:.2f}".format(weapon.attack))
    print("The weapon has a cooldown of {} turns".format(weapon.cooldown))
    if weapon.cooldownTimer - turn_timer > 0:
        print("The item has a cooldown and can not be used for {} turns".format((weapon.cooldownTimer - turn_timer)))

#Asks which potion to use and returns character and opponent attack effectiveness 
def playerPotionAsk(potions):
    slow_print("You have these potions")
    potionList = list(potions.keys())
    for i in range(len(potionList)):
        humanNumber = i + 1
        print("-{} {}".format(humanNumber, potionList[i].name))
        print("   {}".format(potionList[i].description))
        print("   Lasts for {} turns".format(potionList[i].length))
        print("   The defense effectiveness is {} percent".format(potionList[i].defenseEffectiveness))
        print("   The attack effectiveness is {} percent".format(potionList[i].attackEffectiveness))
        print("   You have {} {} left".format(potions[potionList[i]],potionList[i].name))
    potionChoice = safer_input("What potion do you want to use?", 0, len(potions)) - 1
    return(potionList[potionChoice])
#Main engine that deals with each battle. Character should always be the actual player
#Returns (if died (as a boolean), playerhealth)
def fightEngine(character, boss):
    slow_print("You are now fighting a(n) " + boss.name + "!")
    turn_timer = 0
    while character.health > 0 and boss.health > 0:
        #Reset defense stats 
        character_defense = 0
        boss_defense = 0
        character_attack_effectiveness = 100
        boss_attack_effectiveness = 100

        #Ask for player action and calculate boss's actions
        character_action = safer_input("""What do you want to do? \n
                   1. Attack \n
                   2. Defend \n""")
        boss_action = randint(1,2)
        
        #Check if either increased defense 
        if character_action == 2:
            #Print out the current potions and ask for which potion to use
            potion_choice = playerPotionAsk(character.potions)
            
            #Edit the attack effectiveness based on potion effects and change the potions left in inventory
            character_defense = potion_choice.defenseEffectiveness                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
            boss_attack_effectiveness = 100 - character_defense
            character.potions[potion_choice] -= 1
            slow_print("Your defense has been increased by {0} for this round!".format(character_defense))
        if boss_action == 2:
            boss_defense = randint(1,50) 
            character_attack_effectiveness = 100 - boss_defense
            slow_print("The {0} increased his defense by {1} for this round!".format(boss.name, boss_defense))

        #Check if either are attacking and attack
        if character_action == 1:
            #Show the player their current weapons
            slow_print("Here are the your current weapons:")
            i = 0
            while i < len(character.weapons):
                print(str(i+1))
                weaponStats(character.weapons[i], turn_timer)
                print()
                i += 1
            
            #Ask the player what weapon they want
            while i != 0:
                #Use safer_input's range limiter to make sure the weapon actually exist and the -1 is to use code counting from 0 instead of 1
                weapon_choice = safer_input("What weapon do you want to choose?",0, len(character.weapons)) - 1

                #check if it has a cooldown
                if character.weapons[weapon_choice].cooldownTimer > turn_timer:
                    print("That weapon currently has a cooldown. Please use another weapon ")
                else:
                    i = 0

            #Calculate boss health, modify the cooldown timer and print the results
            boss.health -= character.weapons[weapon_choice].attack * (character_attack_effectiveness/100)
            character.weapons[weapon_choice].cooldownTimer = (turn_timer+1) + character.weapons[weapon_choice].cooldown
            slow_print("You {0} the {1} and dealt {2:.2f} damage".format(
                                                                character.weapons[weapon_choice].attackName, 
                                                                boss.name, 
                                                                (character.weapons[weapon_choice].attack * (character_attack_effectiveness/100))))
            slow_print("The {0}'s health is now {1:.2f}".format(boss.name, boss.health))
        
        #Checks if boss attacks
        if boss_action == 1:
            character.health -= boss.attack * (boss_attack_effectiveness/100)
            slow_print("The {0} attacked you and dealt {1:.2f} damage".format(boss.name, (boss.attack * (boss_attack_effectiveness/100))))
            slow_print("Your health is now {0:.2f}".format(character.health))

        #Increment Turn Timer
        turn_timer += 1

    #After the while loop finishes and someone died
    #Checks if character is dead or alive and return the correct arguments
    if character.health <= 0:
        print("You have died")
        return (True, character.health)
    elif character.health > 0:
        print("Congratulations! You won!")
        return (False, character.health)

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
    def __init__(self, name, description, length, defenseEffectiveness = 0, attackEffectiveness = 0):
        self.name = name
        self.description = description
        self.length = length
        self.defenseEffectiveness = defenseEffectiveness
        self.attackEffectiveness = attackEffectiveness
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

main()