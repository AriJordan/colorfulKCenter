import matplotlib.pyplot as plt
from numpy import zeros

def printOutput(results):
    colors = ["r", "b"]
    for result in results:
        print(result.radius)
    for result in results:
        fig, ax = plt.subplots()
        for centerCol, centerId in result.centerIds:
            x = result.points[centerCol][centerId][0]
            y = result.points[centerCol][centerId][1]
            ax.add_patch(plt.Circle((x, y), result.radius, color='k', fill=False))
        for pointCol in range(len(result.points)):
            for pointId in range(len(result.points[pointCol])):
                x = result.points[pointCol][pointId][0]
                y = result.points[pointCol][pointId][1]
                plt.plot(x, y, colors[pointCol] + "o")
        plt.show()

    print("End reached!")