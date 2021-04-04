from numpy import zeros, inf

# Summary: Class to model LPs
# Remark: Adapted from https://github.com/kth-competitive-programming/kactl/blob/master/content/numerical/Simplex.h
class LPSolver():

    # Args: A, b, linear constrains: Ax <= b
    #       c, objective (to minimize)
    def __init__(A, b, c):
        assert len(A) == len(c)
        assert len(A[0]) == len(b)
        self.m = len(b)
        self.n = len(c)
        self.N = zeros((self.n + 1))
        self.B = zeros((self.m))
        self.D = A
        for i in range(self.m):
            B[i] = self.n + i
            D[i][self.n] = -1
            D[i][self.n + 1] = b[i]    
        for j in range(self.n):
            N[j] = j
        self.D[self.m] = c
        self.N[self.n] = -1
        self.D[self.m + 1][self.n] = 1

    def pivot(r, s):
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

    def lexLess(a1, a2, b1, b2):
        return a1 < b1 or (a1 == b1 and a2 < b2)

    def minPivot(Di, N, s):
        if s == -1 or lexLess(Di[j], N[j], Di[s], N[s]):
            s = j

    def simplex(phase):
        x = self.m + phase - 1
        while True:
            s = -1
            for j in range(self.n + 1):
                if self.N[j] != -phase:
                    minPivot(self.D[x], self.N, s)
            if self.D[x][s] >= -1e-6:
                return True
            r = -1
            for i in range(self.m):
                if self.D[i][s] <= 1e-6:
                    continue
                if r == -1 or lexLess(self.D[i][self.n+1] / self.D[i][s], self.B[i],
                                      self.D[r][self.n+1] / self.D[r][s], self.B[r]):
                    r = i
            if r == -1:
                return false
            pivot(r, s)

    # Return: optimal value
    # Post: set x to an optimal solution (with minimum objective)
    def solve(x):
        r = 0
        for i in range(1, self.m):
            if self.D[i][self.n + 1] < self.D[r][self.n + 1]:
                r = i
        if self.D[r][self.n + 1] < -1e-6:
            pivot(r, self.n)
            if (not simplex(2)) or self.D[self.m + 1][self.n + 1] < -1e-6:
                return inf # No solution
            for i in range(self.m):
                if B[i] == -1:
                    s = 0
                    for j in range(1, self.n + 1):
                        minPivot(sef.D[i], self.N, s)
                    pivot(i, s)
        ok = simplex(1)
        x = zeros(self.n)
        for i in range(self.m):
            if self.B[i] < self.n:
                x[self.B[i]] = self.D[i][self.n + 1]
        return self.D[self.m][self.n + 1] if ok else -inf
