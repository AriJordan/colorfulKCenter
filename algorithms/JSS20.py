from numpy import array
from algorithms.binarySearchRadius import binarySearchRadius
from algorithms.BIPV19 import solveLP, buildFractional

# Return: Number of red and blue vertices in D_v for v in S
def getRB(graph, S):

# Return: Fractional solution to helper LP
def solveLPh():

# Return: y rounded up for fractional D_v with most blue points
def roundBlue(graph, y, S, D, b_S):

# Return: whether well-separated and non-separated centers if not
def testNonSeparated(graph, S):

# Return: 3-approximation for fixed radius and whether successful
def fixedRadiusJSS20(nColors, nCenters, nPoints, p, graph, radius, flowers=True):
    # Solve LP
    x, z, success = solveLP(nColors, nCenters, nPoints, p, graph, radius)
    if not success:
        return full((nCenters, 2), -1), False

    # Build fractional centers
    x, z, S, D = buildFractional(nColors, nPoints, graph, radius, x, z)

    # Calculate number of points per color in D_v for v in S
    assert nColors == 2, "only implemented for two colors"
    r_S, b_S = getRB(graph, S)

    # Get fractional solution to helper LP
    y = solveLPh(S, r_S, b_S, graph)

    # Round up blue
    y = roundBlue(graph, y, S, D, b_S)

    isSeparated, nonSepCenters = testNonSeparated(graph, S)
    if not isSeparated:
        return nonSepCenters

    # Guess 3 centers
    for c1 in range(sum(nPoints)):
        for c2 in range(c1 + 1, sum(nPoints)):
            for c3 in range(c2 + 1, sum(nPoints)):
                # Phase 1

                # Create P_s and P_d (Phase 2)

                # Guess number of centers in P_d, number of red and blue points
                for k_d in range(0, K+1):
                    for r_d in range(0, nPoints[0]+1):
                        for r_b in range(0, nPoints[1]+1):
                            A_dCenters, A_dSuccess = A_d()
                            A_sCenters, A_sSuccess = A_s()
                            if A_dSuccess and A_sSuccess:
                                return A_dCenters + A_sCenters, True
    return full((nCenters, 2), -1), False


# Return: 3-approximation for colorful k-center by Jia et al.
def algoJSS20(nColors, nCenters, nPoints, p, graph):
    assert nColors == len(p)
    return binarySearchRadius(fixedRadiusJSS20, nColors, nCenters, nPoints, p, graph)
