from numpy import linalg, random
from numpy import array, append, amax, full, resize, sort, inf, zeros
from result import result
from algorithms.bruteForce import algoBruteForce
from algorithms.G85 import algoG85
from algorithms.HS86 import algoHS86
from algorithms.CKMN01 import algoCKMN01
from algorithms.BIPV19 import algoBIPV19
from algorithms.randomCenters import algoRandomCenters

class algorithmsRunner():
    def __init__(self, nColors, nCenters, nPoints, p, shufflePoints):
        self.nColors = nColors
        self.nCenters = nCenters
        self.nPoints = nPoints
        self.p = p
        self.shufflePoints = shufflePoints

    # Return: random points and corresponding graph
    def createPointsGraph(self, EuclidDim = 2):
        points = zeros((self.nColors, amax(self.nPoints), EuclidDim))
        for col in range(0, self.nColors):
            for pointId in range(0, self.nPoints[col]):
                for dim in range(0, EuclidDim):
                    points[col][pointId][dim] = random.random()
        if self.shufflePoints: # TODO: This only makes sense when reading data from file
            random.shuffle(points)
        graph = zeros((self.nColors, amax(self.nPoints), self.nColors, amax(self.nPoints))) # Indices: col1, point1Id, col2, point2Id
        for col1 in range(0, self.nColors):
            for point1Id in range(0, self.nPoints[col1]):
                for col2 in range(0, self.nColors):
                    for point2Id in range(0, self.nPoints[col2]):
                        graph[col1][point1Id][col2][point2Id] = linalg.norm(points[col1][point1Id] - points[col2][point2Id])
        return points, graph


    def calcMinRadius(self, centerIds, graph):
        maxDist = 0
        for col in range(0, self.nColors):
            minDists = full((amax(self.nPoints)), inf)
            for pointId in range(0, self.nPoints[col]):
                for centerCol, centerId in centerIds:
                    minDists[pointId] = min(minDists[pointId], graph[col][pointId][centerCol][centerId])
            minDists.sort()
            maxDist = max(maxDist, minDists[self.p[col] - 1])
        return maxDist

    def addResult(self, algoName, results, points, graph, centerIds):
        for centerId in range(self.nCenters):
            if centerIds[centerId][0] == -1:
                assert centerIds[centerId][1] == -1
                centerIds = resize(centerIds, (centerId + 1, 2))
                break
        results.append(result(algoName, points, self.calcMinRadius(centerIds, graph), centerIds))

    def runAlgo(self, name, algo, results, points, graph):
        self.addResult(name, results, points, graph, algo(self.nColors, self.nCenters, self.nPoints, self.p, graph))


    def runAlgorithmsOnce(self):
        points, graph = self.createPointsGraph()
        results = [] # python list because of append()
        
        if self.nColors == 1: # and self.nPoints[0] == self.p[0]: # no outliers
            self.runAlgo("Optimal", algoBruteForce, results, points, graph)
            self.runAlgo("G85", algoG85, results, points, graph)
            self.runAlgo("HS86", algoHS86, results, points, graph)
            self.runAlgo("CKMN01", algoCKMN01, results, points, graph)
            self.runAlgo("BIPV19", algoBIPV19, results, points, graph)
            self.runAlgo("Random", algoRandomCenters, results, points, graph)
            return results
