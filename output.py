import matplotlib.pyplot as plt
from numpy import zeros

def printOutput(results):
    pointColors = ["r", "b"]
    algoColors = {
      "G85": "k",
      "HS86": "g",
      "CKMN01": "m",
    }
    for result in results:
        print(result.radius)       
    fig, ax = plt.subplots()
    legendCircles = []
    legendNames = []
    for result in results:
        for centerCol, centerId in result.centerIds:
            x = result.points[centerCol][centerId][0]
            y = result.points[centerCol][centerId][1]
            circle = ax.add_patch(plt.Circle((x, y), result.radius, color=algoColors[result.algoName], fill=False))
        legendCircles.append(circle)
        legendNames.append(result.algoName + ": " + str(round(result.radius, 3)))
        for pointCol in range(len(result.points)):
            for pointId in range(len(result.points[pointCol])):
                x = result.points[pointCol][pointId][0]
                y = result.points[pointCol][pointId][1]
                dot, = plt.plot(x, y, pointColors[pointCol] + "o")
    plt.legend(legendCircles, legendNames)
    plt.show()

    print("End reached!")