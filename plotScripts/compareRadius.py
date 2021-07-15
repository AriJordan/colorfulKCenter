if __name__ == "__main__":
    import allowScriptMain

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from numpy import column_stack, full, random, inf
from datetime import datetime
from algorithmsRunner import algorithmsRunner
from instances import getRandomInstance
from result import result
from algorithms.algoInfo import algoList

### Only change these ###
# See scriptConfigurations.txt for some possible configurations

random.seed(0)
nColors = 2
algoLetters = "ghcbrk"
nCenters = 20
nPointsList = [[70, 70], [30, 30]]
nOutliersList = [[0, 0], [0, 20]]
distribution = "exponential"
nRuns = 10 # Number of times to run algorithms
#########################

algoSelection = full((len(algoList)), False)
for algoId in range(len(algoList)):
    if algoLetters.count(algoList[algoId].letter):
        algoSelection[algoId] = True

nSubplots1 = len(nPointsList)
nSubplots2 = len(nOutliersList)
fig, axs = plt.subplots(nSubplots1, nSubplots2, figsize=(6 * nSubplots1, 6 * nSubplots2))
fig.suptitle('Approximation ratio for ' + str(nColors) + ' colors and ' + str(nCenters) + ' centers over ' + str(nRuns) + ' runs for ' + distribution + 'ly distributed points')
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
legendLines = []
legendNames = []
for subplotId1 in range(nSubplots1):
    for subplotId2 in range(nSubplots2):
        nPoints = nPointsList[subplotId1]
        nOutliers = nOutliersList[subplotId2]
        bestResults = []
        allResults = [[] for _ in range(len(algoList))]

        for run in range(nRuns):
            print("Subplot: (", subplotId1, ", ", subplotId2, "), run: ", run+1, sep="")
            instance = getRandomInstance(nColors=nColors, nPoints=nPoints, distribution=distribution, nCenters=nCenters, p=[nPoints[i] - nOutliers[i] for i in range(nColors)])
            algoRunner = algorithmsRunner(algoSelection, instance)
            results = algoRunner.runAlgorithmsOnce()
            bestResult = inf
            for res in results:
                allResults[res.algoId].append(res.radius)
                bestResult = min(bestResult, res.radius)
            bestResults.append(bestResult)
            for res in results:
                allResults[res.algoId][run] = allResults[res.algoId][run] / bestResults[run]

        bp = axs[subplotId1][subplotId2].boxplot([allResults[i] for i in range(len(algoSelection)) if algoSelection[i]])
        axs[subplotId1][subplotId2].set_xticklabels([algoList[i].name for i in range(len(algoSelection)) if algoSelection[i]])
        axs[subplotId1][subplotId2].set_title("#points = " + str(nPointsList[subplotId1]) + ", #outliers = " + str(nOutliersList[subplotId2]))
        axs[subplotId1][subplotId2].set(ylabel='Approximation ratio')

        # Add colors
        for boxId, algoId in enumerate([a for a in range(len(algoSelection)) if algoSelection[a]]):
            box = bp['boxes'][boxId]
            box_x = []
            box_y = []
            box_x.extend(box.get_xdata())
            box_y.extend(box.get_ydata())
            box_coords = column_stack([box_x, box_y])
            axs[subplotId1][subplotId2].add_patch(Polygon(box_coords, facecolor=algoList[algoId].color))

plt.savefig(datetime.now().strftime("plots\\radius_%d-%m-%Y_%H;%M;%S"))
plt.show()


