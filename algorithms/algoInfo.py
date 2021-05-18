from algorithms.randomCenters import algoRandomCenters
from algorithms.G85 import algoG85
from algorithms.HS86 import algoHS86
from algorithms.CKMN01 import algoCKMN01
from algorithms.BIPV19 import algoBIPV19
from algorithms.bruteForce import algoBruteForce
from algorithms.JSS20 import algoJSS20
from algorithms.LPhHeuristic import algoLPhHeuristic
from algorithms.hillClimbing import algoHillClimbing

# Class to represent different algorithms
class algoInfo: 
    algoIdCnt = 0
    def __init__(self, name, algo, letter, color):
        self.id = self.algoIdCnt
        self.algoIdCnt += 1
        self.name = name
        self.algo = algo
        self.letter = letter
        self.color = color

# List of different algorithms
# The letter representing the algorithm and the color must be unique
algoList = [ 
    # Guaranteed approximations
    algoInfo("G85", algoG85, "g", "g"),
    algoInfo("HS86", algoHS86, "h", "y"),
    algoInfo("CKMN01", algoCKMN01, "c", "c"),
    algoInfo("BIPV19", algoBIPV19, "b", "b"),
    algoInfo("JSS20", algoJSS20, "j", "r"),
    algoInfo("Optimal", algoBruteForce, "o", "k"),
    # Heuristics
    algoInfo("Random", algoRandomCenters, "r", "m"),
    algoInfo("helperLP", algoLPhHeuristic, "l", "#F79245"),
    algoInfo("hillClimbing", algoHillClimbing, "i", "#00FD80")
]
