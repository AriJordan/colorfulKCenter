from numpy import zeros, ones, full, sort
from algorithms.binarySearchRadius import binarySearchRadius
from algorithms.simplifyGraph import ignoreColors, getColor, getPId, getOlds

# Return: centers for fixed radius and whether covered all points successully
def fixedRadiusHS86(nColors, nCenters, nPoints, p, graph, radius):
	assert nColors == 1 and len(nPoints) == 1 and len(p) == 1 and len(graph) == 1 
	pointsLeft = ones(sum(nPoints))
	centerIds = full((nCenters, 2), -1)
	for centerId in range(nCenters):
		for candidateId in range(sum(nPoints)):
			if pointsLeft[candidateId]:
				centerIds[centerId] = [0, candidateId]
				for removeId in range(sum(nPoints)):
					if graph[0][candidateId][0][removeId] < 2 * radius:
						pointsLeft[removeId] = False
				break
	success = True
	for left in pointsLeft:
		if left: # Point not covered
			success = False
	return centerIds, success

# Return: 2-approximation by Hochbaum and Shmoys
# Remark: Guarantee only holds for 1 color and no outliers
def algoHS86(nColors, nCenters, nPoints, p, graph):
	assert nColors == len(graph)
	if nColors > 1:
		graph = ignoreColors(nColors, nPoints, graph)
	assert len(graph[0]) == sum(nPoints)

	centerIds = binarySearchRadius(fixedRadiusHS86, 1, nCenters, [sum(nPoints)], [sum(p)], graph)

	if nColors > 1:
		centerIds = getOlds(nPoints, [centerIds[i][1] for i in range(len(centerIds)) if centerIds[i][1] != -1])
	return centerIds
	

