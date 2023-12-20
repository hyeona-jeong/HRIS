import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sqlite3
from io import BytesIO

class ImageEditor(QMainWindow):
    def __init__(self):
        super(ImageEditor, self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image Editor')

        self.text_edit = QTextEdit(self)
        self.text_edit.setAcceptRichText(True)

        save_button = QPushButton('Save to Database', self)
        save_button.clicked.connect(self.saveToDatabase)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.createActions()
        self.createMenuBar()

    def createActions(self):
        self.insertImageAct = QAction('Insert Image', self, triggered=self.insertImage)

    def createMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(self.insertImageAct)

    def insertImage(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_paths, _ = file_dialog.getOpenFileNames(self, 'Select Image Files', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif)')

        for file_path in file_paths:
            image_label = QLabel(self)
            pixmap = QPixmap(file_path)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)

            cursor = self.text_edit.textCursor()
            cursor.insertBlock()
            cursor.insertHtml('<img src="data:image/png;base64,{}"/>'.format(self.imageToBase64(file_path)))
            cursor.insertBlock()

    def imageToBase64(self, image_path):
        with open(image_path, 'rb') as image_file:
            encoded_image = BytesIO(image_file.read())
            return encoded_image.read().encode('base64').decode()

    def saveToDatabase(self):
        db_connection = sqlite3.connect('images.db')
        cursor = db_connection.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, image_data BLOB)')

        html = self.text_edit.toHtml()
        cursor.execute('INSERT INTO images (image_data) VALUES (?)', (html,))

        db_connection.commit()
        db_connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec_())
