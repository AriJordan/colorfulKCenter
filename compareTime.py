import matplotlib.pyplot as plt
from numpy import full
from algorithmsRunner import algorithmsRunner
from result import result
from algorithms.algoInfo import algoList
try:
    from configuration import configuration
except:
    assert False, "Please first run main.py to create configuration.py"

### Only change these ###
# Recommended: nCentersList = [2, 5, 15], maxPoints = 200, maxTime = 0.3 (ca. 1 minute)
nCentersList = [2, 10] # Different numbers of centers
maxPoints = 200 # Maximum number of points
maxTime = 0.3 # Maximum time allowed per algorithm run
#########################

fig, axs = plt.subplots(1, len(nCentersList), figsize=(6 * len(nCentersList), 5))
fig.suptitle('Runtime of different algorithms')
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
legendLines = []
legendNames = []
nPointsList = [[] for _ in range(len(nCentersList))]
for nCentersId in range(len(nCentersList)):
    allResults = [[] for _ in range(len(algoList))]

    algoSelection = full((len(algoList)), False)
    for algoId in range(len(algoList)):
        if configuration["algoLetters"].count(algoList[algoId].letter):
            algoSelection[algoId] = True

    nPoints = nCentersList[nCentersId]
    while nPoints <= maxPoints:
        nPointsList[nCentersId].append(nPoints)
        algoRunner = algorithmsRunner(algoSelection, configuration["nColors"], nCentersList[nCentersId], [nPoints], [nPoints], configuration["shufflePoints"], configuration["coordinateDistribution"])
        results = algoRunner.runAlgorithmsOnce()
        for res in results:
            allResults[res.algoId].append(res.timeConsumed)
            if res.timeConsumed > maxTime: # Don't run algorithms for more than maxTime seconds
                algoSelection[res.algoId] = False
        nPoints = int(nPoints * 1.05 + 1)
          
    for algoId in range(len(algoList)):
        line, = axs[nCentersId].loglog(nPointsList[nCentersId][0:len(allResults[algoId])], allResults[algoId], color = algoList[algoId].color)
        if nCentersId == 0:
            legendLines.append(line)
            legendNames.append(algoList[algoId].name)
    axs[nCentersId].set_title("#centers = " + str(nCentersList[nCentersId]))  
    axs[nCentersId].set(xlabel='#points', ylabel='time consumed')
    axs[nCentersId].legend(legendLines, legendNames)
plt.show()

