from algorithms.randomCenters import algoRandomCenters
from algorithms.G85 import algoG85
from algorithms.HS86 import algoHS86
from algorithms.CKMN01 import algoCKMN01
from algorithms.BIPV19 import algoBIPV19
from algorithms.bruteForce import algoBruteForce
from algorithms.JSS20 import algoJSS20
from algorithms.LPhHeuristic import algoLPhHeuristic
from algorithms.hillClimbing import algoHillClimbing
from algorithms.hillClimbingKDTree import algoHillClimbingKDTree

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
    algoInfo("Furthest", algoG85, "g", "g"), # Gonzales 1985
    algoInfo("Disks", algoHS86, "h", "y"), # Hochbaum & Shmoys 1986
    algoInfo("Densest", algoCKMN01, "c", "c"),
    algoInfo("Helper LP", algoBIPV19, "b", "b"),
    algoInfo("EPFL 3", algoJSS20, "j", "r"),
    algoInfo("Optimal", algoBruteForce, "o", "k"),
    # Heuristics
    algoInfo("Random", algoRandomCenters, "r", "m"),
    algoInfo("LP Heuristic", algoLPhHeuristic, "l", "#F79245"),
    #algoInfo("Hill Climbing", algoHillClimbing, "i", "#00FAFF"), # old
    algoInfo("Hill Climb", algoHillClimbingKDTree, "k", "#FFA500") # "#00FD80"
]
