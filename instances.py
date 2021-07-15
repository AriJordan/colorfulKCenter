from numpy import array, amax, zeros, shape
from numpy import linalg, random
from randomConfiguration import configuration

class instance():
    '''
    points is a 3 dim array where points[colID][pointID] are the coordinates
    graph is a 4 dim array where graph[colID1][p1ID][colID2][p2ID] is the distance between p1 and p2
    nCenters is the number of centers to be opened
    p is an array where p[colID] is the number of points of colID to be covered
    '''
    def __init__(self, points, nCenters, p):
        self.points = points
        self.nCenters = nCenters
        self.p = p

    @property
    def nPoints(self):
        return array([sum(point.any() for point in colPoints) for colPoints in self.points])

    @property
    def nColors(self):
        return shape(self.points)[0]

    @property
    def graph(self):
        graph = zeros((self.nColors, amax(self.nPoints), self.nColors, amax(self.nPoints)))  # Indices: col1, point1Id, col2, point2Id
        for col1 in range(0, self.nColors):
                for point1Id in range(0, self.nPoints[col1]):
                    for col2 in range(0, self.nColors):
                        for point2Id in range(0, self.nPoints[col2]):
                            graph[col1][point1Id][col2][point2Id] = linalg.norm(self.points[col1][point1Id] - self.points[col2][point2Id])
        return graph

def randomEuclPoints(nColors, nPoints, distribution="normal", EuclidDim=2):
    points = zeros((nColors, amax(nPoints), EuclidDim))
    for col in range(0, nColors):
        for pointId in range(0, nPoints[col]):
            if distribution == "uniform":
                points[col][pointId] = random.uniform(size=EuclidDim)
            elif distribution == "normal":
                points[col][pointId] = random.standard_normal(size=EuclidDim)
            elif distribution == "exponential":
                points[col][pointId] = random.exponential(scale=1.0, size=EuclidDim)
            else:
                assert False, "Error: Unknown distribution"

    return points

def getRandomInstance(nColors = configuration["nColors"],
                      nPoints = configuration["nPoints"],
                      distribution = configuration["coordinateDistribution"],
                      nCenters = configuration["nCenters"],
                      p = configuration["p"]):
    points = randomEuclPoints(nColors, nPoints, distribution)
    return instance(points, nCenters, p)
