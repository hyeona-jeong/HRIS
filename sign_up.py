import os
import sys
import pymysql
import re
import random
import string
import smtplib

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from email.message import EmailMessage


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('sign_up.ui')
form_class = uic.loadUiType(form)[0]

class SignUp(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)        
        self.id = ''

        self.name_lineEdit.setFocus()
        self.emp_num_lineEdit.setValidator(QIntValidator())
        self.name_lineEdit.setMaxLength(5)
        self.emp_num_lineEdit.setMaxLength(8)
        self.id_lineEdit.setMaxLength(20)
        self.authCombo.setCurrentIndex(1)

        self.conn = pymysql.connect(
            host='localhost',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
        )
        self.cur = self.conn.cursor()

        # self.id_lineEdit.editingFinished.connect(self.inputId)
        self.chkBtn.setCheckable(True)
        self.chkBtn.clicked.connect(self.chkId)
        self.submitBtn.clicked.connect(self.userSignUp)
    
    # 231123 회원가입시 입력정보 확인 by 정현아    
    def userSignUp(self):
        name = self.name_lineEdit.text()
        auth = self.authCombo.currentText()
        emp_num = self.emp_num_lineEdit.text()
        passwd = ''
        string_pool = string.ascii_letters + string.digits

        for i in range(8):
            passwd += random.choice(string_pool)

        if(len(name) == 0 or len(self.id) == 0 or len(self.emp_num_lineEdit.text()) == 0 ):
            QMessageBox.warning(self,'Sign up Failed','모든 항목을 입력하셔야 합니다.')
            return
        elif(not self.chkBtn.isChecked()):
            QMessageBox.warning(self,'Sign up Failed','ID중복 확인 바랍니다.')
            return
        else:
            if (re.sub(r"[가-힣]","",name) != ''):
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
                    query = 'SELECT EMP_NUM FROM MAIN_TABLE WHERE EMP_NUM =' + emp_num + ';'
                    self.cur.execute(query)
                    emptyYN = self.cur.fetchone()

                    if not emptyYN:
                        QMessageBox.warning(self,'Sign up Failed','등록되지 않은 사번입니다.')
                        return
                    else: 
                        query = 'SELECT EMP_NUM, MAIL FROM MAIN_TABLE WHERE NAME_KOR = %s AND EMP_NUM = %s'
                        self.cur.execute(query,(name,int(emp_num)))
                        sinkYN = self.cur.fetchone()
                        if not sinkYN:
                            QMessageBox.warning(self,'Sign up Failed','사원정보가 일치하지 않습니다.\n이름, 사번 확인바랍니다.')
                            return
                        else:
                            mail = sinkYN[1]
                            query ='SELECT ID FROM LOGIN_DATA WHERE EMP_NUM = ' + emp_num +';'
                            print(emp_num)
                            self.cur.execute(query)
                            emptyYN = self.cur.fetchone()
                            if emptyYN:
                                QMessageBox.warning(self,'Sign up Failed','사원님의 ID가 이미 존재합니다.')
                                return
                            
                            # 231123 모든 체크 완료시 DB에 Insert. 
                            else:
                                try:
                                    query ='INSERT INTO LOGIN_DATA(ID,PASSWD,EMP_NUM,AUTHORITY) VALUES(%s,%s,%s,%s);'
                                    self.cur.execute(query, (self.id, passwd, int(emp_num), auth))
                                    self.conn.commit()
                                    QMessageBox.information(self,'Sign up Succeed','등록완료되었습니다.')
                                except Exception as e:
                                    QMessageBox.warning(self, 'Id Check Failed',str(e))
                                    print(str(e))
                                    return
                                
                                self.initSignUp()  
                                # 231206 등록된 메일로 ID, 임시 비밀번호 전송
                                # smtp = smtplib.SMTP('smtp.gmail.com',587)
                                # smtp.ehlo()
                                # smtp.starttls()
                                # smtp.login('wjdgusk310@gmail.com','fmvs mwrf ydyp ifkw')

                                # msg = EmailMessage()
                                # msg['Subject'] = 'NoriSystem ID, 비밀번호입니다.'
                                # msg.set_content('ID: ' + self.id +'\n비밀번호: ' + passwd + '입니다.')

                                # msg['From']='wjdgusk310@gmail.com'
                                # msg['To']=mail
                                # smtp.send_message(msg)        
                                     
                                                 
        
    # 231123 ID중복체크 by 정현아
    def chkId(self):
        self.id = self.id_lineEdit.text()
        try:
            if self.id =='':
                QMessageBox.warning(self,'Id Check Failed','ID를 입력해주세요.')
                self.chkBtn.setChecked(False)
                return
            else:
                query = 'SELECT ID FROM LOGIN_DATA WHERE ID = \'' + self.id + '\';'
                self.cur.execute(query)
                emptyYN = self.cur.fetchone()
                if emptyYN :
                    QMessageBox.warning(self,'Id Check Failed','이미 존재하는 ID입니다.\n다른 ID를 사용하시기 바랍니다.')
                    self.chkBtn.setChecked(False)
                    return
                else: 
                    QMessageBox.information(self,'Id Check Succeed','사용가능한 ID입니다.')
                    self.chkBtn.setChecked(True)
        except Exception as e:
            QMessageBox.warning(self,'Id Check Failed',str(e))
            print(str(e))

    def initSignUp(self):
        self.name_lineEdit.clear()
        self.emp_num_lineEdit.clear()
        self.id_lineEdit.clear()
        self.authCombo.setCurrentIndex(1)
        self.name_lineEdit.setFocus()
        self.chkBtn.setChecked(False)
        
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = SignUp() 
    myWindow.show() 
    app.exec_() 