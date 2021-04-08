from numpy import array
from os import execl
from numpy import random
import sys

# Summary: Read parameters from "configuration.py"
#          If it fails, user is asked to create new parameters
# Remark: This is unconventional and probably a bad way to do it
def getInput():
    try:
        from configuration import configuration
        print("Parameters taken from configuration.py")
        print("You can change or delete configuration.py and rerun")
        if configuration["fixSeed"]:
            random.seed(42)
        return configuration["nColors"], configuration["nCenters"], configuration["nPoints"], configuration["p"], configuration["shufflePoints"]
    except:
        confFile = open("configuration.py", "w")
        nColors = 1
        nCenters = 4
        nPoints = array([20])
        p = array([15])
        shufflePoints = True
        fixSeed = False
        print("Default? (y/n)")
        default = input()
        assert default == "y" or default == "n", "please restart and enter y or n instead"
        if default == "n":
            print("#colors? (1)")
            nColors = int(input())
            assert nColors >= 1 and nColors <= 1
            print("#centers? (1 - 1000)")
            nCenters = int(input())
            assert nCenters >= 1 and nCenters <= 1000
            print("#points? (1 - 1000)")
            nPoints[0] = int(input())
            assert nPoints[0] >= 1 and nPoints <= 1000
            print("#points to be covered? (1 - #points)")
            p[0] = int(input())
            assert p[0] <= nPoints
            print("Shuffle points? (y/n)")
            if input() == "y": 
                shufflePoints = True
            print("Fix seed? (y/n)")
            if input() == "y": 
                fixSeed = True
        else:
            assert default == "y", "default should be y or n"
        confFile.write("from numpy import array\n")
        confFile.write("configuration = {\n")
        confFile.write("    \"nColors\" : " + str(nColors) + ",\n")
        confFile.write("    \"nCenters\" : " + str(nCenters) + ",\n")
        confFile.write("    \"nPoints\" : array(["+ str(nPoints[0]))
        for col in range(1, len(nPoints)):
            confFile.write(", " + str(nPoints[col]))
        confFile.write("]),\n")
        confFile.write("    \"p\" : array(["+ str(p[0]))
        for col in range(1, len(nPoints)):
            confFile.write(", " + str(p[col]))
        confFile.write("]),\n")
        confFile.write("    \"shufflePoints\" : " + str(shufflePoints) + ",\n")
        confFile.write("    \"fixSeed\" : " + str(fixSeed) + ",\n")
        
        confFile.write("}\n")
        confFile.close()
        print("Parameters written to configuration.py")
        # Restart
        execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)
