from data.mall.mallConfiguration import mallConfiguration
from instances import instance

def getMallInstance(totalPoints):
    points, graph = getMallPointsGraph(totalPoints)
    return instance(points, graph, mallConfiguration["nCenters"], mallConfiguration["p"])


def getMallPointsGraph(totalPoints):
    points = 0
    graph = 0

    # take a totalPoints subset of all points
    return points, graph

