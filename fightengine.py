from functions import *
from random import randint

#Fight Engine specific functions
#Asks which potion to use and returns character and opponent attack effectiveness 
def playerPotionAsk(potions):
    slow_print("You have these potions")
    #Pulls a list of the potions in inventory from potions dictionary
    potionList = list(potions.keys())
    for i in range(len(potionList)):
        #Adds one to everything to turn it into a human number
        humanNumber = i + 1
        print("-{} {}".format(humanNumber, potionList[i].name))
        print("   {}".format(potionList[i].description))
        print("   Lasts for {} turns".format(potionList[i].length))
        print("   The defense effectiveness is {} percent".format(potionList[i].defenseEffectiveness))
        print("   The attack effectiveness is {} percent".format(potionList[i].attackEffectiveness))
        print("   You have {} {} left".format(potions[potionList[i]],potionList[i].name))
    
    #Asks which potion the player wants to use
    potionChoice = safer_input("What potion do you want to use?", 0, len(potions)) - 1
    #Returns the potion that the player wants by pulling the potion from potionlist
    return(potionList[potionChoice])

def characterAttack(character, boss, turn_timer, character_attack_effectiveness):
    slow_print("You are attacking")

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
        weapon_choice = safer_input("What weapon do you want to choose?",1, len(character.weapons)) - 1

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
    if boss.health > 0:
        slow_print("The {0}'s health is now {1:.2f}".format(boss.name, boss.health))

    #Return boss class (like health)
    return boss

def bossAttack(character, boss, boss_attack_effectiveness):
    slow_print("The boss is attacking")
    character.health -= boss.attack * (boss_attack_effectiveness/100)
    slow_print("The {0} attacked you and dealt {1:.2f} damage".format(boss.name, (boss.attack * (boss_attack_effectiveness/100))))
    if character.health > 0:
        slow_print("Your health is now {0:.2f}".format(character.health))

    #Return character stats
    return character

#Ask what the player wants to do
def playerActionAsk(character_active_potions):
    #Ask for player action and calculate boss's actions
        print("""Your current options are \n
                   1. Attack \n
                   2. Potions \n""")
        if len(character_active_potions) != 0:
            print("""                   3. Check Currently Active Potions""") 
        character_action = safer_input("What do you want to do? ->",1,3)
        return character_action
