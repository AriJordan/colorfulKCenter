from data.mall.mallConfiguration import mallConfiguration
from instances import instance

def getMallInstance():
    points, graph = getMallPointsGraph()
    return instance(points, graph, mallConfiguration["nCenters"], mallConfiguration["p"])


def getMallPointsGraph():
    points = 0
    graph = 0

    # take only a subset of points via configuration["nPoints"] ?
    return points, graph

