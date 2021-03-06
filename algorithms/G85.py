from numpy import array, full, zeros, inf
from timeit import default_timer as timer
from algorithms.simplifyGraph import ignoreColors, getColor, getPId, getOlds

# Return: 2-approximation by Gonzales
# Remark: Guarantee only holds for 1 color and no outliers
def algoG85(nColors, nCenters, nPoints, p, graph):
    assert nColors == len(graph)
    if nColors > 1:
        graph = ignoreColors(nColors, nPoints, graph)
    startTime = timer()
   
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
        centerIds = getOlds(nPoints, [centerIds[i][1] for i in range(len(centerIds)) if centerIds[i][1] != -1])
        
    return centerIds, startTime
