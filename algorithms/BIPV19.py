from numpy import argmax, full, inf, ones, zeros
from algorithms.binarySearchRadius import binarySearchRadius
from algorithms.LPSolver import LPSolver

# Return: centers for fixed radius and whether successful
def fixedRadiusBIPV19(nColors, nCenters, nPoints, p, graph, radius):
	# Solve LP
	A = zeros((nPoints[0] + 2 + 2 * nPoints[0], 2 * nPoints[0]))
	b = zeros((nPoints[0] + 2 + 2 * nPoints[0]))
	c = zeros((2 * nPoints[0]))
	for zId in range(nPoints[0]):
		A[zId][nPoints[0] + zId] = 1.0
		for xId in range(nPoints[0]):
			if graph[0][zId][0][xId] < radius:
				A[zId][xId] = -1.0
	A[nPoints[0]][0:nPoints[0]] = 1
	b[nPoints[0]] = nCenters
	A[nPoints[0] + 1][nPoints[0]:(2 * nPoints[0])] = -1
	b[nPoints[0] + 1] = -p[0]
	for i in range(nPoints[0] + 2, nPoints[0] + 2 + 2 * nPoints[0]):
		A[i][i - (nPoints[0] + 2)] = 1
		b[i] = 1
	xz = zeros((2 * nPoints[0]))
	fractionalRadius, xz = LPSolver(A, b, c).solve(xz)
	if fractionalRadius == inf:
		return full((nCenters, 2), -1), False
	x, z = xz[0:nPoints[0]], xz[nPoints[0]:(2 * nPoints[0])]

	# Build fractional centers
	remPoints = ones((nPoints[0]))
	S = zeros((nPoints[0]))
	nPointsRem = nPoints[0]
	D = [[] for _ in range(nPoints[0])]
	while max(z * remPoints) > 0:
		v_max = argmax(z * remPoints)
		S[v_max] = 1
		x[v_max] = min(1.0, sum((graph[0][v_max][0][u] < radius) * x[u] for u in range(nPoints[0])))
		if x[v_max] < 1e-6:
			break
		for u in range(nPoints[0]):
			if graph[0][v_max][0][u] < radius and remPoints[u]:		
				nPointsRem -= 1
				if u != v_max:
					x[u] = 0		
		D_v = []
		for u in range(nPoints[0]):
			if graph[0][v_max][0][u] < 2 * radius and remPoints[u]:
				z[u] = x[v_max]
				D_v.append(u)
		for u in D_v:
			remPoints[u] = 0
		D[v_max] = D_v
	for v in range(nPoints[0]):
		if S[v] and 1e-6 <= x[v] and x[v] <= 1 - 1e-6:
			for w in range(nPoints[0]):
				if w != v and S[w] and 1e-6 <= x[w] and x[w] <= 1 - 1e-6:
					xsum = x[v] + x[w]
					if len(D[v]) >= len(D[w]):
						x[v] = min(1.0, xsum)
						x[w] = xsum - x[v]
					else:
						x[w] = min(1.0, xsum)
						x[v] = xsum - x[w]						
					for u in D[v]:
						z[u] = x[v]
					for y in D[w]:
						z[y] = x[w]
	for v in range(nPoints[0]):
		if S[v] and 1e-6 <= x[v]:
			x[v] = 1.0
			for u in D[v]:
				z[v] = x[v]
		else:
			x[v] = 0.0
	for v in range(nPoints[0]):
		if S[v] and x[v] == 0:
			S[v] = 0
	assert sum(x) <= nCenters + 1e-6 and sum(x) >= 1 - 1e-6
	centerIds = full((nCenters, 2), -1)
	centerId = 0
	nPointsCovered = 0
	for v in range(nPoints[0]):
		if x[v]:
			assert x[v] == 0.0 or x[v] == 1.0
			centerIds[centerId] = [0, v]
			centerId += 1
			nPointsCovered += len(D[v])
	return centerIds, (nPointsCovered >= p[0])

# Return: 2-approximation by Bandyapadhyay et al.
def algoBIPV19(nColors, nCenters, nPoints, p, graph):
	assert nColors == 1 # 1 color algorithm
	assert len(p) == 1 and len(graph) == 1
	assert len(graph[0]) == nPoints[0]
	return binarySearchRadius(fixedRadiusBIPV19, nColors, nCenters, nPoints, p, graph)
