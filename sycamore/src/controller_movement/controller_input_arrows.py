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

# adding screen for visuals; initialising surface
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

# creating clock to set FPS
clock = pygame.time.Clock()
FPS = 10


# setting run to true; means pygame is running
run = True

while run:
    # creating a short delay (in ms)
    pygame.time.delay(15)

    # for loop going over the list of events
    for event in pygame.event.get():

        # when QUIT, quits the while-loop
        if event.type == pygame.QUIT:
            run = False
    
    # needs to be outside the for-loop, otherwise no fluid movement
    # actions for buttons pressed
        # pressing right-arrow
    if joystick.get_button(14) and x<800 - obj_width:
        x += 10
        # pressing left-arrow
    if joystick.get_button(13) and x>0:
        x -= 10
        # pressing up
    if joystick.get_button(12) and y<500 - obj_height:
        y += 10
        # pressing down
    if joystick.get_button(11) and y>0:
        y -= 10

    # select background colour (blue) for the screen
        # syntax: surface.fill(color)
    # screen.fill(color=255)
        # or with the RGB color codes:
        # syntax: surface.fill((R,G,B))
    screen.fill((100,100,255))

    # put the object (rectangle) to control on screen
        # syntax: pygame.draw.rect(surface, (colour), (x-position obj, y-position obj, obj-w, obj-h))
    pygame.draw.rect(screen, (0,0,100), pygame.Rect(x, y, obj_width, obj_height))

    # updates the display (when passing arguments, it can be limited to updating only those)
    pygame.display.update()

    clock.tick(FPS)

# closes the window    
pygame.quit()