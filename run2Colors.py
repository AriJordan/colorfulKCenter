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
    assert False, "Please first run main.py to create configuration.py"

### Only change these ###
random.seed(0)
nColors = 2 
nCenters = [4, 5] # Number of centers
nPoints = [5, 5]  # Number of points
p = [3, 4] # Number of points to cover
nRuns = 10 # Number of times to run algorithms
algoSelection = full((len(algoList)), False)
for algoId in range(len(algoList)):
    if algoList[algoId].name == "JSS20" or algoList[algoId].name == "Optimal": # JSS20 and optimal algorithms
        algoSelection[algoId] = True
#########################

nSubplots = len(nCenters)
fig, axs = plt.subplots(1, nSubplots, figsize=(6 * nSubplots, 5))
fig.suptitle('Approximation ratio of different algorithms for nPoints: ' + str(nPoints) + ' and p: ' + str(p))
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
legendLines = []
legendNames = []
for subplotId in range(nSubplots):
    optResults = []
    allResults = [[] for _ in range(len(algoList))]
    for run in range(nRuns):
        instance = getRandomInstance(nColors=nColors, nPoints = nPoints, distribution="normal", nCenters=nCenters[subplotId], p=p)
        algoRunner = algorithmsRunner(algoSelection, instance) #nColors, nCenters[subplotId], nPoints, p,
        results = algoRunner.runAlgorithmsOnce()
        for res in results:
            allResults[res.algoId].append(res.radius)
            if algoList[res.algoId].name == "Optimal":
                optResults.append(res.radius)
        for res in results:
            allResults[res.algoId][run] = allResults[res.algoId][run] / optResults[run]

    bp = axs[subplotId].boxplot(allResults)
    axs[subplotId].set_xticklabels([algoList[i].name for i in range(len(algoList))])
    axs[subplotId].set_title("#centers = " + str(nCenters[subplotId]))
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

