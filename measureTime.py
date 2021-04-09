import matplotlib.pyplot as plt
from numpy import full
from algorithmsRunner import algorithmsRunner
from result import result
from output import printOutput
from algorithms.algoInfo import algoList
try:
    from configuration import configuration
except:
    assert False, "Please first run main.py to create configuration.py"

nCentersList = [2, 5, 10, 20, 50, 100]
maxPoints = 100
maxTime = 1.0

allResults = [[] for _ in range(len(algoList))]

algoSelection = full((len(algoList)), False)
for algoId in range(len(algoList)):
    if configuration["algoLetters"].count(algoList[algoId].letter):
        algoSelection[algoId] = True

nCenters = 5
for nPoints in range(nCenters, maxPoints):
    algoRunner = algorithmsRunner(algoSelection, configuration["nColors"], nCenters, [nPoints], [nPoints], False)
    results = algoRunner.runAlgorithmsOnce()
    for res in results:
        allResults[res.algoId].append(res.timeConsumed)
        if res.timeConsumed > maxTime: # Don't run algorithms for more than a second
            algoSelection[res.algoId] = False
legendLines = []
legendNames = []
for algoId in range(len(algoList)):
    line, = plt.loglog([i for i in range (nCenters, nCenters + len(allResults[algoId]))], allResults[algoId], color = algoList[algoId].color)
    legendLines.append(line)
    legendNames.append(algoList[algoId].name)
plt.title("#centers = " + str(nCenters))
plt.legend(legendLines, legendNames)
plt.xlabel('#points')
plt.ylabel('time consumed')
plt.show()

