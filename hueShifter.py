import pygame
pygame.init()
#functions

def shiftColor(naturalColor: int, modifier: int):
    #this one to be used for the color which will not dominate
    highestValue = 255
    newColor = (naturalColor - (highestValue * modifier * 0.01))
    if newColor < 0:
        newColor = 0
    elif newColor > highestValue:
        newColor = highestValue
    return newColor

def moreColor(naturalColor: int, modifier: int):
    #this one to be used for the color that will dominate
    highestValue = 255
    colorDiff = highestValue - naturalColor
    newColor = naturalColor + (0.01 * modifier * colorDiff)
    if newColor < 0:
        newColor = 0
    elif newColor > highestValue:
        newColor = highestValue
    return (newColor)

#variables

redness = 0 #this is a percentage
stop = False
dt = 100
(width, height) = (900, 600)
screen = pygame.display.set_mode((width, height))

#main loop
while ( stop != True):
    for event in pygame.event.get():
        #key inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                #stops the loop
                stop = True
            if event.key == pygame.K_d and redness < 100:
                redness = redness + 5
                print(redness)
            if event.key == pygame.K_a and redness > 0:
                redness = redness - 5
                print(redness)

    #graphics
    screen.fill((shiftColor(255, redness), moreColor(255, redness), shiftColor(255, redness)))
    pygame.draw.circle(screen, (shiftColor(100, redness),moreColor(0, redness), shiftColor(100, redness)), [width/3, height/2], 20)
    pygame.draw.circle(screen, (shiftColor(0, redness), moreColor(100, redness), shiftColor(0, redness)), [2*width/3, height/3], 20)

    #time between each frame
    pygame.time.wait(dt)
    #updates the frame
    pygame.display.update()