import os
import sys
import typing
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from index import Index

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('login.ui')
form_class = uic.loadUiType(form)[0]

class Login(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loginBtn.clicked.connect(self.loginfunction)
        self.passwd.returnPressed.connect(self.loginfunction)
        self.passwd.setEchoMode(QLineEdit.Password)

    # 231120 로그인 함수 (정현아) 
    def loginfunction(self):
        id = self.id.text()
        password = self.passwd.text()
        
        if len(id)==0 or len(password)==0:
            QMessageBox.warning(self, "Login Failed", "ID, 비밀번호 모두 입력하셔야 합니다.")

        #login_data에서 id,passwd가 일치하면 index페이지로 전환
        else:
            conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='test',
                port=3306,
                charset='utf8'
            )
            cur = conn.cursor()
            query = 'SELECT password FROM login_data WHERE id =\''+id+"\'"
            cur.execute(query)
            try:
                result_pass = cur.fetchone()[0]
                if result_pass == password:
                    self.showIndex()

                else:
                    QMessageBox.warning(self, "Login Failed", "잘못된 패스워드입니다.")
                    self.passwd.clear()
            except:
                QMessageBox.warning(self, "Login Failed", "존재하지 않는 ID입니다.")
                
    
    
    # 231122 페이지 전환 함수 by정현아
    def showIndex(self):
        self.w = Index()
        self.w.show()
        self.hide()
        self.w.logoutBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)

    def back(self):
        self.w.close()
        self.id.clear()
        self.passwd.clear()
        



if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Login() 
    myWindow.show() 
    app.exec_() 