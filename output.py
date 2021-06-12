import matplotlib.pyplot as plt
from numpy import zeros
from datetime import datetime
from algorithms.algoInfo import algoList

def printOutput(results):
    pointColors = [ "#FB1C2E", "#1622FE", "#00FD80", "#EAE916", "#00F9FC", "#7F2E58", "#FF16F9", "#F79245", "#4D7340", "#B4B1FB",
                    "#FA269F", "#F8DADF", "#8F0DB4", "#FF82DF", "#007182", "#946632", "#BE2638", "#8CF3BE", "#FE93A5", "#DEE49F",
                    "#73B60D", "#2292F9", "#BBE8FC", "#0DC0F3", "#0D4996", "#F9C555", "#CA00FF", "#93799D", "#FF6622", "#8FFC0D",
                    "#A078FF", "#FEBEFF", "#B32270", "#F100C3", "#5C473B", "#F1006C", "#FEC5A3", "#A5C4AF", "#9D4035", "#970D86",
                    "#8E8800", "#DD92FF", "#1CAC9C", "#169947", "#D691AF", "#1C38C3", "#7A4293", "#D140D1", "#9F956E", "#8EF793",
                    "#FE8177", "#FA608F", "#0DFEB2", "#9522FE", "#5A726D", "#D1EE76", "#3B4973", "#4F8CBE", "#94C879", "#42B8CC",
                    "#D88662", "#D9CDF5", "#00F5D5", "#8369C9", "#B970B0", "#0DFE32", "#DBCE5A", "#E475AC", "#9DEFE0", "#A26968",
                    "#D966FF", "#EA49AF", "#849EB8", "#A39495", "#76B1FF", "#D01C00", "#BDEE1C", "#45CD26", "#D45A00", "#5C75FE",
                    "#D18C1C", "#E3DCBF", "#CEAB60", "#68AD7F", "#760DC9", "#9ECEFE", "#837CB6", "#5C405C", "#B0556D", "#FCB2B6",
                    "#C716AA", "#99003D", "#B65800", "#538716", "#B55CC0", "#8A96FF", "#C495E2", "#94AA16", "#CEA79A", "#C8CED7" ]
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
                dot, = plt.plot(x, y, "o", color=pointColors[pointCol])
    plt.legend(legendCircles, legendNames)
    plt.savefig(datetime.now().strftime("plots\\outputCenters_%d-%m-%Y_%H;%M;%S"))
    plt.show()

    print("End reached!")