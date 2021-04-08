from numpy import random
from numpy import full, resize

def algoRandomCenters(nColors, nCenters, nPoints, p, graph):
    allIds = full((sum(nPoints), 2), -1)
    id = 0
    for col in range(nColors):
        for pointId in range(nPoints[col]):
            allIds[id] = [col, pointId]
            id += 1
    random.shuffle(allIds)
    return resize(allIds, (nCenters, 2))
