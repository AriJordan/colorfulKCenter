from numpy import zeros

# Turns a 4-dimensional graph into a simplified graph, which ignores colors
def simplifyGraph(nColors, nPoints, graph):
    simpleGraph = zeros((sum(nPoints), sum(nPoints)))
    for col1 in range(nColors):
        for v1 in range(nPoints[col1]):
            for col2 in range(nColors):
                for v2 in range(nPoints[col2]):
                    simpleGraph[sum(nPoints[0:col1]) + v1][sum(nPoints[0:col2]) + v2] = graph[col1][v1][col2][v2]
    return simpleGraph

# Return: Id in simpleGraph
def simpleId(nPoints, col, pId):
    return sum(nPoints[0:col]) + pId

# Return: original color of point
def getColor(nPoints, v):
    color = 0
    pSum = nPoints[color]
    while(pSum <= v):
        color += 1
        pSum += nPoints[color]           
    return color

# Return: original id of point
def getPId(nPoints, v):
    color = 0
    pId = v
    while(nPoints[color] <= pId):        
        pId -= nPoints[color]
        color += 1
    return pId

# Return: old ids and colors of points
def getOlds(nPoints, vs):
    old = []
    for v in vs:
        old.append([getColor(nPoints, v), getPId(nPoints, v)])
    return old

def ignoreColors(nColors, nPoints, graph):
    simpleGraph = simplifyGraph(nColors, nPoints, graph)
    graph = zeros((1, len(simpleGraph), 1, len(simpleGraph)))
    for v1 in range(len(simpleGraph)):
        for v2 in range(len(simpleGraph)):
            graph[0][v1][0][v2] = simpleGraph[v1][v2]
    return graph