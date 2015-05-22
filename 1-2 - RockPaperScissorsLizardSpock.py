# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors
import random

# helper functions

def number_to_name(number):
    # fill in your code below
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    else: name = "Error"
    return name


    
def name_to_number(name):
    # fill in your code below

    # convert name to number using if/elif/else
    # don't forget to return the result!
    
    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    elif name == "scissors":
        number = 4
    else: number = "Error"
    return number


def rpsls(name): 
    # fill in your code below

    # convert name to player_number using name_to_number

    player_number =  name_to_number(name)
    
    # compute random guess for comp_number using random.randrange()
    comp_number =  random.randrange(0,5)
    
    # compute difference of player_number and comp_number modulo five
    diff = (player_number - comp_number)%5
    
    # use if/elif/else to determine winner
    
   
    winner = ''
    if diff == 0:
        winner = "Player and computer tie!"
    elif diff == 1:
        winner = "Player wins!"
    elif diff == 2:
        winner = "Player wins!"
    elif diff == 3:
        winner = "Computer wins!"
    elif diff == 4:
        winner = "Computer wins!"
   


    # convert comp_number to name using number_to_name
    
    comp_number = number_to_name(comp_number)
    
    # print results
    
    print "Player chooses", name
    print "Computer chooses", comp_number
    print winner
    print '\n'
    
    

    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


