from numpy import zeros, sort
# Summary: Binary search minimum radius running the passed algorithm algo
# Args: algo, an algorithm to run for different radii
# Return: centerIds, ids of centers for the smallest radius for which algo suceeded
def binarySearchRadius(algo, nColors, nCenters, nPoints, P, graph):
	radii = zeros((nPoints[0]**2))
	for point1Id in range(nPoints[0]):
		for point2Id in range(nPoints[0]):
			radii[point1Id * nPoints[0] + point2Id] = graph[0][point1Id][0][point2Id] + 1e-6
	radii.sort()
	lowerRadiusId = 0 # id of lower bound on radius
	upperRadiusId = nPoints[0]**2 - 1
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