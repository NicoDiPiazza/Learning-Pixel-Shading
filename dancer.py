import pygame
import numpy
import math
from random import random
from PIL import Image


pygame.init()

#function

def direct(num: float):
    stepSize = 5
    a = random() * 3 - 1
    b = math.floor(a) * stepSize
    newNum = num + b
    return(newNum)


#variables

stop = False
dt = 100
width = 500
height = 500
screen = pygame.display.set_mode((width, height))

xCoord = width/2
yCoord = height/2
tailLength = 10


img = Image.new('L', [width, height], 0)

tail = []

for i in range(tailLength):
    tail.append([xCoord, yCoord])
    print (tail)


#main loop
while ( stop != True):
    
    for event in pygame.event.get():
        #key inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                #stops the loop
                stop = True


    

    img.load()[tail[0][0], tail[0][1]] = 0
    tail.pop(0)
    img.load()[xCoord, yCoord] = 100
    xCoord = direct(xCoord)
    yCoord = direct(yCoord)
    tail.append([xCoord, yCoord])
    img.load()[xCoord, yCoord] = 250

    img.save('frame.jpg')
    frame = pygame.image.load('frame.jpg')

#graphics
    
    screen.blit(frame, (0, 0))
    


 #time between each frame
    pygame.time.wait(dt)
    #updates the frame
    pygame.display.update()
