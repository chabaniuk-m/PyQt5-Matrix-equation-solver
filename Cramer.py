import numpy as np


def __replace_column(A: np.array, j: int, b: np.array) -> np.array:
    matrix = A.copy()
    for i in range(len(matrix)):
        matrix[i, j] = b[i]
    return matrix


def cramer(A: np.array, b: np.array) -> list[float]:
    d = np.linalg.det(A)
    x = []
    for i in range(len(A)):
        M = __replace_column(A, i, b)
        print(M)
        print(f"#{i}: {np.linalg.det(M)} / {d}")
        x.append(round(np.linalg.det(M) / d, 3))
    return x


if __name__ == "__main__":
    _A = np.array([
        [2, 1, 4, 8],
        [1, 3, -6, 2],
        [3, -2, 2, -2],
        [2, -1, 2, 0],
    ])
    _b = np.array([-1, 3, 8, 4])

    # _A = np.array([
    #     [2, 5, 4],
    #     [1, 3, 2],
    #     [2, 10, 9]
    # ])
    # _b = np.array([30, 150, 110])
    print(cramer(_A, _b))
