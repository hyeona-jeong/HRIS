import os
import sys
import pymysql
import smtplib
import string
import random

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from email.message import EmailMessage

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('find.ui')
form_class = uic.loadUiType(form)[0]

class Find(QMainWindow, form_class):

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)

        self.fsubmitBtn.clicked.connect(self.findID)
        self.cert_btn.clicked.connect(self.find_cert_num)
        self.cert_btn.setCheckable(True)
        self.emp_num_lineEdit.returnPressed.connect(self.findID)
        self.emp_num_lineEdit.setValidator(QIntValidator(00000000,12000000,self))
        self.emp_num_lineEdit_2.setValidator(QIntValidator(00000000,12000000,self))

        self.tab.currentChanged.connect(self.useBtn)

        self.conn = pymysql.connect(
            host='localhost',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def useBtn(self):
        self.fsubmitBtn.setDisabled(False)

    def find_cert_num(self):
        self.name = self.name_lineEdit.text()
        self.emp_num = int(self.emp_num_lineEdit.text())

        query = 'select id, name_kor, mail from login_data,main_table where name_kor=%s and login_data.emp_num=%s and login_data.emp_num = main_table.emp_num;'
        self.cur.execute(query,(self.name,self.emp_num))
        result = self.cur.fetchone()
        if result is None:
            QMessageBox.warning(self, "Find Failed", "일치하는 이름, 사번 정보가 없습니다.")
            return
        
        else:
            self.id = result[0]
            mail = result[2]
            self.cert_num = ''
            string_pool = string.digits

            for i in range(6):
                self.cert_num += random.choice(string_pool)

            query = 'update login_data set cert_num=%s;'
            self.cur.execute(query,(self.cert_num))
            self.conn.commit()

            smtp = smtplib.SMTP('smtp.gmail.com',587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login('wjdgusk310@gmail.com','fmvs mwrf ydyp ifkw')

            msg = EmailMessage()
            msg['Subject'] = 'NoriSystem ID찾기 인증번호입니다.'
            msg.set_content('인증번호: ' + self.cert_num + '입니다.')

            msg['From']='wjdgusk310@gmail.com'
            msg['To']=mail
            smtp.send_message(msg)

            QMessageBox.information(self, "Find Succeed", "메일이 전송되었습니다.")
            self.cert_btn.setDisabled(True)

    def findID(self):
        if self.tab.currentIndex() == 0:
            if not self.cert_btn.isChecked():
                QMessageBox.warning(self, "Find Failed", "인증번호받기 버튼을 눌러주세요.")
                return
            
            else:
                query = 'select id, name_kor, mail from login_data,main_table where name_kor=%s and login_data.emp_num=%s and login_data.emp_num = main_table.emp_num and cert_num=%s;'
                self.cur.execute(query,(self.name,self.emp_num,self.cert_num))
                result = self.cur.fetchone()
                if result is None:
                    QMessageBox.warning(self, "Find Failed", "인증번호가 틀렸습니다.")
                    return
                else:
                    QMessageBox.information(self,"Notice","ID는 "+self.id+"입니다.")
                    
        else:
            self.id = self.id_lineEdit.text()
            self.name = self.name_lineEdit_2.text()
            self.emp_num = self.emp_num_lineEdit_2.text()

            if(len(self.id) == 0 or len(self.name) == 0 or len(self.emp_num) == 0 ):
                QMessageBox.warning(self, "Find Failed", "모든 정보를 입력해주세요.")
                return
            else:
                query = 'select id, name_kor, login_data.emp_num, mail from login_data,main_table where id = %s and name_kor = %s and login_data.emp_num = %s and login_data.emp_num = main_table.emp_num;'
                self.cur.execute(query,(self.id,self.name,self.emp_num))
                result = self.cur.fetchone()

                if result is None:
                    QMessageBox.warning(self, "Find Failed", "일치하는 ID, 이름, 사번정보가 없습니다.")
                    return
                
                else:
                    id = result[0]
                    mail = result[3]
                    newpasswd = ''
                    string_pool = string.ascii_letters + string.digits

                    for i in range(8):
                        newpasswd += random.choice(string_pool)

                    query = 'update login_data set passwd = %s;'
                    self.cur.execute(query,(newpasswd))
                    self.conn.commit()

                    smtp = smtplib.SMTP('smtp.gmail.com',587)
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login('wjdgusk310@gmail.com','fmvs mwrf ydyp ifkw')

                    msg = EmailMessage()
                    msg['Subject'] = 'NoriSystem Id/Passwd 정보입니다.'
                    msg.set_content('Id: ' +id+ '\nPasswd: ' + newpasswd + '입니다.')

                    msg['From']='wjdgusk310@gmail.com'
                    msg['To']=mail
                    smtp.send_message(msg)

                    QMessageBox.information(self, "Find Succeed", "메일이 전송되었습니다.")
                    self.fsubmitBtn.setDisabled(True)






if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Find() 
    myWindow.show() 
    app.exec_() 