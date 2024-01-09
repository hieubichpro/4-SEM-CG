from my_functions import my_round
from reflection import *
from math import sin, cos, sqrt, pi


def middlePointCircleAlg(xCenter, yCenter, radius, colour = "#000000", reflect = True):
    pointsArray = []

    curX = radius
    curY = 0
    # P = 5/4 - radius
    P = 1 - radius
    
    pointsArray.append([curX + xCenter, curY + yCenter, colour])

    while curY < curX:
        curY += 1
        
        if P >= 0:
            curX -= 1
            P += 2 * curY + 1 - 2 * curX
            
        else:
            P += 2 * curY + 1
        
        pointsArray.append([curX + xCenter, curY + yCenter, colour])
    
    if reflect:    
        reflectPointsXY(pointsArray, xCenter, yCenter)
        reflectPointsY(pointsArray, xCenter)
        reflectPointsX(pointsArray, yCenter)
    
        return pointsArray


def bresenhamCircleAlg(xCenter, yCenter, radius, colour = "#000000", reflect = True):
    pointsArray = []

    curX = 0
    curY = radius
    pointsArray.append([curX + xCenter, curY + yCenter, colour])

    D = 2 * (1 - radius)
    
    while curX <= curY:
        if D < 0:
            d1 = 2 * D + 2 * curY - 1
            curX += 1
            if d1 >= 0 :
                curY -= 1
                D += 2 * (curX - curY + 1)
            else:
                D += 2 * curX + 1
                
        elif D > 0:
            d2 = 2 * D - 2 * curX - 1
            curY -= 1
            if d2 <= 0:
                curX += 1
                D += 2 * (curX - curY + 1)
            else:
                D += -2 * curY + 1
                
        else:
            curX += 1
            curY -= 1
            D += 2 * (curX - curY + 1)
            
        pointsArray.append([curX + xCenter, curY + yCenter, colour])
    if reflect:
        reflectPointsXY(pointsArray, xCenter, yCenter)
        reflectPointsY(pointsArray, xCenter)
        reflectPointsX(pointsArray, yCenter)
        
        return pointsArray


def parameterCircleAlg(xCenter, yCenter, radius, colour = "#000000", reflect = True):
    pointsArray = []
    angleStep = 1 / radius
    i = 0
    
    while i <= pi / 4:
        curX = my_round(xCenter + radius * cos(i))
        curY = my_round(yCenter + radius * sin(i))
        pointsArray.append([curX, curY, colour])
        i += angleStep
    if reflect:
        reflectPointsXY(pointsArray, xCenter, yCenter)
        reflectPointsY(pointsArray, xCenter)
        reflectPointsX(pointsArray, yCenter)
    
        return pointsArray


def canonicalCircleAlg(xCenter, yCenter, radius, colour = "#000000", reflect = True):
    pointsArray = []
    
    xLimit = my_round(xCenter + radius / sqrt(2)) + 1
    
    for curX in range(xCenter, xLimit):
        curY = my_round(yCenter + sqrt(radius * radius - (curX - xCenter) * (curX - xCenter)))
        pointsArray.append([curX, curY, colour])
    
    if reflect:
        reflectPointsXY(pointsArray, xCenter, yCenter)
        reflectPointsY(pointsArray, xCenter)
        reflectPointsX(pointsArray, yCenter)
    
        return pointsArray