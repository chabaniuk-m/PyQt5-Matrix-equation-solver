import numpy as np
import time as t

z = t.time()
c = []
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
x = [0. for i in range(m)]
count = 0
pogr = 0.

if not all(np.abs(A[i,i]) >= np.sum(np.abs(A[i,:])) - np.abs(A[i,i]) for i in range(m)):
    print("Матрица A не удовлетворяет условию диагонального преобладания!")
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
            # c.append(list((b[i] - s1 - s2) / A[i][i]))
        pogr = sum(abs(x_new[i] - x[i]) for i in range(m))
        if pogr <= 0.00001:
            break
        count += 1
        x = x_new

    print('Кількість ітерацій :', count + 1)
    print('Рішення системи рівнянь :', x)
    print('Погрішність :', pogr)
    print('Проізвідність коду :', t.time() - z, 'секунд')
    # print("---------------------------------")
    print('Проверка :', np.matmul(A, x))
