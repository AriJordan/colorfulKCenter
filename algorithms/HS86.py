from numpy import zeros, ones, full, sort
from algorithms.binarySearchRadius import binarySearchRadius

# Return: centers for fixed radius and whether covered all points successully
def fixedRadiusHS86(nColors, nCenters, nPoints, p, graph, radius):
	pointsLeft = ones((nPoints[0]))
	centerIds = full((nCenters, 2), -1)
	for centerId in range(nCenters):
		for candidateId in range(nPoints[0]):
			if pointsLeft[candidateId]:
				centerIds[centerId] = [0, candidateId]
				for removeId in range(nPoints[0]):
					if graph[0][candidateId][0][removeId] < 2 * radius:
						pointsLeft[removeId] = False
				break
	success = True
	for left in pointsLeft:
		if left: # Point not covered
			success = False
	return centerIds, success

# Return: 2-approximation by Hochbaum and Shmoys
def algoHS86(nColors, nCenters, nPoints, p, graph):
	assert nColors == 1 # 1 color algorithm
	assert len(p) == 1 and len(graph) == 1
	assert len(graph[0]) == nPoints[0]
	return binarySearchRadius(fixedRadiusHS86, nColors, nCenters, nPoints, p, graph)
	

