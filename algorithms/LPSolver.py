from numpy import zeros, inf

# Summary: Class to model Linear Programming
# Remark: Adapted from https://github.com/kth-competitive-programming/kactl/blob/master/content/numerical/Simplex.h
class LPSolver():

    # Args: A, b, linear constrains: Ax <= b
    #       c, objective (to minimize)
    def __init__(self, A, b, c):
        assert len(A) == len(b)
        assert len(A[0]) == len(c)
        self.m = len(b)
        self.n = len(c)
        self.N = zeros((self.n + 1))
        self.B = zeros((self.m), dtype = int)
        self.D = zeros((self.m + 2, self.n + 2))
        for i in range(self.m):
            for j in range(self.n):
                self.D[i][j] = A[i][j]
        for i in range(self.m):
            self.B[i] = self.n + i
            self.D[i][self.n] = -1
            self.D[i][self.n + 1] = b[i]    
        for j in range(self.n):
            self.N[j] = j
        self.D[self.m][0:self.n] = c
        self.N[self.n] = -1
        self.D[self.m + 1][self.n] = 1

    def pivot(self, r, s):
        a = self.D[r]
        inv = 1.0 / a[s]
        for i in range(self.m + 2):
            if i != r and abs(self.D[i][s]) > 1e-6:
                b = self.D[i]
                inv2 = b[s] * inv
                b -= a * inv2
                b[s] = a[s] * inv2
        for j in range(self.n + 2): # TODO: optimize for numpy
            if (j != s):
                self.D[r][j] *= inv
        for i in range(self.m + 2):
            if(i != r):
                self.D[i][s] *= -inv
        self.D[r][s] = inv
        self.B[r], self.N[s] = self.N[s], self.B[r]

    # Return: Whether (a1, a2) < (b1, b2)
    def lexLess(self, a1, a2, b1, b2):
        return a1 < b1 or (a1 == b1 and a2 < b2)

    # Return: New pivot if better
    def minPivot(self, Di, N, j, s):
        if s == -1 or self.lexLess(Di[j], N[j], Di[s], N[s]):
            return j
        else:
            return s

    def simplex(self, phase):
        x = self.m + phase - 1
        while True:
            s = -1
            for j in range(self.n + 1):
                if self.N[j] != -phase:
                    s = self.minPivot(self.D[x], self.N, j, s)
            if self.D[x][s] >= -1e-6:
                return True
            r = -1
            for i in range(self.m):
                if self.D[i][s] <= 1e-6:
                    continue
                if r == -1 or self.lexLess(self.D[i][self.n+1] / self.D[i][s], self.B[i],
                                      self.D[r][self.n+1] / self.D[r][s], self.B[r]):
                    r = i
            if r == -1:
                return false
            self.pivot(r, s)

    # Return: optimal value
    # Post: set x to an optimal solution (with minimum objective)
    def solve(self, x):
        r = 0
        for i in range(1, self.m):
            if self.D[i][self.n + 1] < self.D[r][self.n + 1]:
                r = i
        if self.D[r][self.n + 1] < -1e-6:
            self.pivot(r, self.n)
            if (not self.simplex(2)) or self.D[self.m + 1][self.n + 1] < -1e-6:
                return (inf, x) # No solution
            for i in range(self.m):
                if self.B[i] == -1:
                    s = 0
                    for j in range(1, self.n + 1):
                        s = self.minPivot(self.D[i], self.N, j, s)
                    self.pivot(i, s)
        ok = self.simplex(1)
        x = zeros(self.n)
        for i in range(self.m):
            if self.B[i] < self.n:
                x[self.B[i]] = self.D[i][self.n + 1]
        return (self.D[self.m][self.n + 1], x) if ok else (-inf, x)
