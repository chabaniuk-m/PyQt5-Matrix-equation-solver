import numpy as np
import time as t

z = t.time()
A = [[0, 1, 1, 90, 10],
     [8, 0, -1, 2, 3],
     [2, 3, 0, 4, 15],
     [7, 30, 1, 0, 3],
     [-10, 7, 20, 4, 0]]
b = [12, 13, 14, 11, 2]


def Kram(A1, B):
    m = len(A1)
    op = np.linalg.det(A1)
    r = list()
    if op == 0:
        print('определитель матрицы коэффициентов равен нулю, '
              'то система может иметь бесконечное количество решений'
              ' или не иметь решений вовсе.')
    else:
        for i in range(m):
            VM = np.copy(A1)
            VM[:, i] = B
            r.append(np.linalg.det(VM) / op)
        return r


X = Kram(A, b)
print('Рішення системи рівнянь :', X)
print('Проверка :', np.matmul(A, X))
print('Погрешность ответов :', np.array(np.matmul(A, X)) - np.array(b))
print('Проізвідність коду :', t.time() - z, 'секунд')
