from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie

class AnimatedCursorWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.movie = QMovie('C:\\Users\\정현아\\.ssh\\HRIS\\cursor.gif')
        self.setMovie(self.movie)

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.animated_cursor_widget = AnimatedCursorWidget(self)
        layout.addWidget(self.animated_cursor_widget)

        button = QPushButton('Click me to show animated cursor', self)
        button.clicked.connect(self.show_animated_cursor)
        layout.addWidget(button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.stop_animated_cursor)

    def show_animated_cursor(self):
        self.animated_cursor_widget.start_animation()
        self.timer.start(5000)  # 5000 milliseconds = 5 seconds

    def stop_animated_cursor(self):
        self.timer.stop()
        self.animated_cursor_widget.stop_animation()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())