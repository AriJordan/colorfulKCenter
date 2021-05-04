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
    return sum(nPoints[0:col] + pId)

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