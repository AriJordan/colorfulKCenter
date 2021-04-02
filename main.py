from input import getInput
from algorithmsRunner import algorithmsRunner
from output import printOutput

algoRunner = algorithmsRunner(*getInput())
printOutput(algoRunner.runAlgorithmsOnce())

