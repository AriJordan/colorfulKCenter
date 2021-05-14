from numpy import array, append, amax, full, resize, sort, inf, zeros, shape
from numpy import linalg, random

class instance():
    def __init__(self, points, graph, nCenters, p):
        self.points = points
        self.graph = graph
        self.nCenters = nCenters
        self.p = p
        # self.nColors = shape(points)[0]

def randomEuclPointsGraph(nColors, nPoints, distribution="normal", EuclidDim=2):
    points = zeros((nColors, amax(nPoints), EuclidDim))
    for col in range(0, nColors):
        for pointId in range(0, nPoints[col]):
            if distribution == "uniform":
                points[col][pointId] = random.uniform(size=EuclidDim)
            elif distribution == "normal":
                points[col][pointId] = random.standard_normal(size=EuclidDim)
            elif distribution == "exponential":
                points[col][pointId] = random.standard_exponential(size=EuclidDim)
            else:
                assert False, "Error: Unknown distribution"

    graph = zeros((nColors, amax(nPoints), nColors, amax(nPoints)))  # Indices: col1, point1Id, col2, point2Id
    for col1 in range(0, nColors):
        for point1Id in range(0, nPoints[col1]):
            for col2 in range(0, nColors):
                for point2Id in range(0, nPoints[col2]):
                    graph[col1][point1Id][col2][point2Id] = linalg.norm(points[col1][point1Id] - points[col2][point2Id])
    return points, graph

def getRandomInstance():
    from randomConfiguration import configuration
    points, graph = randomEuclPointsGraph(configuration["nColors"], configuration["nPoints"], configuration["coordinateDistribution"])
    return instance(points, graph, configuration["nCenters"], configuration["p"])

