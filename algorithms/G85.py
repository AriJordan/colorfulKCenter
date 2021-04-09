from numpy import array, full, zeros, inf

# Return: 2-approximation by Gonzales
def algoG85(nColors, nCenters, nPoints, p, graph):
    assert nColors == 1 and len(graph) == 1
    assert len(graph[0]) == nPoints[0]
    minDists = full(nPoints[0], inf)
    centerIds = full((nCenters, 2), -1)
    taken = zeros(nPoints)
    for centerId in range(nCenters):
        bestCenterId = -1
        bestRadius = -1
        for candidateId in range(nPoints[0]):
            if not taken[candidateId] and minDists[candidateId] > bestRadius:
                bestRadius = minDists[candidateId]
                bestCenterId = candidateId
        taken[bestCenterId] = True
        centerIds[centerId] = [0, bestCenterId]
        for otherId in range(nPoints[0]):
            minDists[otherId] = min(minDists[otherId], graph[0][bestCenterId][0][otherId])
    return centerIds
