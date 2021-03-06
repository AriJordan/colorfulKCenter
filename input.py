from numpy import random
from os import execl
import sys
from numpy import array, full
from algorithms.algoInfo import algoList
from data.mall.conversion import getMallInstance
from data.bank.conversion import getBankInstance
from instances import getRandomInstance

# Summary: Read parameters from "randomConfiguration.py"
#          If it fails, user is asked to create new parameters
# Remark: This is unconventional and probably a bad way to do it


def getInput(instanceType):
    if instanceType=="random":
        try:  #
            from randomConfiguration import configuration
            print("Parameters taken from randomConfiguration.py")
            print("You can change or delete randomConfiguration.py and rerun program")
            algoSelection = full((len(algoList)), False)
            for algoId in range(len(algoList)):
                if configuration["algoLetters"].count(algoList[algoId].letter):
                    algoSelection[algoId] = True
            if configuration["fixSeed"]:
                random.seed(42)

            instance = getRandomInstance()
            return algoSelection, instance
        except:
            confFile = open("randomConfiguration.py", "w")
            algoLetters = ""
            for algoInfo in algoList:
                algoLetters = algoLetters + algoInfo.letter
            nColors = 1
            nCenters = 4
            nPoints = array([20])
            p = array([15])
            shufflePoints = True
            fixSeed = False
            distribution = "uniform"
            print("Default? (y/n)")
            default = input()
            assert default == "y" or default == "n", "please restart and enter y or n instead"
            if default == "n":
                print("Enter letters for algorithms to run:")
                for algoInfo in algoList:
                    print(algoInfo.letter + " for " + algoInfo.name)
                print("For example enter \"" + algoLetters + "\" (without quotes) to run all algorithms")
                algoLetters = input()
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
                print("Fix seed? (y/n)")
                if input() == "y":
                    fixSeed = True
                distributions = ["uniform", "normal", "exponential"]
                print("What coordinate distribution? Options are:")
                for dist in distributions:
                    print("\"" + dist + "\"", sep = ", ")
                print("(witout quotes)")
                distribution = input()
                assert distribution == "uniform" or distribution == "normal" or distribution == "exponential"
            else:
                assert default == "y", "default should be y or n"

            # Write file randomConfiguration.py
            confFile.write("from numpy import array\n")
            confFile.write("configuration = {\n")
            confFile.write("    \"algoLetters\" : \"" + algoLetters + "\",\n")
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
            confFile.write("    \"fixSeed\" : " + str(fixSeed) + ",\n")
            confFile.write("    \"coordinateDistribution\" : \"" + distribution + "\",\n")

            confFile.write("}\n")
            confFile.close()
            print("Parameters written to randomConfiguration.py")

            # Restart
            execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)
    elif instanceType=="mall":
        from data.mall.mallConfiguration import mallConfiguration
        print("Parameters taken from mallConfiguration.py")
        algoSelection = full((len(algoList)), False)
        for algoId in range(len(algoList)):
            if mallConfiguration["algoLetters"].count(algoList[algoId].letter):
                algoSelection[algoId] = True
        instance = getMallInstance()
        return algoSelection, instance

    elif instanceType=="bank":
        from data.bank.bankConfiguration import bankConfiguration
        print("Parameters taken form bankConfiguration.py")
        algoSelection = full((len(algoList)), False)
        for algoId in range(len(algoList)):
            if bankConfiguration["algoLetters"].count(algoList[algoId].letter):
                algoSelection[algoId] = True

        instance = getBankInstance()
        return algoSelection, instance
