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
# Recommended: nColors = 1, algoLetters = "ghcbork", nCenters = 3, nPointsList = [10, 50], nOutliersList = [0, 5], nRuns = 30 (ca. 2 minutew)
#          or: nColors = 1, algoLetters = "ghrk", nCenters = 10, nPointsList = [100, 300], nOutliersList = [0, 50], nRuns = 30
#          or: nColors = 2, algoLetters = "ghcborkj", nCenters = 4, nPointsList = [10, 20], nOutliersList = [0, 5], nRuns = 30
#          or: nColors = 2, algoLetters = "ghrk", nCenters = 10, nPointsList = [100, 300], nOutliersList = [0, 5], nRuns = 30

random.seed(0)
nColors = 2
algoLetters = "jo"
nCenters = 3 # Number of centers
nPointsList = [[20, 20], [50, 50]] # Number of points
nOutliersList = [[0, 0], [0, 15]] # Numbers of outliers
distribution = "uniform"
nRuns = 30 # Number of times to run algorithms
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


