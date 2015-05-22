# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
angle_vel = 0.1
friction = 0.96
acc = 0.1
started = False
collide = False
highscore = [0]


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://metroid.retropixel.net/mprime/music/mp13.mp3")
soundtrack.set_volume(.8)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

lives_sound = simplegui.load_sound("http://metroid.retropixel.net/metroid3/music/sm14.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, ((self.image_center[0]) * 3, self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.vel[0] = self.vel[0] * friction
        self.vel[1] = self.vel[1] * friction
               
        self.pos[0]=(self.pos[0]+self.vel[0])%WIDTH
        self.pos[1]=(self.pos[1]+self.vel[1])%HEIGHT
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.angle += self.angle_vel
        
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * 0.2
            self.vel[1] += forward[1] * 0.2
    
    def angleveldec(self, angle, angle_vel):
        self.angle_vel = -(angle_vel)
        return self.angle_vel
    
    def anglevelinc(self, angle, angle_vel):
        self.angle_vel = (angle_vel)
        return self.angle_vel
        
    def thrustcheck(self, thrust):
        self.thrust = thrust
        if thrust:
            self.vel[0] += acc
            ship_thrust_sound.play()
        else:
            self.vel[0] * friction
            ship_thrust_sound.rewind()
            
            return my_ship.vel
        
    def getpos(self):
        return self.pos
    
    def getrad(self):
        return self.radius
        
    def missile(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        init_vel = 4
        missile_pos_x = self.pos[0] + self.radius * math.cos(self.angle)
        missile_pos_y = self.pos[1] + self.radius * math.sin(self.angle)
        missile_vel_x = forward[0] * init_vel + self.vel[0]
        missile_vel_y = forward[1] * init_vel + self.vel[1]
        
        missile_group.add(Sprite([missile_pos_x, missile_pos_y], [missile_vel_x,missile_vel_y], 0, 0, missile_image, missile_info, missile_sound))
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        if self.animated:
            if self.age < self.lifespan:
                image_center = [self.image_center[0] + (self.age % self.lifespan) * self.image_size[0], self.image_center[1]]
                canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, self.angle)    
            else:
                pass
                   
    def update(self):
        global soundage
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        
        self.pos[0]=(self.pos[0]+self.vel[0])%WIDTH
        self.pos[1]=(self.pos[1]+self.vel[1])%HEIGHT
        
        self.age += 1
        if self.age > self.lifespan:
            return True
            self.age = 0
        else:
            return False
    
    def getpos(self):
        return self.pos
    
    def getrad(self):
        return self.radius
    
    def collide(self, other_object):
        global lives
        p = self.getpos()
        rr = self.getrad()
        q = other_object.getpos()
        otherrad = other_object.getrad()
        distance = math.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)
        if distance <= (rr + otherrad):
            return True 
        else:
            return False

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    soundtrack.play()
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0        
        
def draw(canvas):
    global time, rock_group, lives, highscore, score, started, soundage
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
 
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    process_sprite_group(rock_group, canvas)
    if group_collide(rock_group, my_ship):
        lives -= 1
    if lives == 0:
        highscore.append(score)
        if started:
            lives_sound.play()
        started = False
        rock_group = set([])
        if highscore[0] > highscore[1]:
            highscore.pop(1)
            canvas.draw_text("Highscore: " + str(highscore[0]), (300, 500), 40, 'White')
        else:
            highscore.pop(0)
            canvas.draw_text("Highscore: " + str(highscore[0]), (300, 500), 40, 'White')
            
    if group_group_collide(missile_group, rock_group):
        score = score + 10
            
    #draw score and lives    
    canvas.draw_text("Lives: " + str(lives), (80, 50), 22, 'White')
    canvas.draw_text("Score: " + str(score), (WIDTH - 150, 50), 22, 'White')    
    
        
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        soundtrack.rewind()
        soundtrack.pause()

#keydown handler and keyup handler
def keydown(key):
    global angle_vel
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        my_ship.thrustcheck(my_ship.thrust)
    if key == simplegui.KEY_MAP['left']:
        my_ship.angleveldec(my_ship.angle, angle_vel)
    if key == simplegui.KEY_MAP['right']:
        my_ship.anglevelinc(my_ship.angle, angle_vel)
    if key == simplegui.KEY_MAP['space']:
        my_ship.missile()
        
def keyup(key):
    global angle_vel
    if key == simplegui.KEY_MAP['left']:
        my_ship.angleveldec(my_ship.angle, angle_vel * 0)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angleveldec(my_ship.angle, angle_vel * 0)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        my_ship.thrustcheck(my_ship.thrust)    
 
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, score
    a_rock = Sprite([random.randrange(0, WIDTH), random.randrange(0, HEIGHT)], [random.randrange(0,5), random.randrange(0,5)], 0.5, 0.05, asteroid_image, asteroid_info)
    a_rock.angle_vel = random.random() * 0.2 - 0.1
    if started:
        if len(rock_group) < 12:
            d1 = dist(a_rock.pos, my_ship.pos)
            if d1 < 2 * (a_rock.radius + my_ship.radius):
                a_rock.pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            else:
                rock_group.add(a_rock)
    return rock_group

#group and group group processors and collision detectors
def process_sprite_group(takeset, canvas):
    global age
    for item in takeset:
        item.draw(canvas)
        item.update()
    for missile in list(missile_group):
        if missile.update():
            missile_group.remove(missile)
    for explosion in list(explosion_group):
        if explosion.update():
            explosion_group.remove(explosion)
    return takeset  
        
 
def group_collide(group, otherobject):
    return_state = False
    for rock in list(group):
        if rock.collide(otherobject):
            group.remove(rock)
            return_state = True
            expl = Sprite(rock.getpos(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(expl)
    return return_state     
        
def group_group_collide(missilegroup, rockgroup):
    hits = 0
    for missile in list(missilegroup):
        if group_collide(rockgroup, missile):
            missilegroup.discard(missile)
            hits += 1
    return hits       
        
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])


# register handlers
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
