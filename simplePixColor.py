import pygame
import math
from PIL import Image
import numpy

pygame.init()

#Functions

def colorAvg(r0: int, g0: int, b0: int, selectedRGB: list, apply: bool):
    highestValue = 255
    #C.A. is the average of the three rgb values
    CA = (r0 + g0 + b0)/3
    darkness = CA / highestValue
    #H.S. is highest of the three highest selected rgb values
    HSRGB = max(selectedRGB)

    absoluteRatio = highestValue / HSRGB
    #newSRGB is the rgb values that we will base all our other colors off of
    newSRGB = [x * absoluteRatio for x in selectedRGB]

    scaledColor = [x * darkness for x in newSRGB]

    # Some things are too fancy to accept floats in rgb, so now this
    flooredScaledColor = [0, 0, 0]

    for i in range(len(scaledColor)):
        flooredScaledColor[i] = math.floor(scaledColor[i])

    if apply:
        return flooredScaledColor
    else:
        return (r0, g0, b0)


#variables

colorScale = True
stop = False
colorChoice = (160, 82, 45)

dt = 100


chosen_image = 'SugarbeetSmall.jpg'

tester = Image.open(chosen_image)
pix = tester.load()

#print (pix[200, 200])

(width, height) = tester.size
screen = pygame.display.set_mode((width + 20, height + 20))


#recoloring each pixel

for i in range(1, (width * height)):
    xCoord = (i - 1) % width
    yCoord = math.floor(i / width)
    (rP, gP, bP) = pix[xCoord, yCoord]
    pix[xCoord, yCoord] = tuple(colorAvg(rP, gP, bP, colorChoice, True))


print (colorAvg(rP, gP, bP, colorChoice, True))


tester.save('newTestImage.jpg')


gameTester = pygame.image.load('newTestImage.jpg')


#main loop
while ( stop != True):
    
    for event in pygame.event.get():
        #key inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                #stops the loop
                stop = True
            if event.key == pygame.K_a:
            
                colorChoice = (0, 255, 255)
            if event.key == pygame.K_d:
            
                colorChoice = (160, 82, 45)

            if event.key == pygame.K_s:
                colorScale = not colorScale





    #graphics
    screen.blit(gameTester, (10, 10))

 #time between each frame
    pygame.time.wait(dt)
    #updates the frame
    pygame.display.update()
