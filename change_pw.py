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
        self.chgBtn.clicked.connect(self.changPw)
        self.oldpwlineEdit.returnPressed.connect(self.changPw)

    def changPw(self):
        oldPw = self.oldpwlineEdit.text()
        newPw = self.newpwlineEdit.text()
        newPw2 = self.newpwlineEdit_2.text()

        conn = pymysql.connect(
            host='localhost',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
        )
        cur = conn.cursor()
        query = ''

        if(len(oldPw) == 0 or len(newPw) == 0 or len(newPw2) == 0):
            QMessageBox.warning(self,"Password Change Failed","모든 항목을 입력해주셔야합니다.")
            return
        else:
            pass
         
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = ChangPw( ) 
    myWindow.show( ) 
    app.exec_( ) 


