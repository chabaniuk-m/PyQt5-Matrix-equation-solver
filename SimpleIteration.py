import math

import numpy as np


def simple_iteration(A: np.array, b: np.array, epsilon: float) -> list:
    m = len(A)
    b = np.array(np.matrix([b]).transpose())
    x = np.zeros((m, 1))  # початкове наближення
    count = 0
    B = np.zeros((m, m))
    c = np.zeros((m, 1))
    # перевіряємо умову діагональної переваги матриці А
    if not all(np.abs(A[i, i]) >= np.sum(np.abs(A[i, :])) - np.abs(A[i, i]) for i in range(m)):
        return []
    else:
        # Вычисляем матрицу B и вектор c
        for i in range(m):
            for j in range(m):
                if i != j:
                    B[i][j] = -A[i][j] / A[i][i]
            c[i] = b[i] / A[i][i]

        while True:
            x_new = np.matmul(B, x) + c
            if np.linalg.norm(x_new - x) <= epsilon:
                break
            count += 1
            x = x_new
        precision = round(math.log10(1 / epsilon))
        return [round(i[0], precision + 1) for i in x]


_A = np.array([[30, 1, 1, 9, 10],
               [8, -41, -1, 2, 3],
               [2, 3, -40, 4, 15],
               [7, 30, 1, -120, 3],
               [-10, 7, 20, 4, -50]])
_b = np.array([12, 13, 14, 11, 2])

if __name__ == "__main__":
    print(simple_iteration(_A, _b, 0.00001))

