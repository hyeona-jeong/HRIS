import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('change_pw.ui')
form_class = uic.loadUiType(form)[0]

class ChangPw(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.chgpw.setLayout(self.chLayout)
         
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = ChangPw( ) 
    myWindow.show( ) 
    app.exec_( ) 


