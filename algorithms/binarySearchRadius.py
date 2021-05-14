from numpy import zeros, sort
# Summary: Binary search minimum radius running the passed algorithm algo
# Args: algo, an algorithm to run for different radii
# Return: centerIds, ids of centers for the smallest radius for which algo suceeded
def binarySearchRadius(algo, nColors, nCenters, nPoints, P, graph):
	radii = zeros((sum(nPoints)**2))
	rId = 0
	for col1 in range(nColors):
		for point1Id in range(nPoints[col1]):
			for col2 in range(nColors):
				for point2Id in range(nPoints[col2]):
					radii[rId] = graph[col1][point1Id][col2][point2Id] + 1e-6
					rId += 1
	radii.sort()
	lowerRadiusId = 0 # id of lower bound on radius
	upperRadiusId = rId - 1
	while lowerRadiusId < upperRadiusId:
		middleRadiusId = (lowerRadiusId + upperRadiusId) // 2
		radius = radii[middleRadiusId]
		centerIds, success = algo(nColors, nCenters, nPoints, P, graph, radius)
		if success:
			upperRadiusId = middleRadiusId
		else:
			lowerRadiusId = middleRadiusId + 1
	centerIds, success = algo(nColors, nCenters, nPoints, P, graph, radii[lowerRadiusId])
	assert success == True
	return centerIds