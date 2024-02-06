import pygame
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
    if apply:
        return scaledColor
    else:
        return (r0, g0, b0)


#variables

colorScale = True
stop = False
colorChoice = (128, 128, 128)

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
            if event.key == pygame.K_a:
            
                colorChoice = (0, 255, 255)
            if event.key == pygame.K_d:
            
                colorChoice = (160, 82, 45)

            if event.key == pygame.K_s:
                colorScale = not colorScale





    #graphics
    screen.fill(colorAvg(255,255, 255, colorChoice, colorScale))
    pygame.draw.circle(screen, (colorAvg(100, 0, 0, colorChoice, colorScale)), [width/3, height/2], 20)
    pygame.draw.circle(screen, (colorAvg(0, 200, 200, colorChoice, colorScale)), [2*width/3, height/3], 20)


    #time between each frame
    pygame.time.wait(dt)
    #updates the frame
    pygame.display.update()