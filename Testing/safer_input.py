import time

fastprint = False
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


safer_input("Test")