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
        
        self.searchbutton.clicked.connect(self.open_image)
        self.savebtn.clicked.connect(self.saveimg)
    
    #찾아보기로 이미지파일 팝업 열기 11.24 by김태균
    def open_image(self):
        file_path = QFileDialog.getOpenFileName(self, '이미지 찾기', './')
        print(file_path)

    def saveimg(self):
        self.w ()

         
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = AddImg( ) 
    myWindow.show( ) 
    app.exec_( ) 


