from math import *
import numpy as np
import time as t

z = t.time()
A = np.array([[30, 1, 1, 9, 10],
              [8, -41, -1, 2, 3],
              [2, 3, -40, 4, 15],
              [7, 30, 1, -120, 3],
              [-10, 7, 20, 4, -50]])
b = np.array([[12],
              [13],
              [14],
              [11],
              [2]])
m = len(A)
x = np.zeros((m, 1))  # начальное приближение
count = 0
pogr = 0.
B = np.zeros((m, m))
c = np.zeros((m, 1))

# Проверяем условие диагонального преобладания матрицы A
if not all(np.abs(A[i,i]) >= np.sum(np.abs(A[i,:])) - np.abs(A[i,i]) for i in range(m)):
    print("Матрица A не удовлетворяет условию диагонального преобладания!")
else:
    # Вычисляем матрицу B и вектор c
    for i in range(m):
        for j in range(m):
            if i != j:
                B[i][j] = -A[i][j] / A[i][i]
        c[i] = b[i] / A[i][i]

    while True:
        x_new = np.matmul(B, x) + c
        pogr = np.linalg.norm(x_new - x)  # вычисляем погрешность
        if pogr <= 0.00001:
            break
        count += 1
        x = x_new

    print('Кількість ітерацій :', count)
    print('Рішення системи рівнянь :', x)
    print('Погрішність :', pogr)
    print('Проізвідність коду :', t.time() - z, 'секунд')
    # print("---------------------------------")
    print('Проверка :', np.matmul(A, x))

