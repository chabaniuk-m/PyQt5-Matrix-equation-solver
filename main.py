import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QGroupBox, \
    QLineEdit, QPushButton, QRadioButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import uic

from Cramer import cramer
from Seidal import seidal
from SimpleIteration import simple_iteration


class Matrix(QMainWindow):
    # за замовчуванням обмежуємо розмірність матриці від 2 до 10
    __correct_dimensions: list[str] = [str(x) for x in range(2, 11)]
    CELL_SIZE: int = 50
    VERTICAL_SEPARATOR_SPACE: int = 20

    def __init__(self):
        super().__init__()
        self.line = None
        uic.loadUi('matrix.ui', self)
        self.cells: list[list[QLineEdit]] = []  # поля вводу елементів матриці
        self.free: list[QLineEdit] = []  # вектор вільних членів
        self.setFixedSize(self.width(), self.height())  # забороняємо розтягувати вікно
        self.n = 0  # розмірність матриці
        self.matrix: list[list[float]] = []  # матриця коефіцієнтів
        self.b: list[float] = []  # вектор вільних членів
        self.group: QGroupBox = self.gb
        self.frame: QFrame = self.matrix_container
        self.frame.setLayout(QVBoxLayout())
        self.solution: QLabel = self.sol  # поле для виводу результату
        self.solution.setAlignment(Qt.AlignCenter)
        self.input_n: QLineEdit = self.in_n  # поле для введення розмірності матриці
        self.input_n.setValidator(
            QtGui.QIntValidator(0, 1000))  # перевірка значення для розмірності матриці
        self.input_n_btn: QPushButton = self.in_n_btn
        self.epsilon_lbl: QLabel = self.eps_lbl
        self.input_epsilon: QLineEdit = self.in_eps  # поле для введення точності
        self.input_epsilon.setValidator(
            QtGui.QDoubleValidator(0, 1, 9,
                                   notation=QtGui.QDoubleValidator.StandardNotation))
        self.input_epsilon.setPlaceholderText("0.001")  # задаємо значення за замовчуванням для точності
        self.epsilon: float = 0.001
        self.epsilon_btn: QPushButton = self.eps_btn  # кнопка, яка змінює задану точність
        self.epsilon_btn.clicked.connect(self.set_epsilon)
        self.hide_epsilon()  # за замовчуванням не просимо ввести точність
        self.method = ""
        self.kramer: QRadioButton = self.kr
        self.simple_iteration: QRadioButton = self.si
        self.seidel: QRadioButton = self.sei
        self.kramer.toggled.connect(self.set_kramer)
        self.simple_iteration.toggled.connect(self.set_simple_iteration)
        self.seidel.toggled.connect(self.set_seidel)
        self.solve_btn: QPushButton = self.s_btn
        self.clear_btn: QPushButton = self.c_btn
        self.solve_btn.clicked.connect(self.solve)
        self.input_n_btn.clicked.connect(self.set_matrix_dimensions)
        self.clear_btn.clicked.connect(self.clear_matrix)

    def set_matrix_dimensions(self):
        if not self.is_correct_dimensions_input():
            self.solution.setText("Некоректна розмірність матриці. Дозволено від 2 до 10")
        else:
            self.solution.setText("")
            self.n = int(self.input_n.text().strip())
            self.display_matrix_cells()

    def display_matrix_cells(self):
        # прибрати попередні клітинки
        for line in self.cells:
            for c in line:
                self.layout().removeWidget(c)
        for c in self.free:
            self.layout().removeWidget(c)
        if self.line is not None:
            self.layout().removeWidget(self.line)

        # позиція для нових клітинок
        n = self.n
        x_0 = (self.frame.geometry().width() - Matrix.CELL_SIZE * (n + 1) - Matrix.VERTICAL_SEPARATOR_SPACE) // 2
        y_0 = (self.frame.geometry().height() - Matrix.CELL_SIZE * n) // 2
        x_0 += self.group.geometry().x() + 5
        y_0 += self.group.geometry().y() + 23

        def get_cell(_x: int, _y: int) -> QLineEdit:
            cell = QLineEdit()
            cell.setPlaceholderText("0")
            cell.setValidator(
                QtGui.QDoubleValidator(
                    notation=QtGui.QDoubleValidator.StandardNotation))
            cell.setFixedSize(Matrix.CELL_SIZE, Matrix.CELL_SIZE)
            self.layout().addWidget(cell)
            cell.setStyleSheet("font-size: 22px; qproperty-alignment: AlignCenter")
            cell.move(_x, _y)
            return cell

        # клітинки матриці
        self.cells = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            x = x_0 + i * Matrix.CELL_SIZE + Matrix.CELL_SIZE // 10
            for j in range(n):
                y = y_0 + j * Matrix.CELL_SIZE + Matrix.CELL_SIZE // 10
                self.cells[i][j] = get_cell(x, y)

        # вертикальна лінія
        x = x_0 + n * Matrix.CELL_SIZE + 15
        self.line = QFrame()
        self.line.setFixedSize(1, n * Matrix.CELL_SIZE)
        self.line.setStyleSheet("border: 1px solid darkgray")
        self.line.move(x, y_0 + Matrix.CELL_SIZE // 10)
        self.layout().addWidget(self.line)

        # вільні члени
        self.free = [None for _ in range(n)]
        x += 12
        for i in range(n):
            y = y_0 + i * Matrix.CELL_SIZE + Matrix.CELL_SIZE // 10
            self.free[i] = get_cell(x, y)

    def is_correct_dimensions_input(self):
        d = self.input_n.text().strip()
        return d in Matrix.__correct_dimensions

    def clear_matrix(self):
        for row in self.cells:
            for cell in row:
                cell.setText("0")
        for cell in self.free:
            cell.setText("0")

    def __set_epsilon_visible(self, visible: bool):
        self.epsilon_lbl.setVisible(visible)
        self.input_epsilon.setVisible(visible)
        self.epsilon_btn.setVisible(visible)

    def hide_epsilon(self):
        self.__set_epsilon_visible(False)
        self.input_epsilon.setText("")

    def show_epsilon(self):
        self.__set_epsilon_visible(True)
        self.epsilon = 1e-3

    def set_epsilon(self):
        self.epsilon = float(self.input_epsilon.text()) \
            if self.input_epsilon.text() != "" \
            else 1e-3
        print(f"epsilon is set to {self.epsilon}")

    def set_kramer(self):
        self.method = 'k'
        self.hide_epsilon()

    def set_simple_iteration(self):
        self.method = 'si'
        self.show_epsilon()

    def set_seidel(self):
        self.method = 's'
        self.show_epsilon()

    def init_system(self):
        self.matrix = [[0 if x.text() == "" else float(x.text()) for x in row] for row in self.cells]
        self.matrix = np.array(np.matrix(self.matrix).transpose())
        self.b = [0 if x.text() == "" else float(x.text()) for x in self.free]
        print(self.matrix)
        print(self.b)

    @staticmethod
    def _pretty_solution(x: list[float]) -> str:
        return ", ".join([f"x{i + 1}={int(x) if x % 1 == 0 else x}" for i, x in enumerate(x)])

    def solve(self):
        print("Trying to solve")
        print(f"{self.n=}")
        sol = ""
        if self.n == 0:
            sol = "Спершу задайте розмірність матриці"
        else:
            self.init_system()
            A = np.array(self.matrix)
            b = np.array(self.b)
            d = np.linalg.det(A)
            if d == 0:
                sol = "Неможливо розв'язати, оскільки визначник = 0"

            if self.kramer.isChecked():
                sol = Matrix._pretty_solution(cramer(A, b))
            elif self.simple_iteration.isChecked():
                x = simple_iteration(A, b, self.epsilon)
                sol = Matrix._pretty_solution(x) \
                    if x \
                    else "Матриця не відповідає умові діагональної переваги"
            elif self.seidel.isChecked():
                x = seidal(A, b, self.epsilon)
                sol = Matrix._pretty_solution(x) \
                    if x \
                    else "Матриця не відповідає умові діагональної переваги"
            else:
                sol = "Оберіть метод для розв'язку системи"

        print(f"solutions: {sol}")
        self.solution.setText(sol)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Matrix()
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing window...")
