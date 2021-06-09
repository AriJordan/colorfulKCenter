import gurobipy as gp
from gurobipy import GRB
from numpy import array

import sys
sys.path.append('.')

from algorithms.gurobiLPSolver import gurobiLPSolver

try:
    A = array([[1,2],[0,4]])

    b = array([2,3])

    c = array([3,4])

    g = gurobiLPSolver(A, b, c)

    opt = g.solve(array([0,0]))

    print('opt value is ', opt)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')#