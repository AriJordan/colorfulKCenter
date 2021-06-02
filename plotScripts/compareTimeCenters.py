if __name__ == "__main__":
    import allowScriptMain

import matplotlib.pyplot as plt
from numpy import array, full
from algorithmsRunner import algorithmsRunner
from instances import getRandomInstance
from result import result
from algorithms.algoInfo import algoList
try:
    from randomConfiguration import configuration
except:
    assert False, "Please first run main.py to create randomConfiguration.py"

### Only change these ###
# Recommended: nCentersList = [2, 5, 15], maxPoints = 200, maxTime = 0.3 (ca. 1 minute)
maxCenters = 50 # Maximum number of centers
nPointsList = [50, 100] # Number of points
maxTime = 30 # Maximum time allowed per algorithm run
nColors = 1
distribution="uniform"
#########################

fig, axs = plt.subplots(1, len(nPointsList), figsize=(6 * len(nPointsList), 5))
fig.suptitle('Runtime of different algorithms')
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
legendLines = []
legendNames = []
nCentersList = [[] for _ in range(len(nPointsList))]
for plotId in range(len(nPointsList)):
    algoSelection = array([(algo.letter == 'i' or algo.letter == 'k') for algo in algoList])
    allResults = [[] for _ in range(len(algoList))]

    nCenters = 2
    nPoints = nPointsList[plotId]
    while nCenters <= maxCenters:
        nCentersList[plotId].append(nCenters)
        instance = getRandomInstance(nColors=nColors, nPoints=[nPoints], distribution=distribution, nCenters=nCenters, p=[nPoints])
        algoRunner = algorithmsRunner(algoSelection, instance)
        results = algoRunner.runAlgorithmsOnce()
        for res in results:
            allResults[res.algoId].append(res.timeConsumed)
            if res.timeConsumed > maxTime: # Don't run algorithms for more than maxTime seconds
                algoSelection[res.algoId] = False
        nCenters += 1
          
    for algoId in range(len(algoList)):
        line, = axs[plotId].loglog(nCentersList[plotId][0:len(allResults[algoId])], allResults[algoId], color = algoList[algoId].color)
        if plotId == 0:
            legendLines.append(line)
            legendNames.append(algoList[algoId].name)
    axs[plotId].set_title("#points = " + str(nPointsList[plotId]))  
    axs[plotId].set(xlabel='#centers', ylabel='time consumed')
    axs[plotId].legend(legendLines, legendNames)
plt.show()

