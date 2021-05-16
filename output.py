import matplotlib.pyplot as plt
from numpy import zeros
from algorithms.algoInfo import algoList

def printOutput(results):
    pointColors = ["r", "b"]
    fig, ax = plt.subplots()
    legendCircles = []
    legendNames = []
    for result in results:
        for centerCol, centerId in result.centerIds:
            x = result.points[centerCol][centerId][0]
            y = result.points[centerCol][centerId][1]
            circle = ax.add_patch(plt.Circle((x, y), result.radius, color=algoList[result.algoId].color, fill=False))
        legendCircles.append(circle)
        legendNames.append(algoList[result.algoId].name + ": " + str(round(result.radius, 2)))
        for pointCol in range(len(result.points)):
            for pointId in range(len(result.points[pointCol])):
                x = result.points[pointCol][pointId][0]
                y = result.points[pointCol][pointId][1]
                dot, = plt.plot(x, y, pointColors[pointCol] + "o")
    plt.legend(legendCircles, legendNames)
    plt.show()

    print("End reached!")