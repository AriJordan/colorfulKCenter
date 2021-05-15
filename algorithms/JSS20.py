from numpy import amax, array, ones, zeros, full, copy
from algorithms.binarySearchRadius import binarySearchRadius
from algorithms.LPSolver import LPSolver
from algorithms.BIPV19 import solveLP, buildFractional
from algorithms.simplifyGraph import simplifyGraph, simpleId, getColor, getPId, getOlds

# Return: Number of red and blue vertices in D_v for v in S
def getRB(nPoints, D):
    r_D = zeros((sum(nPoints)))
    b_D = zeros((sum(nPoints)))
    for v in range(len(D)):
        for w in D[v]:
            if getColor(nPoints, w) == 0:
                r_D[v] += 1
            elif getColor(nPoints, w) == 1:
                b_D[v] += 1
            else:
                assert 0, "2 colors assumed"
    return r_D, b_D

# Return: Fractional solution to helper LP 
def solveLPh(nPoints, S, r_D, b_D, red, blue, k):
    if red == 0 and blue == 0: # Nothing to cover
        return zeros((sum(nPoints)))
    SIds = []
    for id in range(len(S)):
        if S[id]:
            SIds.append(id)

    # Rows represent: -sum_{v in S}(r_v * y_v) <= -r, -sum_{v in S}(b_v * y_v) <= -b, y <= 1
    A = zeros((2 + sum(nPoints), len(SIds)))
    b = zeros((2 + sum(nPoints)))
    c = ones((len(SIds)))

    for vPos in range(len(SIds)):
        v = SIds[vPos]
        A[0][vPos] = -r_D[v]
        A[1][vPos] = -b_D[v]
    b[0] = -red
    b[1] = -blue
    for vPos in range(len(SIds)):
        A[2 + vPos][vPos] = 1
        b[2 + vPos] = 1

    y = zeros((sum(nPoints)))
    nCenters, y = LPSolver(A, b, c).solve(y)
    assert nCenters <= k + 1e-6 and nCenters >= -1e-6
    yInd = zeros(len(S))
    pos = 0
    for id in range(len(S)):
        if S[id]:
            yInd[id] = y[pos]
            pos += 1
    return yInd

# Return: y rounded up for fractional D_v with most blue points
def roundBlue(nCenters, graph, y, S, D, b_S):
    assert len(S) == len(y)
    if sum([1 for y_v in y if y_v > 1e-6 ]) <= nCenters: # Can round all up
        for v in range(len(y)):
            if y[v] > 1e-6:
                y[v] = 1
            else:
                y[v] = 0
        return y

    maxB = -1
    maxv = -1
    for v in range(len(y)):
        if y[v] > 0 and y[v] < 1 and b_S[v] > maxB:
            maxB = b_S[v]
            maxv = v
    if maxv != -1:
        y[maxv] = 1
    for v in range(len(S)):
        if y[v] < 1 - 1e-6:
            y[v] = 0
        else:
            y[v] = 1
    return y


# Return: whether well-separated and non-separated centers if not
def testSeparated(simpleGraph, y, radius):
    for u in range(len(y)):
        assert y[u] == 0 or y[u] == 1, "y[u] is not integral"
        if y[u]:
            for v in range(u + 1, len(y)):
                if y[v]:
                    if simpleGraph[u][v] <= 2 * radius:
                        centers = []
                        for w in range(len(y)):
                            if y[w] == 1 and w != v:
                                centers.append(getPId(nPoints, w), getColor(nPoints, w))
                        return centers, False
    return [], True

# count Gain(p, q) := R ∩ (F(q) \ B(p))
def getGain(nPoints, graph, pCol, pId, qCol, qId, P, radius):
    gain = 0
    counted = zeros((nPoints[0]))
    for vCol in range(len(nPoints)):
        for vId in range(nPoints[vCol]):
            if graph[qCol][qId][vCol][vId] <= radius:
                for wId in range(nPoints[0]):
                    if not counted[wId] and graph[vCol][vId][0][wId] <= radius and graph[pCol][pId][0][wId] > radius and P[simpleId(nPoints, vCol, vId)]:
                        gain += 1
                        counted[wId] = 1
    return gain

