from numpy import amax, full, resize, inf
from result import result
from timeit import default_timer as timer
from algorithms.algoInfo import algoList


class algorithmsRunner():
    def __init__(self, algoSelection, instance):
        self.algoSelection = algoSelection
        assert len(self.algoSelection) > 0, "No algorithms selected"
        self.nColors = instance.nColors
        assert self.nColors > 0, "There must be at least one color"
        self.nCenters = instance.nCenters
        assert self.nCenters > 0, "With 0 centers there is no solution at all"
        self.nPoints = instance.nPoints
        assert amax(self.nPoints) > 0, "There must be at least one point"
        self.p = instance.p
        assert amax(self.p) > 0, "There is nothing to be covered, all radii would be 0"
        for col in range(self.nColors):
            assert self.p[col] <= self.nPoints[col], "Can not cover more points than exist, no solution"
        self.points = instance.points
        self.graph = instance.graph


    def calcMinRadius(self, centerIds):
        maxDist = 0
        minDists = full((len(self.graph), amax(self.nPoints)), inf)
        for col in range(0, self.nColors):
            if self.nPoints[col] > 0:
                for pointId in range(0, self.nPoints[col]):
                    for centerCol, centerId in centerIds:
                        minDists[col][pointId] = min(minDists[col][pointId], self.graph[col][pointId][centerCol][centerId])
                minDists[col].sort()
                if self.p[col] > 0:
                    maxDist = max(maxDist, minDists[col][self.p[col] - 1])
        return maxDist

    def addResult(self, algoId, results, centerIds, timeConsumed):
        for centerId in range(len(centerIds)):
            if centerIds[centerId][0] == -1:
                assert centerIds[centerId][1] == -1
                centerIds = resize(centerIds, (centerId + 1, 2))
                break
        results.append(result(algoId, self.points, self.calcMinRadius(centerIds), centerIds, timeConsumed))

    def runAlgo(self, algoId, results):
        print("Running " + algoList[algoId].name)
        startTime = timer()
        if algoList[algoId].letter == 'k':
            centerIds = algoList[algoId].algo(self.nColors, self.nCenters, self.nPoints, self.p, self.graph, self.points)
        elif algoList[algoId].letter == 'g' or algoList[algoId].letter == 'h': # Don't count the preprocessing as runtime
            centerIds, startTime = algoList[algoId].algo(self.nColors, self.nCenters, self.nPoints, self.p, self.graph)
        else:
            centerIds = algoList[algoId].algo(self.nColors, self.nCenters, self.nPoints, self.p, self.graph)
        endTime = timer()
        print("Time consumed: " + str(round(endTime - startTime, 6)) + " seconds")
        print("Radius: ", round(self.calcMinRadius(centerIds),2))
        self.addResult(algoId, results, centerIds, endTime - startTime)

    def runAlgorithmsOnce(self):
        results = [] # python list because of append()

        for algoId in range(len(self.algoSelection)):
            if self.algoSelection[algoId]:
                self.runAlgo(algoId, results)
                
        return results
