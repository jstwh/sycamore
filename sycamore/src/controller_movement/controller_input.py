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
        

    # finding current position of joystick (float can range from -1 to 1)
    x_axis = joystick.get_axis(0) # moving left joystick along x-axis (left-right)
    y_axis = joystick.get_axis(1) # moving left joystick along y-axis (up-down)


    # introducing threshold to get rid of it moving on its own
    if abs(x_axis) >= threshold or abs(y_axis) >= threshold:

        # if the new x-position is within the frame, update x
        if 0 < x + (x_axis * step_size) < screen_width-obj_width:
            x += x_axis * step_size

        # if the new y-position is within the frame, update y
        if 0 < y + (y_axis * step_size) < screen_height-obj_height:
            y += y_axis * step_size
        

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