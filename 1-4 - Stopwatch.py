# template for "Stopwatch: The Game"
import simplegui

# define global variables
integer = 0
successful_stops = 0
total_stops = 0
tries = "0/0"

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global integer
    minutes = int(integer/600.0)
    seconds = int(integer/10)%10
    tenseconds = int(integer/100)%6
    miliseconds = int(integer)%10
    return str(minutes) + ":" + str(tenseconds) + str(seconds) + "." + str(miliseconds)
    
# define event handlers for buttons; "Start", "Stop", "Reset"

def timer_start():
    timer.start()
    
# timer_stop checks in the timer is running, stops the
#timer and changes players score
    
def timer_stop():
    global tries, successful_stops, total_stops
    if timer.is_running():
        timer.stop()
        if integer % 10 == 0: 
            successful_stops += 1
            total_stops += 1 
            tries = str(successful_stops) + "/" + str(total_stops)
            return tries
        else:
            total_stops += 1
            tries = str(successful_stops) + "/" + str(total_stops)
            return tries
        
def timer_reset():
    global integer, tries
    timer.stop()
    integer = 0
    tries = "0/0"

# define event handler for timer with 0.1 sec interval

def timer_handler():
    global integer
    integer += 1
    return integer


# define draw handler

def draw_handler(canvas):
    canvas.draw_text(format(integer), [100, 100], 40, 'Green')
    canvas.draw_text(tries, [230, 30], 30, "White")  

# create frame
# register event handlers

frame = simplegui.create_frame('Testing', 300, 200)
frame.set_draw_handler(draw_handler)
start = frame.add_button('Start', timer_start)
stop = frame.add_button('Stop', timer_stop)
reset = frame.add_button('Reset', timer_reset)
timer = simplegui.create_timer(100, timer_handler)

# start frame

frame.start()


# Please remember to review the grading rubric
