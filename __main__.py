# 11th grade Spring Semester game
# (c) Jason Zheng 2024

#imports
import time
import bosses

#Functions

#Slowly print out something, letter by letter based on a inputed delay
def slow_print(statement, delay):
    #Check if it is a string
    if isinstance(statement, str) != True:
        print("Slow print received statment not in string format")
        return
    i = 0
    while i < len(statement):
        print(statement[i], end='',flush=True)
        time.sleep(delay)
        i += 1

#grab the variables needed and print a basic title screen
debug = True
class Player:
    def __init__(self, name, health):
        self.name  = name
        self.health = health
class Boss:
    def __init__(self, name, health, attacks):
        self.name = name
        self.health = health
        self.attacks = attacks
 
print("Welcome to Jason's Horrible Fighting Game.")
Name = str(input("To continue, please enter your name ->"))
Player = Player(Name, 100)

def main():
    if debug == True:
        print("Game in Debug Mode")
        print(Player.name)
        print(Player.health)
    slow_print("This is a test of my slow print function to see how useful it is to read dialog and stuff", .05)
main()