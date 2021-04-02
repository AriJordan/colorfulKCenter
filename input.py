from numpy import array

def getInput():
    print("Default (y/n)?")
    default = "y";
    #default = input()
    nColors = 1
    nCenters = 3
    nPoints = array([10])
    p = array([10])
    if default == "n":
        print("# colors? (1)")
        nColors = int(input())
        assert nColors >= 1 and nColors <= 1
        print("# centers? (1 - 10)")
        nCenters = int(input())
        assert nCenters >= 1 and nCenters <= 10
        print("# points? (1 - 50)")
        nPoints[0] = int(input())
        assert nPoints[0] >= 1 and nPoints <= 50
        print("# points to be covered? (1 - # points)")
        p[0] = int(input())
        assert p[0] <= nPoints
    else:
        assert default == "y"

    return nColors, nCenters, nPoints, p
