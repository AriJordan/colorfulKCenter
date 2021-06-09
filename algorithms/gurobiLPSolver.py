from numpy import zeros, inf, array
import gurobipy as gp
from gurobipy import GRB

# Summary: Class to model Linear Programming
# Remark: Adapted from https://github.com/kth-competitive-programming/kactl/blob/master/content/numerical/Simplex.h
class gurobiLPSolver():

    # Args: A, b, linear constrains: Ax <= b
    #       c, objective (to minimize)
    def __init__(self, A, b, c):
        assert len(A) == len(b)
        assert len(A[0]) == len(c)
        self.A = A
        self.b = b
        self.c = c
        self.m = len(b)
        self.n = len(c)


    # Return: optimal value
    # Post: set x to an optimal solution (with minimum objective)
    def solve(self, x):

        with gp.Env(empty=True) as env:
            env.setParam('OutputFlag', 0)  # surpresses console output
            env.start()
            with gp.Model(env=env) as model:

                xvars = array([model.addVar(lb=0) for _ in x])

                model.setObjective(sum(self.c * xvars), GRB.MAXIMIZE)

                for i in range(self.m):
                    model.addConstr(sum(self.A[i, :]*xvars) <= self.b[i])

                model.optimize()

                ok = True if model.status == GRB.OPTIMAL else False

                return (model.objVal, array([var.x for var in xvars])) if ok else (inf, zeros(self.n))
