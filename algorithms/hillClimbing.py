from algorithms.randomCenters import algoRandomCenters
from numpy import array, amin, amax, sort, zeros

def calcDists(nColors, nCenters, nPoints, graph, curCenters):
    centerDists = zeros((nColors, amax(nPoints), nCenters))
    for pCol in range(nColors):
        for pId in range(nPoints[pCol]):
            for cPos in range(len(curCenters)):
                cCol, cId = curCenters[cPos]
                centerDists[pCol][pId][cPos] = graph[pCol][pId][cCol][cId]
    return centerDists

def updateDists(nColors, nPoints, graph, curCenters, centerDists, cPos, newCCol, newCId):
    curCenters[cPos] = [newCCol, newCId]
    for pCol in range(nColors):
        for pId in range(nPoints[pCol]):
            centerDists[pCol][pId][cPos] = graph[pCol][pId][newCCol][newCId]

def calcRadius(nColors, nPoints, p, centerDists):
    radius = 0
    for col in range(nColors):
        if p[col] > 0:
            smallDists = zeros(nPoints[col])
            for pId in range(nPoints[col]):
                smallDists[pId] = amin(centerDists[col][pId])
            smallDists = sort(smallDists)
            radius = max(radius, smallDists[p[col]-1])
    return radius

def algoHillClimbing(nColors, nCenters, nPoints, p, graph):
    curCenters = algoRandomCenters(nColors, nCenters, nPoints, p, graph)
    assert amin(curCenters) > -1, "There should be k centers"
    
    centerDists = calcDists(nColors, nCenters, nPoints, graph, curCenters)
    curRadius = calcRadius(nColors, nPoints, p, centerDists)

    improved = True
    while improved:
        improved = False
        for cPos in range(nCenters):
            for newCCol in range(nColors):
                for newCId in range(nPoints[newCCol]):
                    oldCCol, oldCId = curCenters[cPos]
                    updateDists(nColors, nPoints, graph, curCenters, centerDists, cPos, newCCol, newCId)
                    newRadius = calcRadius(nColors, nPoints, p, centerDists)
                    if newRadius < curRadius:
                        curRadius = newRadius
                        improved = True
                    elif newRadius > curRadius: # Reverse centerDists update
                        updateDists(nColors, nPoints, graph, curCenters, centerDists, cPos, oldCCol, oldCId)
    return curCenters
                    
