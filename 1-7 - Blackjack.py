# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
# Note: I added gamestate, inspired by memory game, to
#help with my implementation of Blackjack
in_play = False
outcome = ""
message = ""
gamestate = ""
score = 0
player_hand = []
dealer_hand = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
        pass	# create Hand object

    def __str__(self):
        return str([str(i) for i in self.hand])

    def add_card(self, card):
        self.hand.append(card)
        return self.hand
        pass	# add a card object to a hand

    def get_value(self):
            hand_value = 0
            aces = False
            for card in self.hand:
                hand_value = hand_value + VALUES[card.get_rank()]
                if hand_value > 21:
                    return "Busted"
                    in_play = False
                    gamestate = 1
                if "A" in [self.hand[i].get_rank() for i in range(len(self.hand))]:
                    aces = True
                else:
                    aces = False     
            if aces and ((hand_value + 10) <= 21):
                hand_value = hand_value + 10
            else:
                hand_value = hand_value           
            
            return hand_value # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for card in self.hand:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0] + 20
            pass	# draw a hand on the canvas, use the draw method for cards

        
# define deck class 
class Deck:
    def __init__(self):         
        self.deck = [Card(s,r) for s in SUITS for r in RANKS]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        self.shuffle();
        return self.deck.pop()
        pass	#deal a card object from the deck
    
    def __str__(self):
        return "Deck contains " + " ".join(str(card) for card in self.deck)
        pass	# return a string representing the deck 



#define event handlers for buttons
#define event handler for 'deal' button
def deal():
    global gamestate, message, outcome, in_play, player_hand, dealer_hand
    in_play = True
    gamestate = 0
    outcome = ""
    message = "Hit or stand?"
    player_hand = []
    dealer_hand = []
    my_deck = Deck()
    my_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(my_deck.deal_card())
    player_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())   

#define event handler for 'hit' button, including some
#essential game logic
# if the hand is in play, hit the player
# if busted, assign a message to outcome, update in_play and score
def hit():
    global score, message, outcome, player_hand, in_play, gamestate, message
    my_deck = Deck()
    if player_hand.get_value() > 21 and gamestate == 0:
        outcome = "You busted."
        message = "New deal?"
        score -= 1
        in_play = False
        gamestate = 1
    else:
        if player_hand.get_value() <= 21 and gamestate == 0:
            player_hand.add_card(my_deck.deal_card())
            if player_hand.get_value() > 21:
                outcome = "You busted."
                message = "New deal?"
                score = score - 1
                in_play = False
                gamestate = 1
                pass

# replace with your code below
# if hand is in play, repeatedly hit dealer until his hand has value 17 or more
# assign a message to outcome, update in_play and score
       
def stand():
    global outcome, message, player_hand, dealer_hand, in_play, gamestate, score
    my_deck = Deck()
    if player_hand.get_value() > 21:
        outcome = player_hand.get_value()
    else:
        while dealer_hand.get_value() <= 17:
            dealer_hand.add_card(my_deck.deal_card())
        if dealer_hand.get_value() > 21:
                outcome = "Dealer busted. You won!"
                in_play = False
                gamestate = 0
                score += 1    
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                outcome = "You won!"
                in_play = False
                gamestate = 0
                score += 1     
            else:
                    outcome = "Dealer won."
                    in_play = False
                    gamestate = 1
                    score -= 1
                    message = "New deal?"            
                    pass	

# draw handler    
def draw(canvas):
    global player_hand, dealer_hand, in_play
    player_hand.draw(canvas,[120,400])
    dealer_hand.draw(canvas,[120,150])
    canvas.draw_text('Blackjack', (20, 40), 40, 'White')
    canvas.draw_text('Player', (120, 370), 25, 'Black')
    canvas.draw_text('Dealer', (120, 120), 25, 'Black')
    canvas.draw_text(message, (300, 370), 25, 'Black')
    canvas.draw_text(outcome, (300, 120), 25, 'Black')
    canvas.draw_text('Score: ' + str(score), (450, 40), 30, 'White')
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (156, 199), (CARD_BACK_SIZE[0], CARD_BACK_SIZE[1]))
        


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric