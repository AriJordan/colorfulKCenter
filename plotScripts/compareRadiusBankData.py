if __name__ == "__main__":
    import allowScriptMain

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from numpy import column_stack, full, random
from datetime import datetime
from algorithmsRunner import algorithmsRunner
from input import getInput
from result import result
from algorithms.algoInfo import algoList
try:
    from data.bank.bankConfiguration import bankConfiguration
except:
    assert False, "Please fix bankConfiguration.py"

### Only change these ###
algoLetters = "ghcbork"
random.seed(0)
nRuns = 30 # Number of times to run algorithms
#########################

algoSelection = full((len(algoList)), False)
for algoId in range(len(algoList)):
    if algoLetters.count(algoList[algoId].letter):
        algoSelection[algoId] = True

nSubplots = 2
fig, axs = plt.subplots(1, nSubplots, figsize=(6 * nSubplots, 5))
fig.suptitle('Approximation ratio for bank data with ' + str(bankConfiguration["totalPoints"]) + ' points and coverage percentage: ' + str(100 * bankConfiguration["percentage"]))
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
legendLines = []
legendNames = []
for subplotId in range(nSubplots):
    bestResults = []
    allResults = [[] for _ in range(len(algoList))]
    for run in range(nRuns):
        trash, instance = getInput("bank")
        algoRunner = algorithmsRunner(algoSelection, instance)
        results = algoRunner.runAlgorithmsOnce()
        bestResult = inf
        for res in results:
            allResults[res.algoId].append(res.radius)
            bestResult = min(bestResult, res.radius)
        bestResults.append(bestResult)
        for res in results:
            allResults[res.algoId][run] = allResults[res.algoId][run] / bestResults[run]

    bp = axs[subplotId].boxplot([allResults[i] for i in range(len(algoSelection)) if algoSelection[i]])
    axs[subplotId].set_xticklabels([algoList[i].name for i in range(len(algoSelection)) if algoSelection[i]])
    #axs[subplotId].set_title("#centers = " + str(nCenters[subplotId]))
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

plt.savefig(datetime.now().strftime("plots\\bank_%d-%m-%Y_%H;%M;%S"))
plt.show()
