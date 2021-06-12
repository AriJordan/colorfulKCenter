if __name__ == "__main__":
    import allowScriptMain

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from numpy import column_stack, full, random
from datetime import datetime
from algorithmsRunner import algorithmsRunner
from instances import getRandomInstance
from result import result
from algorithms.algoInfo import algoList

### Only change these ###
# Recommended: algoLetters = "ghcbori", nCenters = 3, nPointsList = [10, 50], nOutliersList = [0, 5], nRuns = 30 (ca. 2 minutew)
#          or: 
algoLetters = "ghcbori"
random.seed(0)
nColors = 1
nCenters = 3 # Number of centers
nPointsList = [10, 50] # Number of points
nOutliersList = [0, 5] # Numbers of outliers
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
fig.suptitle('Approximation ratio for 1 color and ' + str(nCenters) + ' centers over ' + str(nRuns) + ' runs for ' + distribution + 'ly distributed points')
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
legendLines = []
legendNames = []
for subplotId1 in range(nSubplots1):
    for subplotId2 in range(nSubplots2):
        nPoints = nPointsList[subplotId1]
        nOutliers = nOutliersList[subplotId2]
        optResults = []
        allResults = [[] for _ in range(len(algoList))]

        for run in range(nRuns):
            instance = getRandomInstance(nColors=nColors, nPoints=[nPoints], distribution=distribution, nCenters=nCenters, p=[nPoints - nOutliers])
            algoRunner = algorithmsRunner(algoSelection, instance)
            results = algoRunner.runAlgorithmsOnce()
            for res in results:
                allResults[res.algoId].append(res.radius)
                if algoList[res.algoId].name == "Optimal":
                    optResults.append(res.radius)
            for res in results:
                allResults[res.algoId][run] = allResults[res.algoId][run] / optResults[run]

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


