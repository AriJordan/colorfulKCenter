import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from numpy import column_stack, full
from algorithmsRunner import algorithmsRunner
from result import result
from algorithms.algoInfo import algoList
try:
    from configuration import configuration
except:
    assert False, "Please first run main.py to create configuration.py"

### Only change these ###
# Recommended: nCenters = 4, nPoints = 20, nOutliersList = [0, 2, 5], nRuns = 20 (ca. 1 minute)
nCenters = 3 # Number of centers
nPoints = 20  # Number of points
nOutliersList = [0, 2, 5] # Numbers of outliers
nRuns = 20 # Number of times to run algorithms
#########################

nSubplots = len(nOutliersList)
fig, axs = plt.subplots(1, nSubplots, figsize=(6 * nSubplots, 5))
fig.suptitle('Approximation ratio of different algorithms for ' + str(nPoints) + ' points')
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
legendLines = []
legendNames = []
for subplotId in range(nSubplots):
    nOutliers = nOutliersList[subplotId]
    optResults = []
    allResults = [[] for _ in range(len(algoList))]

    algoSelection = full((len(algoList)), False)
    for algoId in range(len(algoList)):
        if configuration["algoLetters"].count(algoList[algoId].letter):
            algoSelection[algoId] = True

    for run in range(nRuns):
        algoRunner = algorithmsRunner(algoSelection, configuration["nColors"], nCenters, [nPoints], [nPoints - nOutliers], configuration["shufflePoints"], configuration["coordinateDistribution"])
        results = algoRunner.runAlgorithmsOnce()
        for res in results:
            allResults[res.algoId].append(res.radius)
            if algoList[res.algoId].name == "Optimal":
                optResults.append(res.radius)
        for res in results:
            allResults[res.algoId][run] = allResults[res.algoId][run] / optResults[run]

    bp = axs[subplotId].boxplot(allResults)
    axs[subplotId].set_xticklabels([algoList[i].name for i in range(len(algoList))])
    axs[subplotId].set_title("#outliers = " + str(nOutliers))
    axs[subplotId].set(ylabel='Approximation ratio')

    # Add colors
    for algoId in range(len(algoList)):
        box = bp['boxes'][algoId]
        box_x = []
        box_y = []
        box_x.extend(box.get_xdata())
        box_y.extend(box.get_ydata())
        box_coords = column_stack([box_x, box_y])
        axs[subplotId].add_patch(Polygon(box_coords, facecolor=algoList[algoId].color))
plt.show()


