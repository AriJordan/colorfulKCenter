from random import random
from numpy import array, full, zeros, append, amax, linalg, sort, inf
from result import result
from algorithms.G85 import algoG85
from algorithms.HS86 import algoHS86
from algorithms.CKMN01 import algoCKMN01

class algorithmsRunner():
    def __init__(self, nColors, nCenters, nPoints, p):
        self.nColors = nColors
        self.nCenters = nCenters
        self.nPoints = nPoints
        self.p = p

    # Return: random points and corresponding graph
    def createPointsGraph(self, EuclidDim = 2):
        points = zeros((self.nColors, amax(self.nPoints), EuclidDim))
        for col in range(0, self.nColors):
            for pointId in range(0, self.nPoints[col]):
                for dim in range(0, EuclidDim):
                    points[col][pointId][dim] = random()
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

    def addResult(self, algoName, points, results, centerIds, graph):
        results.append(result(algoName, points, self.calcMinRadius(centerIds, graph), centerIds))

    def runAlgorithmsOnce(self):
        points, graph = self.createPointsGraph()
        results = [] # python list because of append()
        
        if self.nColors == 1: # and self.nPoints[0] == self.p[0]: # no outliers
            self.addResult("G85", points, results, algoG85(self.nCenters, self.nPoints, graph), graph)
            self.addResult("HS86", points, results, algoHS86(self.nColors, self.nCenters, self.nPoints, self.p, graph), graph)
            self.addResult("CKMN01", points, results, algoCKMN01(self.nColors, self.nCenters, self.nPoints, self.p, graph), graph)
            return results
