from numpy import copy, full, inf, sort, amax
from algorithms.simplifyGraph import getColor, getPId

# Summary: Try all possible sets of centers recursively
# Return: best radius and best centers
def recursiveBruteForce(nColors, nCenters, nPoints, p, graph, nCentersChosen, nextId, currentCenterIds, closestCenterDist):
    assert nCentersChosen < nCenters
    bestRadius = inf
    bestCenters = full((nCenters, 2), -1)
    for candidateId in range(nextId, sum(nPoints) - (nCenters - nCentersChosen - 1)):
        col1, oldId = getColor(nPoints, candidateId), getPId(nPoints, candidateId)
        newClosestCenterDist = copy(closestCenterDist)

        # Pick [col1, oldId] as new center
        currentCenterIds[nCentersChosen] = [col1, oldId]

        # Update distances and radius
        currentRadius = 0
        for col2 in range(nColors):
            if nPoints[col2] > 0 and p[col2] > 0:
                for pointId in range(nPoints[col2]):
                    newClosestCenterDist[col2][pointId] = min(newClosestCenterDist[col2][pointId], graph[col1][oldId][col2][pointId])
                sortedClosestCenterDist = sort(newClosestCenterDist[col2])
                currentRadius = max(currentRadius, sortedClosestCenterDist[p[col2]-1])

        if nCentersChosen + 1 < nCenters: # Recurse
            radius, centers = recursiveBruteForce(nColors, nCenters, nPoints, p, graph, nCentersChosen + 1, candidateId + 1, currentCenterIds, newClosestCenterDist)
        else:
            radius, centers = currentRadius, currentCenterIds

        if radius < bestRadius:
            bestRadius, bestCenters = radius, copy(centers)

    currentCenterIds[nCentersChosen] = [-1, -1]
    return bestRadius, bestCenters

# Return: Optimal set of centers
def algoBruteForce(nColors, nCenters, nPoints, p, graph):
    assert nCenters > 0
    bestRadius, bestCenters = recursiveBruteForce(nColors, nCenters, nPoints, p, graph, 0, 0, full((nCenters, 2), -1), full((nColors, amax(nPoints)), inf))
    assert len(bestCenters) <= nCenters
    return bestCenters