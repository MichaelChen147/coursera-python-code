# Implementation of classic arcade game Pong

# Importing simplegui and random

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
paddle_width = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = paddle_width / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
left = False
right = True

# initializing other globals

paddle_pos = HEIGHT/2
paddle_pos2 = HEIGHT/2
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [2, 3]
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left

def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    ball_vel[1] = -random.randrange(60, 180)/60
    if direction == True:
        ball_vel[0] = random.randrange(120, 240)/60
    else:
        ball_vel[0] = -random.randrange(120, 240)/60

# define event handlers
def new_game():
    global paddle_pos, paddle_pos2, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle_pos = HEIGHT/2
    paddle_pos2 = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(left)

def draw(c):
    global score1, score2, paddle_pos, paddle_pos2, ball_pos, ball_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([paddle_width, 0],[paddle_width, HEIGHT], 1, "White")
    c.draw_line([WIDTH - paddle_width, 0],[WIDTH - paddle_width, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[0] >= WIDTH - BALL_RADIUS:
        if ball_pos[1] > (paddle_pos2 + HALF_PAD_HEIGHT) or ball_pos[1] < (paddle_pos2 - HALF_PAD_HEIGHT):
           score1 = score1 + 1
           spawn_ball(left)
        else:
            ball_vel[0] =- ball_vel[0] * 1.1
            
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]    
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1]=-ball_vel[1] 
    if ball_pos[0] <= BALL_RADIUS:
        if ball_pos[1] > (paddle_pos + HALF_PAD_HEIGHT) or ball_pos[1] < (paddle_pos - HALF_PAD_HEIGHT):
           score2 = score2 + 1
           spawn_ball(right)  
        else:
            ball_vel[0] =- ball_vel[0] * 1.1
            
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle_pos += paddle1_vel
    if paddle_pos <= HALF_PAD_HEIGHT:
        paddle_pos = HALF_PAD_HEIGHT
    elif paddle_pos >= (HEIGHT - HALF_PAD_HEIGHT):
        paddle_pos = (HEIGHT - HALF_PAD_HEIGHT)
        
    paddle_pos2 += paddle2_vel
    if paddle_pos2 <= HALF_PAD_HEIGHT:
        paddle_pos2 = HALF_PAD_HEIGHT
    elif paddle_pos2 >= (HEIGHT - HALF_PAD_HEIGHT):
        paddle_pos2 = (HEIGHT - HALF_PAD_HEIGHT)    
    
    # draw paddles
    c.draw_line((0, paddle_pos + HALF_PAD_HEIGHT), (0, paddle_pos - HALF_PAD_HEIGHT), (paddle_width + 8), 'white')
    c.draw_line((600, paddle_pos2 + HALF_PAD_HEIGHT), (600, paddle_pos2 - HALF_PAD_HEIGHT), (paddle_width + 8), 'white')
    # draw scores
    c.draw_text(str(score1), (200, 60), 60, 'White')
    c.draw_text(str(score2), (360, 60), 60, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 5
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += acc
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel -= acc
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel -= acc 
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += acc 
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', new_game)


# start frame
new_game()
frame.start()
