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
        self.emp_num_lineEdit.returnPressed.connect(self.findID)
        self.emp_num_lineEdit.setValidator(QIntValidator(00000000,12000000,self))


    def findID(self):
        self.name = self.name_lineEdit.text()
        self.emp_num = int(self.emp_num_lineEdit.text())
        conn = pymysql.connect(
            host='localhost',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
            )
        cur = conn.cursor()
        
        query = 'select id, name, mail from login_data,main_table where name=%s login_data.emp_num=%s and login_data.emp_num = main_table.emp_num;'
        cur.execute(query,(self.name,self.emp_num))
        result = cur.fetchone()
        if result is None:
            QMessageBox.warning(self, "Find Failed", "이름, 사번이 일치하는 정보가 없습니다.")
            return
        else:
            id = result[0]
            mail = result[2]
            newpasswd = ''
            string_pool = string.ascii_letters + string.digits

            for i in range(8):
                newpasswd += random.choice(string_pool)

            query = 'update login_data set passwd=%s;'
            cur.execute(query,(newpasswd))
            conn.commit()
            conn.close
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