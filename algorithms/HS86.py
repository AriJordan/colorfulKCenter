from numpy import zeros, ones, full, sort

# Return: centers for fixed radius and whether covered all points successully
def fixedRadiusCenters(nCenters, nPoints, graph, radius):
	pointsLeft = ones((nPoints[0]))
	centerIds = full((nCenters, 2), -1)
	for centerId in range(nCenters):
		for candidateId in range(nPoints[0]):
			if pointsLeft[candidateId]:
				centerIds[centerId] = [0, candidateId]
				for removeId in range(nPoints[0]):
					if graph[0][candidateId][0][removeId] < radius:
						pointsLeft[removeId] = False
				break
	success = True
	for left in pointsLeft:
		if left: # Point not covered
			success = False
	return centerIds, success

# Return: 2-approximation by Hochbaum and Shmoys
def algoHS86(nCenters, nPoints, graph):
	assert len(graph) == 1 # 1 color
	assert len(graph[0]) == nPoints
	radii = zeros((nPoints[0]**2))
	for point1Id in range(nPoints[0]):
		for point2Id in range(nPoints[0]):
			radii[point1Id * nPoints[0] + point2Id] = graph[0][point1Id][0][point2Id] + 1e-6
	radii.sort()
	lowerRadiusId = 0 # id of lower bound on radius
	upperRadiusId = nPoints**2 - 1
	while lowerRadiusId < upperRadiusId:
		middleRadiusId = (lowerRadiusId + upperRadiusId) // 2
		radius = radii[middleRadiusId]
		centerIds, success = fixedRadiusCenters(nCenters, nPoints, graph, radius)
		if success:
			upperRadiusId = middleRadiusId
		else:
			lowerRadiusId = middleRadiusId + 1
	centerIds, success = fixedRadiusCenters(nCenters, nPoints, graph, radii[lowerRadiusId])
	assert success == True
	return centerIds

