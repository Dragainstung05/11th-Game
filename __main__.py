# 11th grade Spring Semester game
# (c) Jason Zheng 2024
#Set this to true to enable debug mode 
#TODO Make various debug modes to test different parts of the game
debug = True

#imports
import bosses
from time import sleep
from random import randint 

#Functions

#Modified input() that checks if the correct type is inputed and reprompt if is not
def safer_input(statement):
    isInputSafe = False
    while isInputSafe != True:
        player_input = input(statement)
        try:
            int(player_input)
        except:
            slow_print("Your input is invaild. Please try again\n")
        else:
            isInputSafe = True
    return(int(player_input))

#Slowly print out something, letter by letter based on a inputed delay
def slow_print(statement, delay=0.05):

    #Check if it is a string
    if isinstance(statement, str) != True:
        print("Slow print received statment not in string format")
        return
    i = 0
    while i < len(statement):
        print(statement[i], end='',flush=True)
        sleep(delay)
        i += 1
    print()

#Main engine that deals with each battle. Character should always be the actual player
#Returns (if died (as a boolean), playerhealth)
def fightEngine(character, boss):
    slow_print("You are now fighting a(n) " + boss.name + "!")
    while character.health > 0 and boss.health > 0:
        #Ask for player action
        player_action = safer_input("""What do you want to do? \n
                   1. Attack \n
                   2. Defend \n""")
        if player_action == 2:
            character_defense = randint(1,100)
            slow_print("Your defense has been increased by " + character_defense + "for this round!")
        boss_action = randint(1,2)
        if boss_action == 2:
            boss_defense = randint(1,100)
        if player_action == 1:
            boss.health -= character.attack
            slow_print("You attacked the {} and dealt {} damage".format(boss.name, character.attack))
            slow_print("The {}'s health is now {}".format(boss.name, boss.health))
        if boss_action == 1:
            character.health -= boss.attack
            slow_print("The boss attacked you and dealt {} damage".format(boss.attack))
            slow_print("Your health is now " + str(character.health))
    #Check if character is dead or alive and return the correct arguments
    if character.health <= 0:
        return (True, character.health)
    elif character.health > 0:
        return (False, character.health)

#grab the variables needed and print a basic title screen
#Setting up classes
#TODO add weapons class and edit attack atributes to be a weapons list
class Player:
    def __init__(self, name, health, attack):
        self.name  = name
        self.health = health
        self.attack = attack
class Boss:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack
 
print("Welcome to Jason's Horrible Fighting Game.")
#Quick check to bypass some title screen stuff and enter debugging
if debug == True:
    Name = "Testuser"
else:
    Name = str(input("To continue, please enter your name ->"))

Player = Player(Name, 100, 10)

#Main function
def main():
    if debug == True:
        print("Game in Debug Mode")
        print(Player.name)
        print(Player.health)
    Thug = Boss("Thug", 50, 5)
    isDead, Player.health = fightEngine(Player,Thug)
    if debug == True:
        print (isDead)
        print (Player.health)
main()