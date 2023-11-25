import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from emp_regist import Regist

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('test.ui')
form_class = uic.loadUiType(form)[0]

class EmpInfo(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__()
        self.setupUi(self)

        menu = QMenu()
        menu.addAction('action',self.action)
        menu.addAction('Action2')

        self.tool.setMenu(menu)
        self.tool.setPopupMode(QToolButton.InstantPopup)
        


    def action(self):
        print('action bim')
         
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = EmpInfo( ) 
    myWindow.show( ) 
    app.exec_( ) 


