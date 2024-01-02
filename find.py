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

class Find(QDialog, form_class):

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)

        self.fsubmitBtn.clicked.connect(self.findID)
        self.fsubmitBtn_2.clicked.connect(self.findPW)
        self.cert_btn.clicked.connect(self.find_cert_num)
        self.cert_btn.setCheckable(True)
        self.emp_num_lineEdit.returnPressed.connect(self.findID)
        self.emp_num_lineEdit.setValidator(QIntValidator(00000000,12000000,self))
        self.emp_num_lineEdit_2.setValidator(QIntValidator(00000000,12000000,self))
        self.mail_lineEdit.returnPressed.connect(self.findID)
        self.emp_num_lineEdit_2.returnPressed.connect(self.findPW)

        self.tab.currentChanged.connect(self.useBtn)

        self.conn = pymysql.connect(
            host='192.168.2.20',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    # 231125 탭 변경시 버튼 활성화 by 정현아
    def useBtn(self):
        self.fsubmitBtn.setDisabled(False)
        self.fsubmitBtn_2.setDisabled(False)
        # self.name_lineEdit.clear()
        # self.emp_num_lineEdit.clear()
        # self.mail_lineEdit_3.clear()

    # 231125 ID찾기시 인증번호 발송 by 정현아
    def find_cert_num(self):
        self.name = self.name_lineEdit.text()
        self.emp_num = self.emp_num_lineEdit.text()
        if(len(self.name) == 0 or len(self.emp_num )== 0):
            QMessageBox.warning(self, "Find Failed", "이름과 사번을 입력해주세요.")
            return
        
        self.emp_num = int(self.emp_num_lineEdit.text())
        query = 'SELECT NAME_KOR FROM MAIN_TABLE WHERE NAME_KOR = %s'
        self.cur.execute(query,(self.name))
        result = self.cur.fetchone()
        if result is None:
            QMessageBox.warning(self, "Find Failed", "일치하는 이름({})이 없습니다.".format(self.name))
            return
        query = 'SELECT emp_num FROM LOGIN_DATA WHERE emp_num = %s'
        self.cur.execute(query,(self.emp_num))
        result = self.cur.fetchone()
        if result is None:
            QMessageBox.warning(self, "Find Failed", "일치하는 사번({})이 없습니다.".format(self.emp_num))
        
        else:
            # 로딩 중에 WaitCursor로 변경
            self.setLoadingCursor(True)
            query = 'SELECT id, name_kor, mail FROM login_data,main_table WHERE name_kor=%s AND login_data.emp_num=%s AND login_data.emp_num = main_table.emp_num;'
            self.cur.execute(query,(self.name,self.emp_num))
            result = self.cur.fetchone()
            self.id = result[0]
            mail = result[2]
            self.cert_num = ''
            string_pool = string.digits

            for i in range(6):
                self.cert_num += random.choice(string_pool)

            query = 'UPDATE login_data SET cert_num=%s;'
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

            # 로딩이 끝나면 기본 커서로 변경
            self.setLoadingCursor(False)  
            QMessageBox.information(self, "Find Succeed", "메일이 전송되었습니다.")
            self.cert_btn.setChecked(True)
            self.cert_btn.setDisabled(True)

    # 231125 ID/PASSWD찾기 탭0 id찾기, 탭1 passwd찾기 by 정현아
    def findID(self):
        if not self.cert_btn.isChecked():
            QMessageBox.warning(self, "Find Failed", "인증번호받기 버튼을 눌러주세요.")
            return
        
        else:
            self.cert_num = self.mail_lineEdit.text()
            query = 'SELECT id, name_kor, mail FROM login_data,main_table WHERE name_kor=%s AND login_data.emp_num=%s AND login_data.emp_num = main_table.emp_num AND cert_num=%s;'
            self.cur.execute(query,(self.name,self.emp_num,self.cert_num))
            result = self.cur.fetchone()
            if result is None:
                QMessageBox.warning(self, "Find Failed", "인증번호가 틀렸습니다.")
                return
            else:
                QMessageBox.information(self,"Notice","ID는 "+self.id+"입니다.")
                    
    def findPW(self):
        
        self.id = self.id_lineEdit.text()
        self.name = self.name_lineEdit_2.text()
        self.emp_num = self.emp_num_lineEdit_2.text()

        if(len(self.id) == 0 or len(self.name) == 0 or len(self.emp_num) == 0 ):
            QMessageBox.warning(self, "Find Failed", "모든 정보를 입력해주세요.")
            return
        
        query = 'SELECT id FROM LOGIN_DATA WHERE id = %s'
        self.cur.execute(query,(self.id))
        result = self.cur.fetchone()
        if result is None:
            QMessageBox.warning(self, "Find Failed", "일치하는 ID({})가 없습니다.".format(self.id))
            return
        
        query = 'SELECT NAME_KOR FROM MAIN_TABLE WHERE NAME_KOR = %s'
        self.cur.execute(query,(self.name))
        result = self.cur.fetchone()
        if result is None:
            QMessageBox.warning(self, "Find Failed", "일치하는 이름({})이 없습니다.".format(self.name))
            return
        
        query = 'SELECT emp_num FROM LOGIN_DATA WHERE emp_num = %s'
        self.cur.execute(query,(self.emp_num))
        result = self.cur.fetchone()
        if result is None:
            QMessageBox.warning(self, "Find Failed", "일치하는 사번({})이 없습니다.".format(self.emp_num))
            return
        else:
            self.setLoadingCursor(True)
            query = 'SELECT id, name_kor, login_data.emp_num, mail FROM login_data,main_table WHERE id = %s AND name_kor = %s AND login_data.emp_num = %s AND login_data.emp_num = main_table.emp_num;'
            self.cur.execute(query,(self.id,self.name,self.emp_num))
            result = self.cur.fetchone()
            id = result[0]
            mail = result[3]
            newpasswd = ''
            string_pool = string.ascii_letters + string.digits

            # 231125 영대소문자숫자 8글자로 이루어진 임시비밀번호생성
            for i in range(8):
                newpasswd += random.choice(string_pool)

            query = 'UPDATE login_data SET passwd = %s;'
            self.cur.execute(query,(newpasswd))
            self.conn.commit()
            
            # 231125 등록된 메일로 임시 비밀번호 전송
            smtp = smtplib.SMTP('smtp.gmail.com',587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login('wjdgusk310@gmail.com','fmvs mwrf ydyp ifkw')

            msg = EmailMessage()
            msg['Subject'] = 'NoriSystem 새로운 비밀번호입니다.'
            msg.set_content('비밀번호: ' + newpasswd + '입니다.')

            msg['From']='wjdgusk310@gmail.com'
            msg['To']=mail
            smtp.send_message(msg)
            
            # 231128 메일 *처리 by 정현아
            mlen = mail.find('@')
            mail = list(mail)
            mlen = mlen/2
            if(mlen>=4):
                for i in range(int(mlen-2),int(mlen+2)):
                    mail[i] ='*'
                mail = ''.join(mail)
            else:
                for i in range(mlen):
                    mail[i] ='*'
                mail = ''.join(mail)
            
            # 로딩이 끝나면 기본 커서로 변경
            self.setLoadingCursor(False)    
            QMessageBox.information(self, "Find Succeed", "{}로 메일이 전송되었습니다.".format(mail))
            self.fsubmitBtn_2.setDisabled(True)        
    
    # 로딩시 커서 변경
    def setLoadingCursor(self, loading):
        if loading:
            QApplication.setOverrideCursor(Qt.WaitCursor)
        else:
            QApplication.restoreOverrideCursor()

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Find() 
    myWindow.show() 
    app.exec_() 