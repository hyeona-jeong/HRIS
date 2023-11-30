import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from tkinter import filedialog
from tkinter import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('add_img.ui')
form_class = uic.loadUiType(form)[0]


class AddImg(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)

    # 231128 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by김태균
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)
         
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = AddImg( ) 
    myWindow.show( ) 
    app.exec_( ) 


