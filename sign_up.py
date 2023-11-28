import os
import sys
import pymysql
import re

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('sign_up.ui')
form_class = uic.loadUiType(form)[0]

class SignUp(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.signup.setLayout(self.signlayout)

        self.name_lineEdit.setFocus()
        # 231123사번을 12000000~올해년도*1000000까지 입력제한 by 정현아
        year = ((datetime.today().year-2000)+1)*1000000
        self.emp_num_lineEdit.setValidator(QIntValidator(12000000,year,self))

        self.ps_lineEdit.setEchoMode(QLineEdit.Password)
        self.ps2_lineEdit.setEchoMode(QLineEdit.Password)

        self.conn = pymysql.connect(
            host='192.168.2.20',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
        )
        self.cur = self.conn.cursor()

        self.id_lineEdit.editingFinished.connect(self.inputId)

        self.chkBtn.setCheckable(True)
        self.chkBtn.clicked.connect(self.chkId)
        self.submitBtn.clicked.connect(self.userSignUp)
    
    # 231123 회원가입시 입력정보 확인 by 정현아    
    def userSignUp(self):
        self.id = self.id_lineEdit.text()
        self.name = self.name_lineEdit.text()
        self.passwd = self.ps_lineEdit.text()
        self.passwd2 = self.ps2_lineEdit.text()
        self.emp_num = self.emp_num_lineEdit.text()

        if(len(self.name) == 0 or len(self.id) == 0 or len(self.passwd) == 0 or len(self.passwd2) == 0 or len(self.emp_num) == 0 ):
            QMessageBox.warning(self,'Sign up Failed','모든 항목을 입력하셔야 합니다.')
            return
        elif(not self.chkBtn.isChecked()):
            QMessageBox.warning(self,'Sign up Failed','ID중복 확인 바랍니다.')
        else:
            if (len(self.name)<2):
                QMessageBox.warning(self,'Sign up Failed','이름은 최소 두 글자입니다.')
                return
            elif (len(self.name)>4):
                QMessageBox.warning(self,'Sign up Failed','이름은 최대 네 글자입니다.')
                return
            elif (re.sub(r"[가-힣]","",self.name) != ''):
                QMessageBox.warning(self,'Sign up Failed','이름은 영문자, 자음, 모음이 입력될 수 없습니다. ')
                return
            else:
                if self.id[0].isdecimal() :
                    QMessageBox.warning(self,'Sign up Failed','ID 첫 글자는 숫자를 입력할 수 없습니다.')
                    return
                elif(not self.id.isalnum()):
                    QMessageBox.warning(self,'Sign up Failed','ID는 영문자와 숫자만 사용하셔야 합니다.')
                    return
                else:
                    if (len(self.passwd)<8):
                        QMessageBox.warning(self,'Sign up Failed','패스워드는 최소 8자리입니다.')
                        return
                    elif (self.passwd.isalnum()):
                        QMessageBox.warning(self,'Sign up Failed','패스워드는 영숫자로만 구성될 수 없습니다.')
                        return  
                    
                    else:
                        cnt = 0
                        for i in range(len(self.passwd)-1):
                            if self.passwd[i]==self.passwd[i+1]:
                                cnt += 1
                        if(cnt>2):
                            QMessageBox.warning(self,'Sign up Failed','패스워드는 세번 연속 같은 문자를 사용하실 수 없습니다.')
                            return                  

                        num = re.findall(r'\d+', self.passwd)
                        for i in range(len(num[0])-2):
                            if (int(num[0][i]) - int(num[0][i+1]) == 1):
                                if (int(num[0][i+1]) - int(num[0][i+2]) == 1):
                                    QMessageBox.warning(self,'Sign up Failed','패스워드는 연속된 숫자를 사용하실 수 없습니다.')
                                    return
                            elif (int(num[0][i]) - int(num[0][i+1]) == -1):
                                if (int(num[0][i+1]) - int(num[0][i+2]) == -1):
                                    QMessageBox.warning(self,'Sign up Failed','패스워드는 연속된 숫자를 사용하실 수 없습니다.')
                                    return
                            else:
                                if(self.passwd != self.passwd2):
                                    QMessageBox.warning(self,'Sign up Failed','패스워드가 일치하지 않습니다.')
                                    return             
                                else:                  
                                    query = 'select emp_num from main_table where emp_num =\'' + self.emp_num + '\';'
                                    self.cur.execute(query)
                                    emptyYN = self.cur.fetchone()

                                    if emptyYN is None:
                                        QMessageBox.warning(self,'Sign up Failed','등록되지 않은 사번입니다.\n관리자에게 문의바랍니다.')
                                        return
                                    else: 
                                        query ='select id from login_data where emp_num = ' + self.emp_num +';'
                                        self.cur.execute(query)
                                        emptyYN = self.cur.fetchone()
                                        if emptyYN is not None:
                                            QMessageBox.warning(self,'Sign up Failed','사원님의 ID가 이미 존재합니다.')
                                            return
                                        
                                        # 231123 모든 체크 완료시 DB에 Insert. 권한 문제로 미완성 by 정현아
                                        else:
                                            query ='insert into login_data values(%s,%s,%s,%s);'
                                            self.cur.execute(query, (self.id,self.passwd,self.emp_num,'user'))
                                            # self.conn.commit()
                                            self.conn.close()
                                            QMessageBox.information(self,'Sign up Succeed','등록완료되었습니다.')


    def inputId(self) :
        self.id = self.id_lineEdit.text()
        
    # 231123 ID중복체크 by 정현아
    def chkId(self):
        try:
            query = 'select id from login_data where id = \'' + self.id + '\';'
            self.cur.execute(query)
            emptyYN = self.cur.fetchone()
            if emptyYN is not None:
                QMessageBox.warning(self,'Id Check Failed','이미 존재하는 ID입니다.\n다른 ID를 사용하시기 바랍니다.')
                self.chkBtn.setChecked(False)
                return
            else: 
                QMessageBox.information(self,'Id Check Succeed','사용가능한 ID입니다.')
                self.chkBtn.setChecked(True)
        except:
            QMessageBox.warning(self,'Id Check Failed','ID를 입력하세요')

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = SignUp() 
    myWindow.show() 
    app.exec_() 