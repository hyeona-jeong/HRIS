import os
import sys
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from index import Index
# from sign_up import SignUp

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
        self.login.setLayout(self.loginLayout)
        
        self.userRegBtn.clicked.connect(self.showSign)
        
    
    # 231121 로그인 체크 by 정현아    
    def loginfunction(self):
        user = self.id.text()
        password = self.passwd.text()
        
        if len(user)==0 or len(password)==0:
            QMessageBox.warning(self, "Login Failed", "ID, 비밀번호 모두 입력하셔야 합니다.")

        else:
            conn = pymysql.connect(
                host='192.168.2.20',
                user='dev',
                password='nori1234',
                db='test',
                port=3306,
                charset='utf8'
            )
            cur = conn.cursor()
            query = 'SELECT password FROM login_data WHERE id =\''+user+"\'"
            cur.execute(query)
            result_pass = cur.fetchone()
            
            if result_pass is not None :
                if result_pass[0] == password:
                    self.w = Index()
                    self.w.show()
                    self.hide()
                    self.w.logoutBtn.clicked.connect(self.back)
                    self.w.closed.connect(self.show)
                else:
                    QMessageBox.warning(self, "Login Failed", "잘못된 패스워드입니다..")
                    self.passwd.clear()
            else:
                QMessageBox.warning(self, "Login Failed", "존재하지 않는 ID입니다..")
                
    def back(self):
        self.w.hide()
        self.show()
    
    # 231123 회원등록화면과 연결 by 정현아
    def showSign(self):
        self.w = SignUp()
        self.w.show()
        self.w.cnlBtn.clicked.connect(self.w.close)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Login() 
    myWindow.show() 
    app.exec_() 