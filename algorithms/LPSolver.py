from algorithms.gurobiLPSolver import gurobiLPSolver
from algorithms.simplexLPSolver import simplexLPSolver

select = 0
selection = {0: gurobiLPSolver, 1: simplexLPSolver}

LPSolver = selection[select]