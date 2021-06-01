if __name__ == "__main__":
    import allowScriptMain

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from numpy import column_stack, full, random
from algorithmsRunner import algorithmsRunner
from instances import getRandomInstance
from result import result
from algorithms.algoInfo import algoList
try:
    from randomConfiguration import configuration
except:
    assert False, "Please first run main.py to create randomConfiguration.py"

### Only change these ###
# Recommended: nCenters = 4, nPoints = 20, nOutliersList = [0, 2, 5], nRuns = 20 (ca. 1 minute)
algoLetters = "ghcbori"
random.seed(0)
nColors = 1
nCenters = 3 # Number of centers
nPoints = 20  # Number of points
nOutliersList = [0, 5] # Numbers of outliers
distribution = "uniform"
nRuns = 5 # Number of times to run algorithms
#########################

algoSelection = full((len(algoList)), False)
for algoId in range(len(algoList)):
    if algoLetters.count(algoList[algoId].letter):
        algoSelection[algoId] = True

nSubplots = len(nOutliersList)
fig, axs = plt.subplots(1, nSubplots, figsize=(6 * nSubplots, 5))
fig.suptitle('Approximation ratio for 1 Color, ' + str(nPoints) + ' points and ' + str(nCenters) + ' centers')
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
legendLines = []
legendNames = []
for subplotId in range(nSubplots):
    nOutliers = nOutliersList[subplotId]
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

    bp = axs[subplotId].boxplot([allResults[i] for i in range(len(algoSelection)) if algoSelection[i]])
    axs[subplotId].set_xticklabels([algoList[i].name for i in range(len(algoSelection)) if algoSelection[i]])
    axs[subplotId].set_title("#outliers = " + str(nOutliersList[subplotId]))
    axs[subplotId].set(ylabel='Approximation ratio')

    # Add colors
    for boxId, algoId in enumerate([a for a in range(len(algoSelection)) if algoSelection[a]]):
        box = bp['boxes'][boxId]
        box_x = []
        box_y = []
        box_x.extend(box.get_xdata())
        box_y.extend(box.get_ydata())
        box_coords = column_stack([box_x, box_y])
        axs[subplotId].add_patch(Polygon(box_coords, facecolor=algoList[algoId].color))
plt.show()


