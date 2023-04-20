import math

import numpy as np
from SimpleIteration import _A, _b


def seidal(A: np.array, b: np.array, epsilon: float) -> list:
    m = len(A)
    x = [0. for _ in range(m)]
    count = 0
    if not all(np.abs(A[i,i]) >= np.sum(np.abs(A[i,:])) - np.abs(A[i,i]) for i in range(m)):
        return []
    else:
        while True:
            x_new = np.copy(x)
            for i in range(m):
                s1 = 0
                for j in range(i):
                    s1 += A[i][j] * x_new[j]
                s2 = 0
                for j in range(i + 1, m):
                    s2 += A[i][j] * x[j]
                x_new[i] = (b[i] - s1 - s2) / A[i][i]
            if sum(abs(x_new[i] - x[i]) for i in range(m)) <= epsilon:
                break
            count += 1
            x = x_new
        precision = round(math.log10(1 / epsilon))
        return [round(i, precision) for i in x]


if __name__ == "__main__":
    print(seidal(_A, _b, 1e-5))