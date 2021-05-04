from numpy import array
from algorithms.binarySearchRadius import binarySearchRadius
from algorithms.BIPV19 import solveLP, buildFractional
from algorithms.simplifyGraph import simplifyGraph, simpleId, getColor, getPId

# Return: Number of red and blue vertices in D_v for v in S
def getRB(graph, D):
    r_D = zeros((sum(nPoints)))
    b_D = zeros((sum(nPoints)))
    for v in range(len(D)):
        for w in D[v]:
            if getColor(w) == 0:
                r_D[v] += 1
            elif getColor(w) == 1:
                b_D[v] += 1
            else:
                assert 0, "2 colors assumed"
    return r_D, b_D

# Return: Fractional solution to helper LP 
def solveLPh():
    # ▓▒░ ♥♥♥♥♥♥ ░▒▓

# Return: y rounded up for fractional D_v with most blue points
def roundBlue(graph, y, S, D, b_S):
    maxB = -1
    maxv = -1
    for v in range(len(S)):
        if S[v] > 0 and S[v] < 1 and b_S[v] > maxB:
            maxB = b_S[v]
            maxv = v
    if maxv != -1:
        S[v] = 1
    for v in range(len(S)):
        if S[v] < 1:
            S[v] = 0


# Return: whether well-separated and non-separated centers if not
def testNonSeparated(simpleGraph, S, radius):
    for u in range(len(S)):
        assert S[u] == 0 or S[v] == 1, "S[v] is not integral"
        if S[u]:
            for v in range(len(S)):
                if S[v]:
                    if simpleGraph[u][v] <= 2 * radius:
                        centers = []
                        for w in range(len(S)):
                            if S[w] == 1 and w != v:
                                centers.append(getPId(w), getColor(w))
                        return centers
    return full((len(S), 2), -1), False               


# Return : q_i and P_i
def getqP(nPoints, graph, guessedCenters, radius):
    q = []
    P = [[1 for n in range(sum(nPoints))]]
    for i in range(3):
        gC = guessedCenters[i]
        pCol = getColor(gC)
        pId = getPId(gC)
        # find q_i
        bestGain = -1
        bestq = [-1, -1]
        for qCol in range(len(nPoints)):
            for qId in range(len(nPoints[qCol])):
                if graph[pCol][pId][qCol][qId] <= radius: # q in B(p)
                    # count Gain(p, q) := R ∩ (F(q) \ B(p))
                    gain = 0
                    for vCol in range(len(nPoints)):
                        for vId in range(len(nPoints[vCol])):
                            if graph[qCol][qId][vCol][vId] <= radius:
                                for wId in range(len(nPoints[0])):
                                    if graph[vCol][vId][0][wId] <= radius and graph[pCol][pId][0][wId] and P[i]:
                                        gain += 1
                    if gain > bestGain:
                        bestGain = gain
                        bestq = [qCol, qId]
        assert bestq[1] != -1
        q.append(bestq)

        # Build P_(i+1)
        P_ip1 = P[i]
        for vCol in range(len(nPoints)):
            for vId in range(len(nPoints[vCol])):
                if graph[qCol][qId][vCol][vId] <= radius:
                    for wCol in range(len(nPoints)):
                        for wId in range(len(nPoints[0])):
                            if graph[vCol][vId][wCol][wId] <= radius:
                                P_ip1[simpleId(nPoints, wCol, wId)] = 0
        P.append(P_ip1)
    return q, P         

# Return : P_s (sparse points) and P_d (dense points)
def getP_sP_d(graph, q, P):

# Return: centers in S_d
def A_d(graph, P_d, k_d, r_d, b_d):

# Return: centers in S_s
def A_s(graph, P_s, k_s, r_s, b_s):

# Return: 3-approximation for fixed radius and whether successful
def fixedRadiusJSS20(nColors, nCenters, nPoints, p, graph, radius, flowers=True):
    simpleGraph = simplifyGraph(graph)

    # Solve LP
    x, z, success = solveLP(nColors, nCenters, nPoints, p, graph, radius)
    if not success:
        return full((nCenters, 2), -1), False

    # Build fractional centers
    x, z, oldS, D = buildFractional(nColors, nPoints, graph, radius, x, z)
    assert len(S) == nCenters

    # Calculate number of points per color in D_v for v in S
    assert nColors == 2, "only implemented for two colors"
    r_D, b_D = getRB(D)

    # Get fractional solution to helper LP
    y = solveLPh(S, r_D, b_D, simpleGraph)

    # Round up blue
    y = roundBlue(graph, y, S, D, b_D)

    nonSepCenters, isSeparated = testNonSeparated(graph, S)
    if not isSeparated:
        return nonSepCenters

    # Guess 3 centers
    for c1 in range(sum(nPoints)):
        for c2 in range(c1 + 1, sum(nPoints)):
            for c3 in range(c2 + 1, sum(nPoints)):
                # Phase 1
                q, P = getqP(graph, [c1, c2, c3])

                # Create P_s and P_d (Phase 2)
                P_s, P_d = getP_sP_d(graph, q, P)

                # Guess number of centers in P_d, number of red and blue points
                for k_d in range(0, K+1):
                    for r_d in range(0, nPoints[0]+1):
                        for b_d in range(0, nPoints[1]+1):
                            A_dCenters, A_dSuccess = A_d(graph, P_d, k_d, r_d, b_d)
                            A_sCenters, A_sSuccess = A_s(graph, P_s, K - k_d, nPoints[0] - r_d, nPoints[1] - b_d)
                            if A_dSuccess and A_sSuccess: # TODO: return best if several guesses succeed
                                return A_dCenters + A_sCenters, True
    return full((nCenters, 2), -1), False


# Return: 3-approximation for colorful k-center by Jia et al.
def algoJSS20(nColors, nCenters, nPoints, p, graph):
    assert nColors == len(p)
    return binarySearchRadius(fixedRadiusJSS20, nColors, nCenters, nPoints, p, graph)