# Return: q_i, P_i,
#         τ: the minimal value such that |Gain(p,q) ∩ P_4| ≤ τ
# TODO: Buggy
def getqP(nPoints, graph, guessedCenters, radius):
    q = []
    P = [[1 for n in range(sum(nPoints))]]
    for i in range(3):
        gC = guessedCenters[i]
        pCol = getColor(nPoints, gC)
        pId = getPId(nPoints, gC)
        # find q_i
        bestGain = -1
        bestq = [-1, -1]
        for qCol in range(len(nPoints)):
            for qId in range(nPoints[qCol]):
                if graph[pCol][pId][qCol][qId] <= radius: # q in B(p)
                    gain = getGain(nPoints, graph, pCol, pId, qCol, qId, P[i], radius)
                    if gain > bestGain:
                        bestGain = gain
                        bestq = [qCol, qId]
        assert bestq[1] != -1
        q.append(bestq)

        # Build P_(i+1)
        P_ip1 = copy(P[i])
        qCol, qId = bestq
        for vCol in range(len(nPoints)):
            for vId in range(nPoints[vCol]):
                if graph[qCol][qId][vCol][vId] <= radius:
                    for wCol in range(len(nPoints)):
                        for wId in range(nPoints[wCol]):
                            if graph[vCol][vId][wCol][wId] <= radius:
                                P_ip1[simpleId(nPoints, wCol, wId)] = 0
        P.append(P_ip1)
    return q, P, bestGain

# Return : P_s (sparse points) and P_d (dense points)
def getP_sP_dI(nPoints, graph, simpleGraph, q, P_4, tau, radius):
    P_s = copy(P_4)
    P_d = zeros(len(P_s))
    I = []
    D = []
    for v in range(len(P_s)):
        if P_s[v]:
            nRed = 0
            for wId in range(nPoints[0]):
                assert len(graph) == 2
                if P_s[wId] and graph[getColor(nPoints, v)][getPId(nPoints, v)][0][wId] <= radius:
                    nRed += 1
            if nRed > 2 * tau:
                I_v = []
                D_v = zeros((len(nPoints), max(nPoints[0], nPoints[1]))) # Indicator
                for uCol in range(2):
                    for uId in range(nPoints[uCol]):
                        # calculate |B(v) ∩ B(u) ∩ R|
                        lBv_n_Bu_n_Rl = 0
                        for wId in range(nPoints[0]):
                            if graph[uCol][uId][0][wId] <= radius and graph[getColor(nPoints, v)][getPId(nPoints, v)][0][wId] <= radius:
                                lBv_n_Bu_n_Rl += 1
                        if lBv_n_Bu_n_Rl > tau:
                            u = simpleId(nPoints, uCol, uId)
                            I_v.append(u)
                            # Remove D_u = U_{z in B(u)} ∩ P_s
                            for z in range(len(P_s)):
                                if simpleGraph[u][z] <= radius and P_s[z]:
                                    P_s[z] = 0
                                    P_d[z] = 1
                                    D_v[getColor(nPoints, z), getPId(nPoints, z)] = 1
                I.append(I_v)
                D.append(D_v)
    return P_s, P_d, I, D

# Return: centers in P_d
def A_d(nPoints, graph, P_d, I, k_d, r_d, b_d, D, radius):
    T = zeros((len(I) + 1, r_d + 1, b_d + 1, k_d + 1))
    T[0,0,0,0] = True
    choices = full((len(I) + 1, r_d + 1, b_d + 1, k_d + 1, 4), -1)
    lastC = full((len(I) + 1, r_d + 1, b_d + 1, k_d + 1), -1)
    for m in range(1, len(I) + 1):
        for r in range(r_d + 1):
            for b in range(b_d + 1):
                for k in range(k_d + 1):
                    if m > 0 and T[m-1][r][b][k]:
                        T[m][r][b][k] = True
                        choices[m][r][b][k] = [m-1, r, b, k]
                    for I_Id in range(len(I)):
                        for c in I[I_Id]:
                            rpp = r
                            bpp = b
                            for vId in range(len(graph[0])): 
                                if graph[getColor(nPoints, c)][getPId(nPoints, c)][0][vId] <= radius and D[I_Id][0][vId]:
                                    rpp -= 1
                            for vId in range(len(graph[1])): 
                                if graph[getColor(nPoints, c)][getPId(nPoints, c)][1][vId] <= radius and D[I_Id][1][vId]:
                                    bpp -= 1
                            rpp = max(0, rpp)
                            bpp = max(0, bpp)
                            if m > 0 and k > 0 and T[m-1][rpp][bpp][k-1]:
                                T[m][r][b][k] = True
                                choices[m][r][b][k] = [m-1, rpp, bpp, k-1]
                                lastC[m][r][b][k] = c
                                break

    if T[len(I)][r_d][b_d][k_d]: # success
        A_dCenters = []
        pm, pr, pb, pk = len(I), r_d, b_d, k_d
        while pk > 0:
            c = lastC[pm][pr][pb][pk]
            if c != -1:
                A_dCenters.append([getColor(nPoints, c), getPId(nPoints, c)])
            pm, pr, pb, pk = choices[pm][pr][pb][pk]
        return A_dCenters, True
    else:
        return [], False

