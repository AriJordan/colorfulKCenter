from algorithms.binarySearchRadius import binarySearchRadius
from algorithms.BIPV19 import solveLPc
from algorithms.JSS20 import buildFractional, getRB, solveLPh
from algorithms.simplifyGraph import getOlds

# Return: y rounded up for fractional D_v with most points
def roundUp(nCenters, graph, y, S, D, b_S):
    assert len(S) == len(y)
    if sum([1 for y_v in y if y_v > 1e-6 ]) <= nCenters: # Can round all up
        for v in range(len(y)):
            if y[v] > 1e-6:
                y[v] = 1
            else:
                y[v] = 0
        return y

    # Round up biggest
    maxY = -1
    maxv = -1
    for v in range(len(y)):
        if y[v] > 0 and y[v] < 1 and Y[v] > maxPoints:
            maxY = Y[v]
            maxv = v
    if maxv != -1:
        y[maxv] = 1
    for v in range(len(S)):
        if y[v] < 1 - 1e-6:
            y[v] = 0
        else:
            y[v] = 1
    return y

# Return: Centers where Y[c] = 1
def getCenters(nPoints, y):
    return getOlds(nPoints, [v for v in range(len(y)) if y[v] == 1])

def fixedRadiusLPhHeuristic(nColors, nCenters, nPoints, p, graph, radius):
    x, z, success = solveLPc(nColors, nCenters, nPoints, p, graph, radius)
    if not success:
        return [], False
    
    # Build fractional centers
    x, z, S, D = buildFractional(nColors, nPoints, graph, radius, x, z)
    assert len(S) == sum(nPoints) # S is indicator
    
    # Calculate number of points per color in D_v for v in S
    assert nColors == 2, "only implemented for two colors"
    r_D, b_D = getRB(nPoints, D)
    
    # Get fractional solution to helper LP
    y = solveLPh(nPoints, S, r_D, b_D, p[0], p[1], nCenters)
    
    # Round up biggest y
    y = roundUp(nCenters, graph, y, S, D, b_D)

    # Return centers where y == 1
    return getCenters(nPoints, y), True

def algoLPhHeuristic(nColors, nCenters, nPoints, p, graph):
    assert nColors == len(p)
    return binarySearchRadius(fixedRadiusLPhHeuristic, nColors, nCenters, nPoints, p, graph)