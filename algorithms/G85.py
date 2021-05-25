from numpy import array, full, zeros, inf
from algorithms.simplifyGraph import ignoreColors, getColor, getPId

# Return: 2-approximation by Gonzales
def algoG85(nColors, nCenters, nPoints, p, graph):
    assert nColors == len(graph)
    assert len(graph[0]) == nPoints[0]
    if nColors > 1:
        graph = ignoreColors(nColors, nPoints, graph)
   
    minDists = full(sum(nPoints), inf)
    centerIds = full((nCenters, 2), -1)
    taken = zeros(sum(nPoints))
    for centerId in range(nCenters):
        bestCenterId = -1
        bestRadius = -1
        for candidateId in range(sum(nPoints)):
            if not taken[candidateId] and minDists[candidateId] > bestRadius:
                bestRadius = minDists[candidateId]
                bestCenterId = candidateId
        taken[bestCenterId] = True
        centerIds[centerId] = [0, bestCenterId]
        for otherId in range(sum(nPoints)):
            minDists[otherId] = min(minDists[otherId], graph[0][bestCenterId][0][otherId])

    if nColors > 1:
        for cPos in range(len(centerIds)):
            cCol, cId = centerIds[cPos]
            centerIds[cPos] = [getColor(nPoints, cId), getPId(nPoints, cId)]
    return centerIds