#Main engine that deals with each battle. Character should always be the actual player
#Returns (if died (as a boolean), playerhealth)
def fightEngine(character, boss):
    slow_print("You are now fighting a(n) " + boss.name + "!")
    turn_timer = 0
    character_active_potions = []
    while character.health > 0 and boss.health > 0:
        #Calculate defense stats based on active potions and clear potion deletion list
        character_defense = 0
        potionDeleteList = []
        for i in range(len(character_active_potions)):
            #Unpack next list item
            current_potion, potion_length = character_active_potions[i]
            #Check if potion length has expired
            if potion_length > turn_timer:
                #If not expired, reapply the effects
                character_defense += current_potion.defenseEffectiveness
                character_attack_effectiveness += current_potion.attackEffectiveness
                character.health += current_potion.healthBoost
            else:
                #If expired, marked for deletion. (You can not delete rn w/o breaking something)
                potionDeleteList.append(character_active_potions[i])
        
        #Actual potion deletion based on potion delete list
        #Used list comprehension to define a new list w/o the potions in the potion delete list
        character_active_potions = [x for x in character_active_potions if x not in potionDeleteList]
        
        #Tell the player there are still active potions
        if len(character_active_potions) != 0:
            slow_print("You still have active potions")

        #Clear other stats and variables          
        boss_defense = 0
        character_attack_effectiveness = 100
        boss_attack_effectiveness = 100
        character_action = 0

        character_action_ready = False
        #Ask for player action and calculate boss's actions
        while character_action_ready == False:
            character_action = playerActionAsk(character_active_potions)

            #If the player wants to check active potions, print out whats active and ask what to do next
            if character_action == 3:
                for i in range(len(character_active_potions)):
                    current_potion, potion_length = character_active_potions[i]
                    if current_potion.defenseEffectiveness != 0:
                        slow_print("A {0} is increasing your defense by {1} for {2} more turns".format(
                                                            current_potion.name, 
                                                            current_potion.defenseEffectiveness,
                                                            (potion_length-turn_timer)))
                    if current_potion.attackEffectiveness != 0:
                        slow_print("A {0} is increasing your attacks by {1} percent for {2} more turns".format(
                                                            current_potion.name, 
                                                            current_potion.attackEffectiveness,
                                                            (potion_length-turn_timer)))
                        
            #If the character chooses to attack or use potions, break loop by setting character_action_ready to True        
            if character_action == 1:
                character_action_ready = True
            if character_action == 2:
                character_action_ready = True
                

        #Calculate Boss action   
        boss_action = randint(1,2)
        
        #Check if either used potions 
        if character_action == 2:
            #If there are no potions left, force the character to attack
            if len(character.potions) == 0:
                slow_print("You have no potions left. You have to attack")
                character_action = 1
            else:
                #Print out the current potions and ask for which potion to use
                potion_choice = playerPotionAsk(character.potions)

                #Take the chosen potion and add it to character_active_potions list with a calulated length that it should last
                character_active_potions.append([potion_choice, (turn_timer + potion_choice.length)])

                #Edit the defense and offense effectiveness and add the health boost based on potion effects 
                if potion_choice.defenseEffectiveness != 0:
                    character_defense += potion_choice.defenseEffectiveness
                    slow_print("Your defense has been increased by {0} percent for {1} round(s)!".format(potion_choice.defenseEffectiveness, potion_choice.length))
                    slow_print("Your defense is now boosted by {0} percent".format(character_defense))
                if potion_choice.attackEffectiveness != 0:
                    character_attack_effectiveness += potion_choice.attackEffectiveness
                    slow_print("Your offense has been increased by {0} percent for {1} round(s)".format(potion_choice.attackEffectiveness, potion_choice.length))
                    slow_print("Your offensive is now boosted by {0} percent".format(character_attack_effectiveness))
                if potion_choice.healthBoost != 0:
                    character.health += potion_choice.healthBoost
                    slow_print("Your health has been increased by {0}".format(potion_choice.healthBoost))
                    slow_print("Your health is now {0}".format(character.health))

                #change the potions left in inventory                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                boss_attack_effectiveness = 100 - character_defense
                character.potions[potion_choice] -= 1
                
                #If there are no more of the potion choice left, delete it from the dictionary
                if character.potions[potion_choice] == 0:
                    del character.potions[potion_choice]
        if boss_action == 2:
            boss_defense = randint(1,50) 
            character_attack_effectiveness -= boss_defense
            slow_print("The {0} increased his defense by {1} for this round!".format(boss.name, boss_defense))


        #Check if either are attacking and attack
        playerAttackChance = randint(0,100)

        if playerAttackChance <= 30:
            if character_action == 1:
                boss = characterAttack(character, boss, turn_timer, character_attack_effectiveness)
            #Check for health first to see if they died
            if boss_action == 1 and boss.health > 0:
                character = bossAttack(character, boss, boss_attack_effectiveness)
        else:
            if boss_action == 1:
                character = bossAttack(character, boss, boss_attack_effectiveness)
            #Check for health first to see if they died
            if character_action == 1 and character.health > 0:
                boss = characterAttack(character,boss,turn_timer,character_attack_effectiveness)

        #Increment Turn Timer
        turn_timer += 1

    #After the while loop finishes and someone died
    
    #Reset cooldowns
    for i in range(len(character.weapons)):
        character.weapons[i].cooldownTimer = 0

    #Checks if character is dead or alive and return the correct arguments
    if character.health <= 0:
        print("You have died")
        return (True, character.health)
    elif character.health > 0:
        print("Congratulations! You won!")
        return (False, character.health)
