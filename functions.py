from debug_symbols import *
from time import sleep
import msvcrt


class keyboardDisable():
    def start(self):
        self.on = True

    def stop(self):
        self.on = False

    def __call__(self):
        while self.on:
            msvcrt.getwch()

    def __init__(self):
        self.on = False
disable = keyboardDisable()
def clearKeyboardBuffer():
    while msvcrt.kbhit():
        msvcrt.getwch()

#Modified input() that checks if the correct type is inputed in a certain range and reprompt if is not
def safer_input(statement, lower_extreme = 0, upper_extreme = 0):
    isInputSafe = False
    while isInputSafe != True:
        player_input = input(statement)
        #Check if the input can be turned into a int
        try:
            int(player_input)
        except:
            disable.start()
            slow_print("Your input is invaild. Please try again\n")
            clearKeyboardBuffer()
            disable.stop()
        else:
            #Checks if either the lower extreme or the upper extreme as been changed and needs to be considered
            if lower_extreme == 0 and upper_extreme == 0:
                isInputSafe = True
            #If either the extremes have been changed, check for them
            elif int(player_input) >= lower_extreme and int(player_input) <= upper_extreme:
                isInputSafe = True
            else: 
                disable.start()
                slow_print("Your input is invaild. Please try again\n")
                clearKeyboardBuffer()
                disable.stop()
    return(int(player_input))

#Slowly print out something, letter by letter based on a inputed delay
def slow_print(statement, delay=0.05):

    #Check if it is a string
    if isinstance(statement, str) != True:
        print("Slow print received statment not in string format")
        return
    
    #While loop that prints each letter
    i = 0    
    while i < len(statement):
        print(statement[i], end='',flush=True)
        if fastprint == False:
            sleep(delay)
        i += 1
    #One final print to create a new line
    print()

#Print the stats of a weapon
def weaponStats(weapon, turn_timer = 0):
    print("The " + weapon.name)
    print("Attack: {0:.2f}".format(weapon.attack))
    print("The weapon has a cooldown of {} turns".format(weapon.cooldown))
    if turn_timer != 0:
        if weapon.cooldownTimer - turn_timer > 0:
            print("The weapon is on COOLDOWN and can not be used for {} TURNS".format((weapon.cooldownTimer - turn_timer)))
