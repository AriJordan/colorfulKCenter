if __name__ == "__main__":
    import allowScriptMain

import matplotlib.pyplot as plt
from numpy import array, full
from datetime import datetime
from algorithmsRunner import algorithmsRunner
from instances import getRandomInstance
from result import result
from algorithms.algoInfo import algoList

### Only change these ###
# Recommended: nCentersList = [2, 5, 15], maxPoints = 200, maxTime = 0.3 (ca. 1 minute)
nCentersList = [2, 10] # Different numbers of centers
maxPoints = 200 # Maximum number of points
maxTime = 0.2 # Maximum time allowed per algorithm run
nColors = 1
distribution="uniform"
#########################

fig, axs = plt.subplots(1, len(nCentersList), figsize=(6 * len(nCentersList), 5))
fig.suptitle('Runtime of different algorithms')
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
legendLines = []
legendNames = []
nPointsList = [[] for _ in range(len(nCentersList))]
for nCentersId in range(len(nCentersList)):
    algoSelection = array([(algo.letter != 'j' and algo.letter!= 'l') for algo in algoList])
    allResults = [[] for _ in range(len(algoList))]

    nPoints = nCentersList[nCentersId]
    while nPoints <= maxPoints:
        nPointsList[nCentersId].append(nPoints)
        instance = getRandomInstance(nColors=nColors, nPoints=[nPoints], distribution=distribution, nCenters=nCentersList[nCentersId], p=[nPoints])
        algoRunner = algorithmsRunner(algoSelection, instance)
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


plt.savefig(datetime.now().strftime("plots\\time_%d-%m-%Y_%H;%M;%S"))
plt.show()

