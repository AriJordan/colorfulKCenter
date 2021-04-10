from numpy import zeros, ones, full, sort
from algorithms.binarySearchRadius import binarySearchRadius

# Return: centers for fixed radius and whether covered all points successully
def fixedRadiusCKMN01(nColors, nCenters, nPoints, p, graph, radius):
	nPointsWithinRadius = zeros((nPoints[0]))
	for point1Id in range(nPoints[0]):
		for point2Id in range(nPoints[0]):
			if graph[0][point1Id][0][point2Id] < radius:
				nPointsWithinRadius[point1Id] += 1
	centerIds = full((nCenters, 2), -1)
	remaining = full((nPoints[0]), True)
	nCovered = 0
	for centerId in range(nCenters):
		if nCovered == nPoints[0]:
			return centerIds, True
		bestNPoints = -1
		bestCenterId = -1
		for candidateId in range(nPoints[0]):
			if remaining[candidateId] and nPointsWithinRadius[candidateId] > bestNPoints:
				bestNPoints = nPointsWithinRadius[candidateId]
				bestCenterId = candidateId
		centerIds[centerId] = [0, bestCenterId]
		for in3RId in range(nPoints[0]):
			if remaining[in3RId] and graph[0][bestCenterId][0][in3RId] < 3 * radius:
				for in1RId in range(nPoints[0]):
					if remaining[in1RId] and graph[0][in3RId][0][in1RId] < radius:
						nPointsWithinRadius[in1RId] -= 1
				nCovered += 1
				remaining[in3RId] = False
	return centerIds, (nCovered >= p[0])

# Return: 3-approximation by Charikar et al.
def algoCKMN01(nColors, nCenters, nPoints, p, graph):
	assert nColors == 1 # 1 color algorithm
	assert len(p) == 1 and len(graph) == 1
	assert len(graph[0]) == nPoints[0]
	return binarySearchRadius(fixedRadiusCKMN01, nColors, nCenters, nPoints, p, graph)
	