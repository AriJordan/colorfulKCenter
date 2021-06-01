from algorithms.randomCenters import algoRandomCenters
from scipy.spatial import KDTree
from numpy import array, amin, amax, sort, zeros

def calcDists(nColors, nCenters, nPoints, graph, curCenters):
    centerDists = zeros((nColors, amax(nPoints), nCenters))
    for pCol in range(nColors):
        for pId in range(nPoints[pCol]):
            for cPos in range(len(curCenters)):
                cCol, cId = curCenters[cPos]
                centerDists[pCol][pId][cPos] = graph[pCol][pId][cCol][cId]
    return centerDists

def updateDists(curCenters, cPos, newCCol, newCId, points):
    curCenters[cPos] = [newCCol, newCId]
    return KDTree([points[cCol][cPos] for cCol, cPos in curCenters])

def calcRadius(nColors, nPoints, p, points, kdTree):
    radius = 0
    for col in range(nColors):
        if p[col] > 0:
            smallDists = sort(array(kdTree.query(array([points[col][pId] for pId in range(nPoints[col])]))[0]))
            radius = max(radius, smallDists[p[col]-1])
    return radius

def algoHillClimbingKDTree(nColors, nCenters, nPoints, p, graph, points):
    curCenters = algoRandomCenters(nColors, nCenters, nPoints, p, graph)
    assert amin(curCenters) > -1, "There should be k centers"
    
    kdTree = KDTree([points[cCol][cPos] for cCol, cPos in curCenters])
    curRadius = calcRadius(nColors, nPoints, p, points, kdTree)

    improved = True
    while improved:
        improved = False
        for cPos in range(nCenters):
            for newCCol in range(nColors):
                for newCId in range(nPoints[newCCol]):
                    oldCCol, oldCId = curCenters[cPos]
                    kdTree = updateDists(curCenters, cPos, newCCol, newCId, points)
                    newRadius = calcRadius(nColors, nPoints, p, points, kdTree)
                    if newRadius < curRadius:
                        curRadius = newRadius
                        improved = True
                    elif newRadius > curRadius: # Reverse centerDists update
                        updateDists(curCenters, cPos, oldCCol, oldCId, points)
    return curCenters

