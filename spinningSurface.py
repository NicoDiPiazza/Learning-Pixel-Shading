import pygame
import math
import numpy
from PIL import Image

pygame.init()



#functions
def drawPoint(pt: list, origin: list, screenOrigin: list, pic):
    x = pt[0]
    y = pt[1]
    z = pt[2]
    cameraDistance = 1 # keep at 1 or above to prevent crashes (definitely above zero)
    #formula: 1/[(0.01z)+1]
    xCoord = screenOrigin[0] + ((origin[0] + x) * 1/((0.001 * z)+cameraDistance))
    yCoord = screenOrigin[1] - ((origin[1] + y) * 1/((0.001 * z)+cameraDistance))

    if 0 < xCoord < pic.width and 0 < yCoord < pic.height:
        pic.load()[xCoord, yCoord] = 255

def drawLine(start: list, end: list, origin: list, screenOrigin: list, pic, density: float):
    stepSizeX = (end[0] - start[0])/density
    stepSizeY = (end[1] - start[1])/density
    stepSizeZ = (end[2] - start[2])/density
    for i in range(density):
        currentPointX = (start[0] + (stepSizeX * i))
        currentPointY = (start[1] + (stepSizeY * i))
        currentPointZ = (start[2] + (stepSizeZ * i))
        currentPoint = [currentPointX, currentPointY, currentPointZ]
        drawPoint(currentPoint, origin, screenOrigin, pic)

def drawFace(start: list, end: list, pivot:list, origin: list, screenOrigin: list, pic, density: float):
    stepSizeX = (end[0] - start[0])/density
    stepSizeY = (end[1] - start[1])/density
    stepSizeZ = (end[2] - start[2])/density
    for i in range(density):
        currentPointX = (start[0] + (stepSizeX * i))
        currentPointY = (start[1] + (stepSizeY * i))
        currentPointZ = (start[2] + (stepSizeZ * i))
        currentPoint = [currentPointX, currentPointY, currentPointZ]
        drawLine(pivot, currentPoint, origin, screenOrigin, pic, density)

#variables
stop = False
dt = 100
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))
img = Image.new('L', [width, height], 0)
screenCenterX = width/2
screenCenterY = height/2
screenCenter = [screenCenterX, screenCenterY]

#making this so that in theory any shape defined relative to a set position in 3D space will be anchored to it, in case the camera ceases to
#   be fixed, and moves relative to the anchor position (format: [x, y, z]) (lower Ys are lower on the screen)
origin = [0, 0, 0]



shapeHeight = 400
shapeWidth = 400

pointOne = [0, 50, 0]
pointTwo = [-50, -50, 0]
pointThree = [50, -50, 0]
normVec = 0
density = 25

#main loop
while ( stop != True):
    
    for event in pygame.event.get():
        #key inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                #stops the loop
                stop = True

# function for using z distance to know how much the point should be moved toward the center, where z is the distance
#                from the camera plus some constant, and x and y are defined relative to the center of the screen:
#                   [1/(z+1)] * (x or y)

#the position of each point on the surface should be given in 3D space (x, y, z) (z is depth into the screen) 
#(as z gets larger, the shape's y approaches horizon, x gets closer to center)
#Since it is spinning, y can be held constant, while x and z will be given by cos and sin
#every surface needs the corners (as many as there are) and the normal vector
#to calculate the light level of a given point on the surface, there are steps
#1: if normal vector is away from camera, then skip lighting the surface
#2: calculate theta between source of light and normal vector (calculate once, this changes once per surface)
#3: use hypotenuse to calculate distance from light source (calculated every point on the surface, as this changes each point)
#4: multiply distance strength by cos(theta); you have your light level
#5: use z to figure out how much to distort x and y, those are the pix coordinates. And yes, this does mean some redundancy
#       relighting each pixel several times, as multiple integer-wise points interpolated between the corners will round to
#       the same pixel coordinate. This can be optimized by finding the pixel positions of the corners and deducing the max
#       width and height of the shape on screen, and then using those to find the ratio such that each pixel is checked less,
#       using shapeWidth/screenWidth = stepWidth

    pointOne = [0, shapeHeight/2, 0]
    pointTwo = [(shapeWidth/2) * math.cos(normVec), -shapeHeight/2, (shapeWidth/2) * math.sin(normVec)]
    pointThree = [(-shapeWidth/2) * math.cos(normVec), -shapeHeight/2, (-shapeWidth/2) * math.sin(normVec)]
    normVec = normVec + 0.2

    if abs(normVec) > math.pi * 2:
        normVec = 0


    img = Image.new('L', [width, height], 0)


    drawFace(pointOne, pointTwo, pointThree, origin, screenCenter, img, density)
    drawFace(pointThree, pointOne, pointTwo, origin, screenCenter, img, density)
    drawFace(pointTwo, pointThree, pointOne, origin, screenCenter, img, density)


    img.save('square.jpg')
    square = pygame.image.load('square.jpg')

#graphics
    
    
    screen.blit(square, (0, 0))
    


 #time between each frame
    pygame.time.wait(dt)
    #updates the frame
    pygame.display.update()
