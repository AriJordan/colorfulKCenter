from numpy import argmax, full, inf, ones, zeros
from algorithms.binarySearchRadius import binarySearchRadius
from algorithms.LPSolver import LPSolver
from algorithms.simplifyGraph import simplifyGraph, getColor, getPId

# Return: fractional solution to LP if it exists
def solveLPc(nColors, nCenters, nPoints, p, graph, radius):
	assert nColors == len(p)
	# Rows represent: -sum_{v in B(z_u)}(x_v) + z_u <= 0, sum(x_v) <= k, -sum_{v in color}(x_v) <= -p[color], x <= 1, z <= 1
	A = zeros((sum(nPoints) + 1 + nColors + 2 * sum(nPoints), 2 * sum(nPoints)))
	b = zeros((sum(nPoints) + 1 + nColors + 2 * sum(nPoints)))
	c = zeros((2 * sum(nPoints)))
	for col1 in range(nColors):
		for zId in range(nPoints[col1]):
			for col2 in range(nColors):
				for xId in range(nPoints[col2]):
					if graph[col1][zId][col2][xId] < radius:
						A[sum(nPoints[0:col1]) + zId][sum(nPoints[0:col2]) + xId] = -1.0
			A[sum(nPoints[0:col1]) + zId][sum(nPoints) + sum(nPoints[0:col1]) + zId] = 1.0
	A[sum(nPoints)][0:sum(nPoints)] = 1
	b[sum(nPoints)] = nCenters
	for col in range(nColors):
		A[(sum(nPoints) + 1) + col][(sum(nPoints) + sum(nPoints[0:col])) : (sum(nPoints) + sum(nPoints[0:col+1]))] = -1
		b[(sum(nPoints) + 1) + col] = -p[col]
	for i in range((sum(nPoints) + 1 + nColors), (sum(nPoints) + 1 + nColors) + 2 * sum(nPoints)):
		A[i][i - (sum(nPoints) + 1 + nColors)] = 1
		b[i] = 1
	xz = zeros((2 * sum(nPoints)))
	fractionalRadius, xz = LPSolver(A, b, c).solve(xz)
	x, z = xz[0:sum(nPoints)], xz[sum(nPoints):(2 * sum(nPoints))]
	if fractionalRadius == inf:
		return x, z, False
	else:
		return x, z, True

def buildFractional(nColors, nPoints, graph, radius, x, z, flowers=False):
	remPoints = ones((sum(nPoints)))
	S = zeros((sum(nPoints)))
	nPointsRem = sum(nPoints)
	D = [[] for _ in range(sum(nPoints))]
	simpleGraph = simplifyGraph(nColors, nPoints, graph)
	while len(z) > 0 and max(z * remPoints) > 0:
		v_max = argmax(z * remPoints)
		S[v_max] = 1
		x[v_max] = min(1.0, sum((simpleGraph[v_max][u] < radius) * x[u] for u in range(sum(nPoints))))
		if x[v_max] < 1e-6:
			break
		for u in range(sum(nPoints)):
			if simpleGraph[v_max][u] < radius and remPoints[u]:		
				nPointsRem -= 1
				if u != v_max:
					x[u] = 0		
		D_v = []
		if flowers: # for JSS20 flowers
			for u in range(sum(nPoints)):
				if simpleGraph[v_max][u] < radius:
					for w in range(sum(nPoints)):
						if simpleGraph[u][w] < radius and remPoints[w]:
							nPointsRem -= 1
							if w != w_max:
								x[w] = 0
		else: # for radius 2
			for u in range(sum(nPoints)):
				if simpleGraph[v_max][u] < 2 * radius and remPoints[u]:
					z[u] = x[v_max]
					D_v.append(u)
		for u in D_v:
			remPoints[u] = 0
		D[v_max] = D_v
	return x, z, S, D


# Return: centers for fixed radius and whether successful
def fixedRadiusBIPV19(nColors, nCenters, nPoints, p, graph, radius, flowers=False):
	# Solve LP
	x, z, success = solveLPc(nColors, nCenters, nPoints, p, graph, radius)
	if not success:
		return full((nCenters, 2), -1), False
	
	# Build fractional centers
	x, z, S, D = buildFractional(nColors, nPoints, graph, radius, x, z)	

	# Make integral
	for v in range(sum(nPoints)):
		if S[v] and 1e-6 <= x[v] and x[v] <= 1 - 1e-6:
			for w in range(sum(nPoints)):
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
	for v in range(sum(nPoints)):
		if S[v] and 1e-6 <= x[v]:
			x[v] = 1.0
			for u in D[v]:
				z[v] = x[v]
		else:
			x[v] = 0.0
	for v in range(sum(nPoints)):
		if S[v] and x[v] == 0:
			S[v] = 0

	# Create and test resulting centers
	assert sum(x) <= nCenters + 1e-6 and sum(x) >= 1 - 1e-6
	centerIds = full((nCenters, 2), -1)
	centerId = 0
	nPointsCovered = zeros(nColors)
	for v in range(sum(nPoints)):
		if x[v]:
			assert x[v] == 0.0 or x[v] == 1.0
			centerIds[centerId] = [getColor(nPoints, v), getPId(nPoints, v)]
			centerId += 1
			for u in D[v]:
				nPointsCovered[getColor(nPoints, u)] += 1
	return centerIds, (nPointsCovered >= p)

# Return: 2-approximation by Bandyapadhyay et al.
def algoBIPV19(nColors, nCenters, nPoints, p, graph):
	assert nColors == 1 # 1 color algorithm
	assert len(p) == 1 and len(graph) == 1
	assert len(graph[0]) == nPoints[0]
	return binarySearchRadius(fixedRadiusBIPV19, nColors, nCenters, nPoints, p, graph)
