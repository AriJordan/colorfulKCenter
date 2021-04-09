from numpy import linalg, random
from numpy import array, append, amax, full, resize, sort, inf, zeros
from result import result
from timeit import default_timer as timer
from algorithms.algoInfo import algoList


class algorithmsRunner():
    def __init__(self, algoSelection, nColors, nCenters, nPoints, p, shufflePoints):
        self.algoSelection = algoSelection
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
