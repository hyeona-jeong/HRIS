from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QVBoxLayout, QWidget

class TableComboBoxExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.table.setColumnCount(2)
        self.table.setRowCount(3)

        for row in range(3):
            for col in range(2):
                combo_box = QComboBox(self)
                combo_box.addItem("Option 1")
                combo_box.addItem("Option 2")
                combo_box.addItem("Option 3")

                self.table.setCellWidget(row, col, combo_box)

        self.setWindowTitle("Table with ComboBox Example")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = TableComboBoxExample()
    window.show()
    sys.exit(app.exec_())