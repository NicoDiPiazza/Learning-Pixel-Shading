import pygame
import math
import numpy
from PIL import Image
from random import random
from surfaceFunctions import drawFace

pygame.init()



#functions

def draw3D(points: list, origin: list, screenOrigin: list, pic, density: float, lightSource: list, surfNormal: list):

    for i in range(len(points) - 1):

        if i < len(points) - 2:
            drawFace(points[i], points[i+1], points[i+2], origin, screenOrigin, pic, density, lightSource, surfNormal)
        
        elif i < len(points) - 1:
            drawFace(points[i], points[i+1], points[0], origin, screenOrigin, pic, density, lightSource, surfNormal)
        else:
            drawFace(points[i], points[0], points[1], origin, screenOrigin, pic, density, lightSource, surfNormal)



#variables
stop = False
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))
img = Image.new('L', [width, height], 0)
screenCenterX = width/2
screenCenterY = height/2
screenCenter = [screenCenterX, screenCenterY]

clock = pygame.time.Clock()

#making this so that in theory any shape defined relative to a set position in 3D space will be anchored to it, in case the camera ceases to
#   be fixed, and moves relative to the anchor position (format: [x, y, z]) (lower Ys are lower on the screen)
origin = [0, 0, 0]



shapeHeight = 400
shapeWidth = 400

pointOne = [0, 50, 0]
pointTwo = [-50, -50, 0]
pointThree = [50, -50, 0]
normVec = [0, 0, 1]
thetaNV = 0


density = 25
sun = [-300, 300, 400, 1000] #x, y, z, strength
sunRadius = 50


#main loop
while ( stop != True):
    
    for event in pygame.event.get():
        #key inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                #stops the loop
                stop = True

    mouseX, mouseY = pygame.mouse.get_pos()


    sun[0], sun[1] = mouseX - width/2, -(mouseY - height/2)


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


#note that while the normal vector of the surface is constant, the direction from which light is hitting changes slightly at each
#       point, because the light is from a point, not a plane. As such, as, for ex. you go lower on the plane, the angle from the point
#       of light to the current point changes because the coordinates of the point changes.
#           However, note additionally that as the size of faces goes down and poly counts go up, the change of angle goes down,
#       and this means it is not as neccessary to calculate the dot product of the angles for every point, and to optimize (even though
#       it isn't as accurate in lighting) we can calculate for the center of the face, and just apply that light vector to every point.
#       similarly, in any instance where the light source is sufficiently far away, such as the sun, then the angle difference becomes
#       equally negligable. While this is a sad sacrifice to make, and should be remedied if possible, but in the meantime, it is ok.


    pointOne = [0, shapeHeight/2, 0]
    pointTwo = [(shapeWidth/2) * math.cos(thetaNV), -shapeHeight/2, (shapeWidth/2) * math.sin(thetaNV)]
    pointThree = [(-shapeWidth/2) * math.cos(thetaNV), -shapeHeight/2, (-shapeWidth/2) * math.sin(thetaNV)]
    thetaNV = thetaNV + 0.2
    normVec[0] = math.sin(thetaNV)
    normVec[2] = math.cos(thetaNV)

    if abs(thetaNV) > math.pi * 2:
        thetaNV = 0
        normVec[0] = 0
        normVec[2] = 1


    img = Image.new('L', [width, height], 0)

    #if normVec[2] > 0:
    drawFace(pointOne, pointTwo, pointThree, origin, screenCenter, img, density, sun, normVec)
    drawFace(pointThree, pointOne, pointTwo, origin, screenCenter, img, density, sun, normVec)
    drawFace(pointTwo, pointThree, pointOne, origin, screenCenter, img, density, sun, normVec)

    for i in range(500):

        xOffset = random() * sunRadius - (sunRadius/2)
        yOffset = random() * sunRadius - (sunRadius/2)
        xCoord = screenCenter[0] + sun[0] + xOffset
        yCoord = screenCenter[1] - sun[1] + yOffset
        if 0 < xCoord < img.width and 0 < yCoord < img.height: 
            img.load()[xCoord, yCoord] = 255


    img.save('square.jpg')
    square = pygame.image.load('square.jpg')

#graphics
    
    
    screen.blit(square, (0, 0))


    


 #time between each frame
    clock.tick()
    #print(clock.get_fps())
    # currently at 23.69
    # linearly interpolating light levels takes it down to 19.84
    #or not, it's really fluxuating. Regardless, there is not a significant change in frame rate with linear interpolation :(
    
    #updates the frame
    pygame.display.update()
