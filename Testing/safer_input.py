from time import sleep
def slow_print(statement, delay):
    #Check if it is a string
    if isinstance(statement, str) != True:
        print("Slow print received statment not in string format")
        return
    i = 0
    while i < len(statement):
        print(statement[i], end='',flush=True)
        sleep(delay)
        i += 1

def safer_input(statement):
    isInputSafe = False
    while isInputSafe != True:
        player_input = input(statement)
        try:
            int(player_input)
        except:
            slow_print("Your input is invaild. Please try again\n", 0.05)
        else:
            isInputSafe = True
    return(int(player_input))
input = safer_input("Hello")
print(type(input))
print(input)