def getBluePseudo(graph, nColors, nCenters, nPoints, p, radius, simpleGraph):
    x, z, success = solveLP(nColors, nCenters, nPoints, p, graph, radius)
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
    
    # Round up blue
    y = roundBlue(nCenters, graph, y, S, D, b_D)

    return y, True

# Return: A subgraph for the points in P_s
def buildP_sSubgraph(P_s, nPoints, graph):
    newPos = zeros((len(P_s), 2), dtype=int)
    oldPos = zeros((len(P_s), 2), dtype=int)
    rCnt = 0
    bCnt = 0
    newId = 0
    for pos in range(len(P_s)):
        if P_s[pos]:
            if getColor(nPoints, pos) == 0:
                newPos[pos] = [0, rCnt]
                rCnt += 1
            else:
                newPos[pos] = [1, bCnt]
                bCnt += 1
            oldPos[newId] = [getColor(nPoints, pos), getPId(nPoints, pos)]
            newId += 1
    P_sGraph = zeros((2, max(rCnt, bCnt), 2, max(rCnt, bCnt)))
    for pos1 in range(len(P_s)):
        if P_s[pos1]:
            for pos2 in range(len(P_s)):
                if P_s[pos2]:
                    P_sGraph[newPos[pos1][0]][newPos[pos1][1]][newPos[pos2][0]][newPos[pos2][1]] = graph[getColor(nPoints, pos1)][getPId(nPoints, pos1)][getColor(nPoints, pos2)][getPId(nPoints, pos2)]
    return P_sGraph, [rCnt, bCnt], oldPos


# Return: centers in P_s
def A_s(nPoints, graph, P_s, k_s, r_s, b_s, radius):
    P_sGraph, P_sNPoints, oldPos = buildP_sSubgraph(P_s, nPoints, graph)
    y, success = getBluePseudo(P_sGraph, 2, k_s, P_sNPoints, [r_s, b_s], radius, simplifyGraph(2, P_sNPoints, P_sGraph)) 
    if not success:
        return [], False
    else:
        A_sCenters = []
        for pos in range(len(y)):
            if y[pos] == 1:
                A_sCenters.append(oldPos[pos].tolist())
            else:
                assert y[pos] == 0
        return A_sCenters, True
    

# Return: 3-approximation for fixed radius and whether successful
def fixedRadiusJSS20(nColors, nCenters, nPoints, p, graph, radius, flowers=True):
    assert nColors == 2, "JSS20 only implemented for 2 colors"
    simpleGraph = simplifyGraph(nColors, nPoints, graph)

    # Solve LP
    y, success = getBluePseudo(graph, nColors, nCenters, nPoints, p, radius, simpleGraph)
    if not success:
        return full((nCenters, 2), -1), False

    # TODO: if less centers just return nonSeparated
    nonSepCenters, isSeparated = testSeparated(simpleGraph, y, radius)
    if not isSeparated:
        return nonSepCenters, True

    # Phase 1: Guess 3 centers and construct q_i, P_i for these centers
    for c1 in range(sum(nPoints)):
        for c2 in range(c1 + 1, sum(nPoints)):
            for c3 in range(c2 + 1, sum(nPoints)):
                q, P, tau = getqP(nPoints, graph, [c1, c2, c3], radius)
                guessCenters = getOlds(nPoints, [c1, c2, c3])

                # Phase 2: Create P_s, P_d, I, D
                P_s, P_d, I, D = getP_sP_dI(nPoints, graph, simpleGraph, q, P[3], tau, radius)

                # Calculate how much is covered by the 3 centers
                k_left = nCenters - 3
                p_left = copy(p)
                for vId in range(len(P[3])):
                    if not P[3][vId]:
                        p_left[getColor(nPoints, vId)] = max(p_left[getColor(nPoints, vId)] - 1, 0)

                # Guess number of centers in P_d, number of red and blue points             
                for k_d in range(0, k_left+1):
                    for r_d in range(0, p_left[0]+1):
                        for b_d in range(0, p_left[1]+1):
                            A_dCenters, A_dSuccess = A_d(nPoints, graph, P_d, I, k_d, r_d, b_d, D, radius)
                            A_sCenters, A_sSuccess = A_s(nPoints, graph, P_s, k_left - k_d, p_left[0] - r_d, p_left[1] - b_d, radius)
                            if A_dSuccess and A_sSuccess: # possible optimization: return best if several guesses succeed
                                return guessCenters + A_dCenters + A_sCenters, True
    return full((nCenters, 2), -1), False


# Return: 3-approximation for colorful k-center by Jia et al.
def algoJSS20(nColors, nCenters, nPoints, p, graph):
    assert nColors == len(p)
    return binarySearchRadius(fixedRadiusJSS20, nColors, nCenters, nPoints, p, graph)

