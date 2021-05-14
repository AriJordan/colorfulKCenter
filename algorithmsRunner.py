from numpy import linalg, random
from numpy import array, append, amax, full, resize, sort, inf, zeros
from result import result
from timeit import default_timer as timer
from algorithms.algoInfo import algoList

from instances import getRandomInstance, randomEuclPointsGraph


class algorithmsRunner():
    def __init__(self, algoSelection, nColors, nCenters, nPoints, p, distribution = "normal"):
        self.algoSelection = algoSelection
        self.nColors = nColors
        self.nCenters = nCenters
        self.nPoints = nPoints
        self.p = p
        self.distribution = distribution

    # Return: random points and corresponding graph
    def createPointsGraph(self, EuclidDim=2):
        points, graph = randomEuclPointsGraph(self.nColors, self.nPoints, self.distribution, EuclidDim)
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

    def addResult(self, algoId, results, points, graph, centerIds, timeConsumed):
        for centerId in range(self.nCenters):
            if centerIds[centerId][0] == -1:
                assert centerIds[centerId][1] == -1
                centerIds = resize(centerIds, (centerId + 1, 2))
                break
        results.append(result(algoId, points, self.calcMinRadius(centerIds, graph), centerIds, timeConsumed))

    def runAlgo(self, algoId, results, points, graph):
        print("Running " + algoList[algoId].name)
        startTime = timer()
        centerIds = algoList[algoId].algo(self.nColors, self.nCenters, self.nPoints, self.p, graph)
        endTime = timer()
        print("Time consumed: " + str(round(endTime - startTime, 6)) + " seconds")
        self.addResult(algoId, results, points, graph, centerIds, endTime - startTime)

    def runAlgorithmsOnce(self):
        points, graph = self.createPointsGraph()
        results = [] # python list because of append()

        for algoId in range(len(self.algoSelection)):
            if self.algoSelection[algoId]:
                self.runAlgo(algoId, results, points, graph)
                
        return results
