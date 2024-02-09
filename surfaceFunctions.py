import pygame
import math
import numpy
from PIL import Image
from random import random


def drawPoint(pt: list, origin: list, screenOrigin: list, pic, lightSource: list):

    #The max light value we can have is 255, sooooo...
    maxLight = 255
    x = pt[0]
    y = pt[1]
    z = pt[2]
    cameraDistance = 1 # keep at 1 or above to prevent crashes (definitely above zero)
    #formula: 1/[(0.01z)+1]
    xCoord = screenOrigin[0] + ((origin[0] + x) * 1/((0.001 * z)+cameraDistance))
    yCoord = screenOrigin[1] - ((origin[1] + y) * 1/((0.001 * z)+cameraDistance))

    lightX = lightSource[0]
    lightY = lightSource[1]
    lightZ = lightSource[2]
    lightStrength = lightSource[3]

    a = lightX - x
    b = lightY - y
    c = lightZ - z

    lightDist = math.sqrt(a**2 + b**2 + c**2)

    diffusePercent = lightStrength / lightDist
    if diffusePercent > 1:
        diffusePercent = 1

    lightLevel = math.ceil(diffusePercent**2 * maxLight)

    if 0 < xCoord < pic.width and 0 < yCoord < pic.height:
        pic.load()[xCoord, yCoord] = lightLevel

def drawLine(start: list, end: list, origin: list, screenOrigin: list, pic, density: float, lightSource: list):
    stepSizeX = (end[0] - start[0])/density
    stepSizeY = (end[1] - start[1])/density
    stepSizeZ = (end[2] - start[2])/density
    for i in range(density):
        currentPointX = (start[0] + (stepSizeX * i))
        currentPointY = (start[1] + (stepSizeY * i))
        currentPointZ = (start[2] + (stepSizeZ * i))
        currentPoint = [currentPointX, currentPointY, currentPointZ]
        drawPoint(currentPoint, origin, screenOrigin, pic, lightSource)

def drawFace(start: list, end: list, pivot:list, origin: list, screenOrigin: list, pic, density: float, lightSource: list, surfNormal: list):
    stepSizeX = (end[0] - start[0])/density
    stepSizeY = (end[1] - start[1])/density
    stepSizeZ = (end[2] - start[2])/density

    triCenterX = (start[0] + end[0] + pivot[0])/3
    triCenterY = (start[1] + end[1] + pivot[1])/3
    triCenterZ = (start[2] + end[2] + pivot[2])/3
    
    a = (triCenterX - lightSource[0])
    b = (triCenterY - lightSource[1])
    c = (triCenterZ - lightSource[2])

    lightDistToCenter = math.sqrt(a**2 + b**2 + c**2)
    lightVecNormal = [a/lightDistToCenter, b/lightDistToCenter, c/lightDistToCenter]
    magLVN = math.sqrt(lightVecNormal[0]**2 + lightVecNormal[1]**2 + lightVecNormal[2]**2)
    magSN = math.sqrt(surfNormal[0]**2 + surfNormal[1]**2 + surfNormal[2]**2)

    dotProduct = -((surfNormal[0] * lightVecNormal[0]) + (surfNormal[1] * lightVecNormal[1]) + (surfNormal[2] * lightVecNormal[2]))
    print(dotProduct)


    newLightSource = [0, 0, 0, 0]
    newLightSource[0], newLightSource[1], newLightSource[2], newLightSource[3] = [lightSource[0], lightSource[1], lightSource[2], lightSource[3]]
    newLightSource[3] = lightSource[3] * dotProduct



    for i in range(density):
        currentPointX = (start[0] + (stepSizeX * i))
        currentPointY = (start[1] + (stepSizeY * i))
        currentPointZ = (start[2] + (stepSizeZ * i))
        currentPoint = [currentPointX, currentPointY, currentPointZ]
        drawLine(pivot, currentPoint, origin, screenOrigin, pic, density, newLightSource)
