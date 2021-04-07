from numpy import array
from random import seed

def getInput():
    print("Default (y/n)?")
    default = "y";
    #default = input()
    nColors = 1
    nCenters = 4
    nPoints = array([20])
    p = array([15])
    #rSeed = 42
    #seed(rSeed)
    if default == "n":
        print("# colors? (1)")
        nColors = int(input())
        assert nColors >= 1 and nColors <= 1
        print("# centers? (1 - 1000)")
        nCenters = int(input())
        assert nCenters >= 1 and nCenters <= 1000
        print("# points? (1 - 1000)")
        nPoints[0] = int(input())
        assert nPoints[0] >= 1 and nPoints <= 1000
        print("# points to be covered? (1 - # points)")
        p[0] = int(input())
        assert p[0] <= nPoints
    else:
        assert default == "y"

    return nColors, nCenters, nPoints, p
