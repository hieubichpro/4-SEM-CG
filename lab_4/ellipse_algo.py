from math import *
from reflection import *
from my_functions import my_round

def middlePointEllipseAlg(xCenter, yCenter, radiusX, radiusY, colour = "#000000", reflect = True):
    pointsArray = []

    sqrRadX = radiusX * radiusX
    sqrRadY = radiusY * radiusY

    limit = round(radiusX / sqrt(1 + sqrRadY / sqrRadX))

    curX = 0
    curY = radiusY
    pointsArray.append([curX + xCenter, curY + yCenter, colour])

    func = sqrRadY - sqrRadX * (radiusY - 1 / 4)
    while curX < limit:
        curX += 1
        
        if func >= 0:
            curY -= 1
            func += sqrRadY * 2 * curX - sqrRadX * 2 * curY + sqrRadY 
            
        else:
            func += sqrRadY * 2 * curX + sqrRadY
            
        pointsArray.append([curX + xCenter, curY + yCenter, colour])

    limit = round(radiusY / sqrt(1 + sqrRadX / sqrRadY))

    curX = radiusX
    curY = 0
    pointsArray.append([curX + xCenter, curY + yCenter, colour])

    func = sqrRadX - sqrRadY * (curX - 1 / 4)
    
    while curY < limit:
        curY += 1
        
        if func >= 0:
            curX -= 1
            func += sqrRadX * 2 * curY - sqrRadY * 2 * curX + sqrRadX
        
        else:
            func += sqrRadX * 2 * curY + sqrRadX
            
        pointsArray.append([curX + xCenter, curY + yCenter, colour])
        
    if reflect:
        reflectPointsX(pointsArray, yCenter)
        reflectPointsY(pointsArray, xCenter)

        return pointsArray


def bresenhamEllipseAlg(xCenter, yCenter, radiusX, radiusY, colour = "#000000", reflect = True):
    pointsArray = []

    curX = 0
    curY = radiusY

    sqrRadX = radiusX * radiusX
    sqrRadY = radiusY * radiusY

    pointsArray.append([curX + xCenter, curY + yCenter, colour])

    D = sqrRadY + sqrRadX * (1 - 2 * radiusY)
    while curY > 0:
        
        if D < 0:
            d1 = 2 * D + sqrRadX * (2 * curY - 1)
            curX += 1
            if d1 >= 0:
                curY -= 1
                D += 2 * sqrRadY * curX - 2 * sqrRadX * curY + sqrRadX + sqrRadY
            else:
                D += 2 * sqrRadY * curX + sqrRadY
                
        elif D > 0:
            d2 = 2 * D - 2 * sqrRadY * curX - sqrRadY
            curY -= 1
            if d2 <= 0:
                curX += 1
                D += 2 * sqrRadY * curX - 2 * sqrRadX * curY + sqrRadX + sqrRadY
            else:
                D += -2 * sqrRadX * curY + sqrRadX
                
        else:
            curX += 1
            curY -= 1
            D += 2 * sqrRadY * curX - 2 * sqrRadX * curY + sqrRadX + sqrRadY
            
        pointsArray.append([curX + xCenter, curY + yCenter, colour])
        
    if reflect:
        reflectPointsY(pointsArray, xCenter)
        reflectPointsX(pointsArray, yCenter)

        return pointsArray


def parameterEllipseAlg(xCenter, yCenter, radiusX, radiusY, colour = "#000000", reflect = True):
    pointsArray = []

    if radiusX > radiusY:
        step = 1 / radiusX
    else:
        step = 1 / radiusY

    i = 0
    while i <= pi / 2:
        curX = my_round(xCenter + radiusX * cos(i))
        curY = my_round(yCenter + radiusY * sin(i))
        pointsArray.append([curX, curY, colour])

        i += step
    if reflect:
        reflectPointsY(pointsArray, xCenter)
        reflectPointsX(pointsArray, yCenter)
        
        return pointsArray


def canonicalEllipseAlg(xCenter, yCenter, radiusX, radiusY, colour = "#000000", reflect = True):
    pointsArray = []

    sqrRadX = radiusX * radiusX
    sqrRadY = radiusY * radiusY
    sqrMix = sqrRadX * sqrRadY

    limitX = my_round(xCenter + sqrRadX / sqrt(sqrRadX + sqrRadY))
    limitY = my_round(yCenter + sqrRadY / sqrt(sqrRadX + sqrRadY))

    for curX in range(xCenter, limitX + 1):
        curY = my_round(yCenter + sqrt(sqrMix - (curX - xCenter) * (curX - xCenter) * sqrRadY) / radiusX)
        pointsArray.append([curX, curY, colour])

    for curY in range(yCenter, limitY + 1):
        curX = my_round(xCenter + sqrt(sqrMix - (curY - yCenter) * (curY - yCenter) * sqrRadX) / radiusY)
        pointsArray.append([curX, curY, colour])

    if reflect:
        reflectPointsX(pointsArray, xCenter)
        reflectPointsY(pointsArray, yCenter)
        
        return pointsArray