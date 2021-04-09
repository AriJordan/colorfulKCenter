from numpy import copy, full, inf, sort

# Summary: Try all possible sets of centers recursively
# Return: best radius and best centers
def recursiveBruteForce(nColors, nCenters, nPoints, p, graph, nCentersChosen, nextId, currentCenterIds, closestCenterDist):
    assert nColors == 1
    assert nCentersChosen < nCenters
    bestRadius = inf
    bestCenters = full((nCenters, 2), -1)
    col1 = 0 # TODO: handle different colors
    for candidateId in range(nextId, nPoints[col1] - (nCenters - nCentersChosen - 1)):   
        newClosestCenterDist = copy(closestCenterDist)
        # Pick candidateId as new center
        currentCenterIds[nCentersChosen] = [col1, candidateId]
        # Update distances and radius
        currentRadius = 0
        for col2 in range(nColors):
            for pointId in range(nPoints[col2]):
                newClosestCenterDist[col2][pointId] = min(newClosestCenterDist[col2][pointId], graph[col1][candidateId][col2][pointId])
            sortedClosestCenterDist = sort(newClosestCenterDist[col2])
            currentRadius = max(currentRadius, sortedClosestCenterDist[p[col2]-1])
        if nCentersChosen + 1 < nCenters: # recurse
            radius, centers = recursiveBruteForce(nColors, nCenters, nPoints, p, graph, nCentersChosen + 1, candidateId + 1, currentCenterIds, newClosestCenterDist)
        else:
            radius, centers = currentRadius, currentCenterIds
        if radius < bestRadius:
            bestRadius, bestCenters = radius, copy(centers)
    currentCenterIds[nCentersChosen] = [-1, -1]
    return bestRadius, bestCenters

# Return: Optimal set of centers
def algoBruteForce(nColors, nCenters, nPoints, p, graph):
    assert nColors == 1
    assert nCenters > 0
    bestRadius, bestCenters = recursiveBruteForce(nColors, nCenters, nPoints, p, graph, 0, 0, full((nCenters, 2), -1), full((nColors, nPoints[0]), inf)) # TODO: several colors
    return bestCenters