import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QGroupBox, \
                            QLineEdit, QPushButton, QRadioButton, QVBoxLayout
from PyQt5 import uic


class Matrix(QMainWindow):
    # за замовчуванням обмежуємо розмірність матриці від 2 до 10
    __correct_dimensions: list[str] = [str(x) for x in range(2, 11)]
    CELL_SIZE: int = 50
    VERTICAL_SEPARATOR_SPACE: int = 20

    def __init__(self):
        super().__init__()
        self.line = None
        uic.loadUi('matrix.ui', self)
        self.cells: list[list[QLineEdit]] = []                 # поля вводу елементів матриці
        self.free: list[QLineEdit] = []                  # вектор вільних членів
        self.n = 0
        self.group: QGroupBox = self.gb
        self.frame: QFrame = self.matrix_container
        self.frame.setLayout(QVBoxLayout())
        self.solution: QLabel = self.sol
        self.input_n: QLineEdit = self.in_n
        self.input_n_btn: QPushButton = self.in_n_btn
        self.kramer: QRadioButton = self.kr
        self.simple_iteration: QRadioButton = self.si
        self.seidel: QRadioButton = self.sei
        self.calc_btn: QPushButton = self.c_btn
        self.clear_btn: QPushButton = self.cl_btn
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
            cell.setText("0")
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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Matrix()
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing window...")

