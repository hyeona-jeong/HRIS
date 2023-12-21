from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class HTMLLabelExample(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # QLabel을 사용하여 HTML 포맷의 텍스트 표시
        label = QLabel()
        html_text = """
        <html>
            <body>
                <h1>This is a heading</h1>
                <p>This is a paragraph with <b>bold</b> text.</p>
                <img src="path/to/your/image.png" alt="Image">
            </body>
        </html>
        """
        label.setText(html_text)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = HTMLLabelExample()
    window.show()
    sys.exit(app.exec_())