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
        self.emp_num = None
        self.result_pass = None
        self.img = None
        
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
            return
        #login_data에서 id,passwd가 일치하면 index페이지로 전환
        else:
            query = 'SELECT PASSWD,CERT_NUM,AUTHORITY FROM LOGIN_DATA WHERE ID = %s'
            try:
                self.cur.execute(query, self.id)
                self.result_pass = self.cur.fetchone()
                if self.result_pass is not None:
                    if self.result_pass[0] == password:
                        self.showIndex()
                        # 231125 비밀번호 찾기로 생긴 인증번호값 초기화
                        if (self.result_pass[1] is None):
                            return
                        else:
                            query='update login_data set cert_num = Null;'
                            self.cur.execute(query)
                            self.conn.commit()
                            self.conn.close()
                    else:
                        QMessageBox.warning(self, "Login Failed", "잘못된 패스워드입니다.")
                        self.passwdlineEdit.clear()
                        return
        
                else:
                    QMessageBox.warning(self, "Login Failed", "존재하지 않는 ID입니다.")
            except Exception as e:
                QMessageBox.warning(self, "로그인실패", "Error: " + str(e))
                return
    
    # 231122 인덱스 페이지 by정현아
    def showIndex(self):
        self.w = Index()
        self.w.show()
        # self.w.chgBtn.clicked.connect(self.showChPw)
        regist_action = None
        for action in self.w.menuHr.actions():
            if action.text() == '사원정보등록':
                regist_action = action
                break
        if self.result_pass[2] == 'regular' :
            regist_action.setVisible(False)
            self.w.showedList.connect(self.controlEmpListBtn)
            
        self.w.showedInfo.connect(self.showMyInfo)
        self.w.showedEdit.connect(self.showEdit)
        
        # 231128 인덱스 페이지에 DB를 가져와 사원 사진 출력 by 정현아
        query = 'SELECT ID, PIC, MAIN_TABLE.EMP_NUM FROM LOGIN_DATA, MAIN_TABLE WHERE LOGIN_DATA.EMP_NUM = MAIN_TABLE.EMP_NUM AND ID = %s'
        self.cur.execute(query,(self.id))
        result = self.cur.fetchone()
        self.emp_num = result[2]
        data = result[1]
        self.img = QPixmap()
        self.img.loadFromData(data, 'PNG')
        icon = QIcon(self.img)        
        self.w.chgBtn.setIcon(icon)
        
        # 231128 사원 증명사진 버튼에 패스워드 변경 메뉴 추가 by 정현아
        chmenu = QMenu()
        chmenu.setStyleSheet(stylesheet)
        chmenu.addAction('패스워드 변경',self.showChPw)
        self.w.chgBtn.setMenu(chmenu)
        
        self.hide()
        self.w.logoutBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)
        
    # 231201 사원권한이 regular일 경우 리스트의 등록,삭제 버튼이 안보이게 하기 by 정현아
    def controlEmpListBtn(self):
        self.w.w.listRegBtn.setVisible(False)
        self.w.w.listDelBtn.setVisible(False)
    
    # 231201 개인정보조회/편집 화면 데이터 바인딩    
    def showMyInfo(self):
        query = """
        SELECT 
        NAME_KOR, EMP_NUM, EMP_RANK, POSITION, PHONE, MAIL, CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_ENG, ADDRESS, WORK_POS, SALARY, DATE_JOIN, IFNULL(HEIGHT,''), IFNULL(WEIGHT,''), MILITARY, MARRY, LAST_EDU,ADDRESS_NUM 
        FROM MAIN_TABLE 
        WHERE EMP_NUM = %s; 
        """
        self.cur.execute(query,(self.emp_num))
        result = self.cur.fetchone()
        
        self.w.w.namekor.setText(result[0])
        self.w.w.empnum.setText(str(result[1]))
        self.w.w.emprank.setText(result[2])
        self.w.w.position.setText(result[3])
        self.w.w.phone.setText(result[4])
        self.w.w.mail.setText(result[5])
        self.w.w.dept.setText(result[6])
        self.w.w.nameeng.setText(result[7])
        self.w.w.address.setText(result[8])
        self.w.w.work_pos.setText(result[9])
        self.w.w.sal.setText(result[10])
        self.w.w.joindate.setText(str(result[11]))
        self.w.w.height.setText(str(result[12]))
        self.w.w.weight.setText(str(result[13]))
        self.w.w.militay.setText(result[14])
        self.w.w.marry.setText(result[15])
        self.w.w.lastedu.setText(result[16])
        self.w.w.addressnum.setText(str(result[17]))
        
        resize_pixmap = self.img.scaled(130,150)
        self.w.w.pic.setPixmap(resize_pixmap) 
        
        
    # 231201 개인정보수정화면 by 정현아 
    def showEdit(self):
        self.w.w.w.regnum_lineEdit.setEchoMode(QLineEdit.Password)
        query = """
        SELECT 
        NAME_KOR, NAME_ENG, EMP_NUM, DATE_JOIN, EMP_RANK, REG_NUM, MAIL, PHONE, CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, WORK_POS, 
        POSITION, ADDRESS_NUM,ADDRESS, SALARY, IFNULL(HEIGHT,''), IFNULL(WEIGHT,''), IFNULL(MILITARY,''), IFNULL(MARRY,''), LAST_EDU 
        FROM MAIN_TABLE 
        WHERE EMP_NUM = %s; 
        """
        self.cur.execute(query,(self.emp_num))
        result = self.cur.fetchone()
        self.w.w.w.namekor.setText(result[0])
        self.w.w.w.nameeng.setText(result[1])
        self.w.w.w.empnum.setText(str(result[2]))
        self.w.w.w.joindate.setText(str(result[3]))
        self.w.w.w.emprank.setText(result[4])
        self.w.w.w.regnum_lineEdit.setText(result[5])
        self.w.w.w.mail_lineEdit.setText(result[6])
        self.w.w.w.phone_lineEdit.setText(result[7])
        self.w.w.w.dept.setText(result[8])
        self.w.w.w.work_pos.setText(result[9])
        self.w.w.w.position.setText(result[10])
        self.w.w.w.addressnum_lineEdit.setText(str(result[11]))
        self.w.w.w.address_lineEdit.setText(result[12])
        self.w.w.w.salary.setText(result[13])
        self.w.w.w.weight_lineEdit.setText(str(result[14]))
        self.w.w.w.height_lineEdit.setText(str(result[15]))
        mil = result[16]
        if mil == '군필':
            self.w.w.w.milBtn.setChecked(True)
        elif mil == '미필':
            self.w.w.w.milBtn2.setChecked(True)
        else:
            self.w.w.w.milBtn3.setChecked(True)
        
        marry = result[17]
        if marry == '미혼':
            self.w.w.w.maryyBtn2.setChecked(True)
        else : 
            self.w.w.w.maryyBtn.setChecked(True)
        
        if result[17] == '고졸':
            self.w.w.w.lastedu_combo.setCurrentIndex(0)
        elif result[17] == '초대졸':
            self.w.w.w.lastedu_combo.setCurrentIndex(1)
        elif result[17] == '대졸':
            self.w.w.w.lastedu_combo.setCurrentIndex(2)
        elif result[17] == '대학원석사':
            self.w.w.w.lastedu_combo.setCurrentIndex(3)
        else:
            self.w.w.w.lastedu_combo.setCurrentIndex(4)
            
        resize_pixmap = self.img.scaled(130,150)
        self.w.w.w.pic.setPixmap(resize_pixmap) 
        
        
    def back(self):
        self.w.close()
        self.idlineEdit.clear()
        self.passwdlineEdit.clear()
        
    def showFind(self):
        self.w = Find()
        self.w.show()
        self.w.cnlBtn.clicked.connect(self.w.close)
        self.w.cnlBtn_2.clicked.connect(self.w.close)
    
    # 231127 패스워드 변경 페이지 호출 by 정현아
    def showChPw(self):
        self.w2 = ChangPw()
        self.w2.show()
        self.w2.cnlBtn.clicked.connect(self.w2.close)
        self.w2.chgBtn.clicked.connect(self.changPw)
        self.w2.oldpwlineEdit.returnPressed.connect(self.changPw)
        
    # 231127 패스워드 변경 함수 by 정현아
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
            query='UPDATE LOGIN_DATA SET PASSWD = %s WHERE ID = %s;'
            self.cur.execute(query,(newPw,self.id))
            self.conn.commit()
            QMessageBox.information(self,'Password Change Succeed','패스워드가 변경되었습니다.')
            self.w2.close()
            
stylesheet = """
    QMenu{
        background-color: white;
        color: black;
        font-family: Malgun Gothic;
    }
    QMenu::item:selected{
        background-color: #c6c6c6; 
    }
"""
            


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Login() 
    myWindow.show() 
    app.exec_() 