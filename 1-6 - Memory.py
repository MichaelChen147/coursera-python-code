# implementation of card game - Memory
import simplegui
import random

#Establishing global variables
CARDS = [range(8)]*2
EXPOSED = [False]*16
TURNS = 0
CURRENTCARD = []
STATE = 0

# helper function to initialize globals
def new_game():
    global CARDS, EXPOSED, TURNS, CURRENTCARD, STATE
    CARDS = 2 * list(range(8))
    random.shuffle(CARDS)
    EXPOSED = [False]*16
    TURNS = 0
    CURRENTCARD = []
    STATE = 0
    label.set_text("Turns = " + str(TURNS))
    pass  

# define event handlers
def mouseclick(pos):
    global EXPOSED, TURNS, CURRENTCARD, STATE
    cardclicked = pos[0]//50
    if STATE == 0:
            EXPOSED[cardclicked] = True
            CURRENTCARD.append(cardclicked)
            STATE = 1
            TURNS = 1
            
   
    elif STATE == 1:
        if not (cardclicked in CURRENTCARD):
            CURRENTCARD.append(cardclicked)
            STATE = 2
            EXPOSED[cardclicked] = True  
            TURNS += 1
            label.set_text("Turns = " + str(TURNS))
                  
    else:
       if not (cardclicked in CURRENTCARD): 
            if CARDS[CURRENTCARD[-1]] != CARDS[CURRENTCARD[-2]]:
                EXPOSED[CURRENTCARD[-1]]=False
                EXPOSED[CURRENTCARD[-2]]=False
                CURRENTCARD.pop()
                CURRENTCARD.pop()
            STATE = 1
            EXPOSED[cardclicked]=True
            CURRENTCARD.append(cardclicked)
            
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global CARDS
    for i in range(len(CARDS)):
            x_pos = 50 * (i)
            canvas.draw_text(str(CARDS[i]), [x_pos, 70], 80, "White")
            if EXPOSED[i] == False:
                canvas.draw_polygon([(0 + i * 50, 0), 
                                 (0 + i * 50, 100), 
                                 (50 + i * 50, 100), 
                                 (50 + i * 50, 0)], 3, "Black", "Green")
    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric