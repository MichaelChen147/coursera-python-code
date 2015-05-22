# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math

# initialize global variables used in your code

comp_num = 0
guesses = 0
maxrange = 100

# helper function to start and restart the game

def new_game():
    global comp_num, guesses, maxrange
    if maxrange == 100:
        comp_num = comp100()
    elif maxrange == 1000:
        comp_num = comp1000()

# define event handlers for control panel
# button that changes range to range [0,100) and restarts
        
def comp100():
    global comp_num, guesses, maxrange
    guesses = 7
    maxrange = 100
    comp_num = random.randrange(0, 100)
    print "New game. Range is from 1-100"
    print "Number of guesses remaining", guesses,
    print ("\n")
    return comp_num

# button that changes range to range [0,1000) and restarts

def comp1000():
    global comp_num, guesses, maxrange
    guesses = 10
    maxrange = 1000
    comp_num = random.randrange(0, 1000)
    print "New game. Range is from 1-1000"
    print "Number of guesses remaining", guesses,
    print ("\n")
    return comp_num

# main game logic goes here	

def inputguess(inp):
    global comp_num, guesses
    player_num = int(inp)
    guesses = guesses - 1
    if (player_num == comp_num) and (guesses > 0):
        print "Guess was", inp
        print "Correct!"
        print ""
        new_game()
    elif (player_num > comp_num) and (guesses > 0):
        print "Guess was", inp
        print "Number of remaining guesses", guesses
        print "Lower!"
        print ""
    elif (player_num < comp_num) and (guesses > 0):
        print "Guess was", inp
        print "Number of remaining guesses", guesses
        print "Higher!"
        print ""
    else: 
        print "Guess was", inp
        print "Number of remaining guesses", guesses
        print "You ran out of guesses.The number was", comp_num
        print ""
        return new_game()
   
            

   
    
# create frame
    
f = simplegui.create_frame("Guess the Number", 300, 300)

# register event handlers for control elements

inp = f.add_input("Enter guess", inputguess, 100)
f.add_button("1-100", comp100, 100)
f.add_button("1-1000", comp1000, 100)

# call new_game and start frame

new_game()

# always remember to check your completed program against the grading rubric