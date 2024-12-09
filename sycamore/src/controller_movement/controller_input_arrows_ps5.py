import pygame
import sys

# initialise pygame and joystick modules
pygame.init()
pygame.joystick.init()

# checking whether joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    sys.exit()
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Connected joystick: " + joystick.get_name())

# creating screen: MIGHT NEED TO CHANGE VALUES FOR RPI
        # syntax: pygame.display.set_mode((screen_width, screen_height))
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))


# variables below needed for control function and not moving out of frame

# current position of the object to be controlled:
x = 0
y = 0
# setting dimensions of object
obj_width = 50
obj_height = 50

step_size = 2 # setting the step size
threshold = 0.1 # setting threshold for movement of joystick

# creating clock to set FPS: MIGHT NEED TO CHANGE VALUE FOR RPI
clock = pygame.time.Clock()
FPS = 10


# setting run to true; means pygame is running
run = True

while run:
    # creating a short delay (in ms); needed to set small steps; otherwise the step is entire screen
    pygame.time.delay(15)

    # for loop going over the list of events
    for event in pygame.event.get():

        # when the window is closed, quit the while-loop
        if event.type == pygame.QUIT:
            run = False
        # maybe useful for rpi; quit while-loop when Esc-key is pressed
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        

    # finding which arrow key is pressed of joystick
    arrow_key = joystick.get_hat() 

    # (-1,0) means the left key is pressed
    if arrow_key(-1,0) and x > 0:
        x -= 5
    # (1,0) means the right key is pressed
    if arrow_key(1,0) and x < screen_width-obj_width:
        x += 5
    # (0,1) means the up key is pressed
    if arrow_key(0,1) and y < screen_height-obj_height:
        y += 5
    # (0,-1) means the down key is pressed
    if arrow_key(0,-1) and y > 0:
        y -= 5
    

    # select background colour (blue) for the screen
    screen.fill((100,100,255)) # syntax: surface.fill((R,G,B))

    # put the object (rectangle) to control on screen
        # syntax: pygame.draw.rect(surface, (colour), (x-position obj, y-position obj, obj-w, obj-h))
    pygame.draw.rect(screen, (0,0,100), pygame.Rect(x, y, obj_width, obj_height))

    # updates the display (when passing arguments, it can be limited to updating only those)
    pygame.display.update()

    clock.tick(FPS)

# closes the window    
pygame.quit()