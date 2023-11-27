import os
import sys
import typing
import pymysql
import re

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from index import Index
from find import Find
from change_pw import ChangPw

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
        self.passwdlineEdit.returnPressed.connect(self.loginfunction)
        self.passwdlineEdit.setEchoMode(QLineEdit.Password)

        self.findBtn.clicked.connect(self.showFind)
        
        
        self.conn = pymysql.connect(
                host='192.168.2.20',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        self.cur = self.conn.cursor()

    # 231120 로그인 함수 (정현아) 
    def loginfunction(self):
        self.id = self.idlineEdit.text()
        password = self.passwdlineEdit.text()
        
        if len(self.id)==0 or len(password)==0:
            QMessageBox.warning(self, "Login Failed", "ID, 비밀번호 모두 입력하셔야 합니다.")

        #login_data에서 id,passwd가 일치하면 index페이지로 전환
        else:
            query = 'SELECT passwd,cert_num FROM login_data WHERE id = %s'
            self.cur.execute(query, self.id)
            result_pass = self.cur.fetchone()
            if result_pass is not None:
                if result_pass[0] == password:
                    self.showIndex()
                    # 231125 비밀번호 찾기로 생긴 인증번호값 초기화
                    if (result_pass[1] is None):
                        return
                    else:
                        query='update login_data set cert_num = Null;'
                        self.cur.execute(query)
                        self.conn.commit()
                        self.conn.close()
                else:
                    QMessageBox.warning(self, "Login Failed", "잘못된 패스워드입니다.")
                    self.passwdlineEdit.clear()
    
            else:
                QMessageBox.warning(self, "Login Failed", "존재하지 않는 ID입니다.")
    
    # 231122 페이지 전환 함수 by정현아
    def showIndex(self):
        self.w = Index()
        self.w.show()
        self.w.chpwBtn.clicked.connect(self.showChPw)
        self.hide()
        self.w.logoutBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)

    def back(self):
        self.w.close()
        self.idlineEdit.clear()
        self.passwdlineEdit.clear()
        
    def showFind(self):
        self.w = Find()
        self.w.show()
        self.w.cnlBtn.clicked.connect(self.w.close)
        self.w.cnlBtn_2.clicked.connect(self.w.close)
    
    # 231127 패스워드 변경 함수 by 정현아
    def showChPw(self):
        self.w2 = ChangPw()
        self.w2.show()
        self.w2.cnlBtn.clicked.connect(self.w.close)
        self.w2.chgBtn.clicked.connect(self.changPw)
        self.w2.oldpwlineEdit.returnPressed.connect(self.changPw)
        
    def changPw(self):
        oldPw = self.w2.oldpwlineEdit.text()
        newPw = self.w2.newpwlineEdit.text()
        newPw2 = self.w2.newpwlineEdit_2.text()
        
        cnt = 0
        for i in range(len(newPw)-1):
            if newPw[i]==newPw[i+1]:
                cnt += 1
        
        query = 'SELECT PASSWD FROM LOGIN_DATA WHERE PASSWD = %s;'
        self.cur.execute(query,oldPw)
        result = self.cur.fetchone()
        
        if(len(oldPw) == 0 or len(newPw) == 0 or len(newPw2) == 0):
            QMessageBox.warning(self,"Password Change Failed","모든 항목을 입력해주셔야합니다.")
            return
        elif result is None:
            QMessageBox.warning(self,"Password Change Failed","현재 패스워드가 틀립니다.")
            return
        elif newPw != newPw2:
            QMessageBox.warning(self,"Password Change Failed","패스워드 확인이 다릅니다.\n다시 확인바랍니다.")
            return
        elif oldPw == newPw:
            QMessageBox.warning(self,"Password Change Failed","패스워드가 변경되지 않았습니다.")
            return
        elif (len(newPw)<8):
            QMessageBox.warning(self,'Password Change Failed','패스워드는 최소 8자리입니다.')
            return
        elif (newPw.isalnum()):
            QMessageBox.warning(self,'Password Change Failed','패스워드는 영숫자로만 구성될 수 없습니다.')
            return          
        elif(cnt>2):
            QMessageBox.warning(self,'Password Change Failed','패스워드는 세번 연속 같은 문자를 사용하실 수 없습니다.')
            return  
        else:                
            num = re.findall(r'\d+', newPw)
            for i in range(len(num[0])-2):
                if (int(num[0][i]) - int(num[0][i+1]) == 1):
                    if (int(num[0][i+1]) - int(num[0][i+2]) == 1):
                        QMessageBox.warning(self,'Password Change Failed','패스워드는 연속된 숫자를 사용하실 수 없습니다.')
                        return
                elif (int(num[0][i]) - int(num[0][i+1]) == -1):
                    if (int(num[0][i+1]) - int(num[0][i+2]) == -1):
                        QMessageBox.warning(self,'Password Change Failed','패스워드는 연속된 숫자를 사용하실 수 없습니다.')
                        return     
                else:
                    query='UPDATE LOGIN_DATA SET PASSWD = %s WHERE ID = %s;'
                    self.cur.execute(query,(newPw,self.id))
                    self.conn.commit()
                    QMessageBox.information(self,'Password Change Succeed','패스워드가 변경되었습니다.')
                    self.w2.close()
            


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Login() 
    myWindow.show() 
    app.exec_() 