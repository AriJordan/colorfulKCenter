from numpy import zeros, ones, full, sort
from algorithms.binarySearchRadius import binarySearchRadius
from algorithms.simplifyGraph import ignoreColors, getColor, getPId, getOlds

# Return: centers for fixed radius and whether covered all points successully
def fixedRadiusCKMN01(nColors, nCenters, nPoints, p, graph, radius):
	assert nColors == 1 and len(nPoints) == 1 and len(p) == 1 and len(graph) == 1 
	nPointsWithinRadius = zeros(sum(nPoints))
	for point1Id in range(sum(nPoints)):
		for point2Id in range(sum(nPoints)):
			if graph[0][point1Id][0][point2Id] < radius:
				nPointsWithinRadius[point1Id] += 1
	centerIds = full((nCenters, 2), -1)
	remaining = full((sum(nPoints)), True)
	nCovered = 0
	for centerId in range(nCenters):
		if nCovered == nPoints[0]:
			return centerIds, True
		bestNPoints = -1
		bestCenterId = -1
		for candidateId in range(sum(nPoints)):
			if remaining[candidateId] and nPointsWithinRadius[candidateId] > bestNPoints:
				bestNPoints = nPointsWithinRadius[candidateId]
				bestCenterId = candidateId
		centerIds[centerId] = [0, bestCenterId]
		for in3RId in range(sum(nPoints)):
			if remaining[in3RId] and graph[0][bestCenterId][0][in3RId] < 3 * radius:
				for in1RId in range(sum(nPoints)):
					if remaining[in1RId] and graph[0][in3RId][0][in1RId] < radius:
						nPointsWithinRadius[in1RId] -= 1
				nCovered += 1
				remaining[in3RId] = False
	return centerIds, (nCovered >= sum(p))

# Return: 3-approximation by Charikar et al.
# Remark: Guarantee only holds for 1 color
def algoCKMN01(nColors, nCenters, nPoints, p, graph):
	if nColors > 1:
		graph = ignoreColors(nColors, nPoints, graph)
	assert len(graph[0]) == sum(nPoints)

	centerIds = binarySearchRadius(fixedRadiusCKMN01, 1, nCenters, [sum(nPoints)], [sum(p)], graph)

	if nColors > 1:
		centerIds = getOlds(nPoints, [centerIds[i][1] for i in range(len(centerIds))])
	return centerIds
	