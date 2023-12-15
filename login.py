import os
import sys
import pymysql
import re

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from index import Index
from find import Find
from edit_tap import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('login.ui')
form_class = uic.loadUiType(form)[0]

class Login(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.result =None
        self.emp_num = None
        self.result_pass = None
        self.img = None
        self.pixmap = None
        self.TSP = ['생산실행IT G','생산스케쥴IT G','생산품질IT G','TSP운영 1G','TSP운영 2G','TSP고객총괄','']
        self.FAB = ['빅데이터 G','인프라 G','스마트팩토리 G','']
        self.MIS = ['전기운영 G','PLM G','']
        self.TC = ['TC/TPSS개발파트','화성 TC2.5','SAS TC2.5','']
        self.SP = ['사업기획팀','기술전략팀','']
        self.BS = ['경영지원','']
        
        self.setupUi(self)
        self.setWindowTitle("        ")
        self.setStyleSheet(stylesheet)
        self.loginBtn.clicked.connect(self.loginfunction)
        self.passwdlineEdit.returnPressed.connect(self.loginfunction)
        self.passwdlineEdit.setEchoMode(QLineEdit.Password)

        self.findBtn.clicked.connect(self.showFind)
        
        self.conn = pymysql.connect(
                host='localhost',
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
        regist_action = None

        # 231202 권한제어 권한이 레귤러이면 사원정보등록화면 및 리스트 화면에서 삭제 버튼 비활성화 by 정현아
        for action in self.w.menuHr.actions():
            if action.text() == '사원정보등록' or action.text() == '사원ID등록' or action.text() == '사용자권한관리':
                regist_action = action
                if self.result_pass[2] == 'Regular' :
                    regist_action.setVisible(False)
                
        if self.result_pass[2] == 'Regular' :
            self.w.showedList.connect(self.controlEmpListBtn)
            self.w.listToInfo.connect(self.controlEmpListBtn)

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
        
    # 231201 사원권한이 regular일 경우 리스트의 등록,삭제 버튼, 체크박스가 안보이게 하기 by 정현아
    def controlEmpListBtn(self):
        self.w.w.listRegBtn.setVisible(False)
        self.w.w.listDelBtn.setVisible(False)
        self.w.w.table.setColumnHidden(0,True)
        if self.w.w.w is not None:
            self.w.w.w.listChgbtn.setVisible(False)

    # 231201 개인정보조회/편집 화면 데이터 바인딩    
    def showMyInfo(self):
        # 231212 탭 초기화 by 정현아
        while self.w.w.tabWidget.count() > 1:
            self.w.w.tabWidget.removeTab(1)
            
        query = """
        SELECT 
        NAME_KOR, EMP_NUM, EMP_RANK, POSITION, PHONE, MAIL, CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_ENG, 
        ADDRESS, WORK_POS, SALARY, DATE_JOIN, IFNULL(HEIGHT,''), IFNULL(WEIGHT,''), MILITARY, MARRY, LAST_EDU,ADDRESS_NUM, PIC 
        FROM MAIN_TABLE 
        WHERE EMP_NUM = %s; 
        """
        # 나중에 self.result 굳이 self.안써도 되는지 확인
        self.cur.execute(query,(self.emp_num))
        self.result = self.cur.fetchone()
        
        self.w.w.namekor.setText(self.result[0])
        self.w.w.empnum.setText(str(self.result[1]))
        self.w.w.emprank.setText(self.result[2])
        self.w.w.position.setText(self.result[3])
        self.w.w.phone.setText(self.result[4])
        self.w.w.mail.setText(self.result[5])
        self.w.w.dept.setText(self.result[6])
        self.w.w.nameeng.setText(self.result[7])
        self.w.w.address.setText(self.result[8])
        self.w.w.work_pos.setText(self.result[9])
        self.w.w.sal.setText(self.result[10])
        self.w.w.joindate.setText(str(self.result[11]))
        self.w.w.height.setText(str(self.result[12]))
        self.w.w.weight.setText(str(self.result[13]))
        self.w.w.militay.setText(self.result[14])
        self.w.w.marry.setText(self.result[15])
        self.w.w.lastedu.setText(self.result[16])
        self.w.w.addressnum.setText(str(self.result[17]))

        data = self.result[18]
        img = QPixmap()
        img.loadFromData(data, 'PNG')

        resize_pixmap = img.scaled(130,150)
        self.w.w.pic.setPixmap(resize_pixmap) 
        
        familyTab = FamilyTab(self.emp_num,'info')
        self.w.w.familyTab = familyTab
        self.w.w.tabWidget.addTab(self.w.w.familyTab.family, '가족관계')

        contactTab = ContactTab(self.emp_num,'info')
        self.w.w.contactTab = contactTab
        self.w.w.tabWidget.addTab(self.w.w.contactTab.contact, '비상연락처')

        schoolTab = SchoolTab(self.emp_num,'info')
        self.w.w.schoolTab = schoolTab
        self.w.w.tabWidget.addTab(self.w.w.schoolTab.school, '학력')

        certificationTab = CertificationTab(self.emp_num,'info')
        self.w.w.certificationTab = certificationTab
        self.w.w.tabWidget.addTab(self.w.w.certificationTab.certificate, '자격증')
        
        careerTab = CareerTab(self.emp_num,'info')
        self.w.w.careerTab = careerTab
        self.w.w.tabWidget.addTab(self.w.w.careerTab.career, '경력')

        technicalTab = TechnicalTab(self.emp_num,'info')
        self.w.w.technicalTab = technicalTab
        self.w.w.tabWidget.addTab(self.w.w.technicalTab.technical, '기술사항')

        rpTab = RPTab(self.emp_num,'info')
        self.w.w.rpTab = rpTab
        self.w.w.tabWidget.addTab(self.w.w.rpTab.rp, '상벌')

        rsTab = RSTab(self.emp_num,'info')
        self.w.w.rsTab = rsTab
        self.w.w.tabWidget.addTab(self.w.w.rsTab.rs, '호봉')
        
        self.w.w.layout = QVBoxLayout()
        self.w.w.layout.addWidget(self.w.w.tabWidget)
        
        
    # 231201 개인정보수정화면 by 정현아 
    def showEdit(self):
        familyTab = FamilyTab(self.emp_num,'edit')
        self.w.w.w.familyTab = familyTab
        self.w.w.w.tabWidget.addTab(self.w.w.w.familyTab.family, '가족관계')
        
        contactTab = ContactTab(self.emp_num,'edit')
        self.w.w.w.contactTab = contactTab
        self.w.w.w.tabWidget.addTab(self.w.w.w.contactTab.contact, '비상연락처')

        schoolTab = SchoolTab(self.emp_num,'edit')
        self.w.w.w.schoolTab = schoolTab
        self.w.w.w.tabWidget.addTab(self.w.w.w.schoolTab.school, '학력')

        certificationTab = CertificationTab(self.emp_num,'edit')
        self.w.w.w.certificationTab = certificationTab
        self.w.w.w.tabWidget.addTab(self.w.w.w.certificationTab.certificate, '자격증')
        
        careerTab = CareerTab(self.emp_num,'edit')
        self.w.w.w.careerTab = careerTab
        self.w.w.w.tabWidget.addTab(self.w.w.w.careerTab.career, '경력')

        technicalTab = TechnicalTab(self.emp_num,'edit')
        self.w.w.w.technicalTab = technicalTab
        self.w.w.w.tabWidget.addTab(self.w.w.w.technicalTab.technical, '기술사항')

        rpTab = RPTab(self.emp_num,'edit')
        self.w.w.w.rpTab = rpTab
        self.w.w.w.tabWidget.addTab(self.w.w.w.rpTab.rp, '상벌')

        rsTab = RSTab(self.emp_num,'edit')
        self.w.w.w.rsTab = rsTab
        self.w.w.w.tabWidget.addTab(self.w.w.w.rsTab.rs, '호봉')
        
        self.w.w.w.layout = QVBoxLayout()
        self.w.w.w.layout.addWidget(self.w.w.w.tabWidget)
        
        query = """
        SELECT 
        NAME_KOR, NAME_ENG, EMP_NUM, DATE_JOIN, EMP_RANK, SUBSTRING(REG_NUM,1,6), SUBSTRING(REG_NUM,7,7), MAIL, SUBSTRING(PHONE,1,3), SUBSTRING(PHONE,4,4), 
        SUBSTRING(PHONE,8,4), DEPT_BIZ, WORK_POS, POSITION, ADDRESS_NUM, ADDRESS, SUBSTRING(SALARY,1,1), 
        IFNULL(HEIGHT,''), IFNULL(WEIGHT,''), IFNULL(MILITARY,''), IFNULL(MARRY,''), LAST_EDU, PIC, DEPT_GROUP, SUBSTRING(SALARY,2,3), AGE, GENDER
        FROM MAIN_TABLE
        WHERE EMP_NUM = %s; 
        """
        self.cur.execute(query,(self.emp_num))
        self.result = self.cur.fetchone()

        self.w.w.w.dept.activated[str].connect(self.changeGroup)
        self.w.w.w.addImgBtn.clicked.connect(self.showAddImg)
        self.w.w.w.regnum_lineEdit2.setEchoMode(QLineEdit.Password)

        # 231201 입력 제한 by 정현아
        self.w.w.w.regnum_lineEdit.setValidator(QIntValidator(1,100000,self))
        self.w.w.w.regnum_lineEdit2.setValidator(QIntValidator(1,1000000,self))
        self.w.w.w.phone_lineEdit2.setValidator(QIntValidator(1,1000,self))
        self.w.w.w.phone_lineEdit3.setValidator(QIntValidator(1,1000,self))
        self.w.w.w.addressnum_lineEdit.setValidator(QIntValidator(1,10000,self))
        rep = QRegExp("[가-힣0-9\\s,()]{0,49}")
        self.w.w.w.address_lineEdit.setValidator(QRegExpValidator(rep))
        self.w.w.w.height_lineEdit.setValidator(QIntValidator(1,100,self))
        self.w.w.w.weight_lineEdit.setValidator(QIntValidator(1,100,self))

        if(self.result_pass[2] == 'Regular'):
            self.w.w.w.namekor.setDisabled(True)

            self.w.w.w.empnum.setDisabled(True)
            self.w.w.w.regnum_lineEdit.setDisabled(True)
            self.w.w.w.regnum_lineEdit2.setDisabled(True)
            self.w.w.w.joindate.setDisabled(True)

        # 231201 저장된 사원정보가져와 라벨 및 에디트에 세팅 by 정현아
        self.w.w.w.namekor.setText(self.result[0])
        self.w.w.w.nameeng.setText(self.result[1])
        self.w.w.w.empnum.setText(str(self.result[2]))
        date_str = self.result[3].strftime("%Y-%m-%d")
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        self.w.w.w.joindate.setDate(date)
        self.w.w.w.emprank.setCurrentText(self.result[4])
        self.w.w.w.regnum_lineEdit.setText(self.result[5])
        self.w.w.w.regnum_lineEdit2.setText(self.result[6])
        self.w.w.w.mail_lineEdit.setText(self.result[7])
        self.w.w.w.phone_combo.setCurrentText(self.result[8])
        self.w.w.w.phone_lineEdit2.setText(self.result[9])
        self.w.w.w.phone_lineEdit3.setText(self.result[10])
        self.w.w.w.dept.setCurrentText(self.result[11])

        self.w.w.w.work_pos.setCurrentText(self.result[12])
        self.w.w.w.position.setCurrentText(self.result[13])
        self.w.w.w.addressnum_lineEdit.setText(str(self.result[14]))
        self.w.w.w.address_lineEdit.setText(self.result[15])
        self.w.w.w.sal.setCurrentText(self.result[16])
        self.w.w.w.height_lineEdit.setText(str(self.result[17]))
        self.w.w.w.weight_lineEdit.setText(str(self.result[18]))
        mil = self.result[19]
        if mil == '군필':
            self.w.w.w.milBtn.setChecked(True)
        elif mil == '미필':
            self.w.w.w.milBtn2.setChecked(True)
        else:
            self.w.w.w.milBtn3.setChecked(True)
        
        marry = self.result[20]
        if marry == '기혼':
            self.w.w.w.maryyBtn.setChecked(True)
        else : 
            self.w.w.w.maryyBtn2.setChecked(True)
            
        self.w.w.w.lastedu_combo.setCurrentText(self.result[21])
        resize_pixmap = self.img.scaled(130,150)
        self.w.w.w.pic.setPixmap(resize_pixmap) 
        self.w.w.w.saveBtn.clicked.connect(self.saveEdit)
        
        self.changeGroup(self.result[11])
        self.w.w.w.dept_g.setCurrentText(self.result[23])
        self.w.w.w.sal2.setText(self.result[24])
    
    def changeGroup(self,biz):
        self.w.w.w.dept_g.clear()
        if biz == '경영지원실':
            self.w.w.w.dept_g.addItems(self.BS)
        elif biz == 'TSP':
            self.w.w.w.dept_g.addItems(self.TSP)
            return
        elif biz == 'FAB':
            self.w.w.w.dept_g.addItems(self.FAB)
            return
        elif biz == 'MIS':
            self.w.w.w.dept_g.addItems(self.MIS)
            return
        elif biz == 'TC':
            self.w.w.w.dept_g.addItems(self.TC)
            return
        elif biz == '전략기획실':    
            self.w.w.w.dept_g.addItems(self.SP) 
            return        

    def saveEdit(self):
        date_str = self.result[3].strftime("%Y-%m-%d")
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        attrDict ={
            '주민번호': self.result[5] + self.result[6],  
            '메일': self.result[7], 
            '휴대폰번호': self.result[8] + self.result[9] + self.result[10],  
            '우편번호':self.result[14],
            '주소':self.result[15], 
            '신장': self.result[17],  
            '체중': self.result[18],             
            '군필여부': self.result[19], 
            '결혼여부': self.result[20],  
            '최종학력': self.result[21],            
            '사진': self.result[22],
            '한글성명': self.result[0],
            '영문성명': self.result[1],
            '사번': self.result[2],
            '입사일': date,
            '직급': self.result[4],
            '사업부': self.result[11],
            '직책': self.result[12],
            '그룹': self.result[23],
            '직무': self.result[13],
            '호봉': self.result[16] + self.result[24],
            '나이': self.result[25],
            '성별': self.result[26]
            }        
        attrDict['주민번호'] = self.w.w.w.regnum_lineEdit.text() + self.w.w.w.regnum_lineEdit2.text()
        reg_num = self.w.w.w.regnum_lineEdit.text() + self.w.w.w.regnum_lineEdit2.text()
        attrDict['메일'] = self.w.w.w.mail_lineEdit.text()
        attrDict['휴대폰번호'] = self.w.w.w.phone_combo.currentText() + self.w.w.w.phone_lineEdit2.text() + self.w.w.w.phone_lineEdit3.text()
        if self.w.w.w.addressnum_lineEdit.text() == '':
            QMessageBox.warning(self, "사원등록실패", "우편번호가 입력되지 않았습니다. 우편번호 입력바랍니다.")
            return
        else:
            attrDict['우편번호'] = int(self.w.w.w.addressnum_lineEdit.text())
        attrDict['주소'] = self.w.w.w.address_lineEdit.text()

        height = self.w.w.w.height_lineEdit.text()
        weight = self.w.w.w.weight_lineEdit.text()

        if height == '': 
            attrDict['신장'] = None
        else:
            attrDict['신장'] = int(height)

        if weight == '': 
            attrDict['체중'] = None
        else:
            attrDict['체중'] = int(weight)       


        if self.w.w.w.milBtn.isChecked():
            attrDict['군필여부'] = self.w.w.w.milBtn.text()
        elif self.w.w.w.milBtn2.isChecked():
            attrDict['군필여부'] = self.w.w.w.milBtn2.text()
        else:
            attrDict['군필여부'] = self.w.w.w.milBtn3.text()
            
        if self.w.w.w.maryyBtn.isChecked():
            attrDict['결혼여부'] = self.w.w.w.maryyBtn.text()
        else:
            attrDict['결혼여부'] = self.w.w.w.maryyBtn2.text()    
        attrDict['최종학력'] = self.w.w.w.lastedu_combo.currentText()

        if self.pixmap is not None:
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            self.pixmap.toImage().save(buffer, 'PNG')
            attrDict['사진'] = byte_array.data()  

        attrDict['한글성명'] = self.w.w.w.namekor.text()
        attrDict['영문성명'] = self.w.w.w.nameeng.text()
        # 사번은 int type
        if self.w.w.w.empnum.text() != '' :
            attrDict['사번'] = int(self.w.w.w.empnum.text())
        attrDict['입사일'] = self.w.w.w.joindate.date().toString("yyyy-MM-dd")
        attrDict['직급'] = self.w.w.w.emprank.currentText()
        attrDict['사업부'] = self.w.w.w.dept.currentText()
        attrDict['직책'] = self.w.w.w.work_pos.currentText()
        attrDict['그룹'] = self.w.w.w.dept_g.currentText()
        attrDict['직무'] = self.w.w.w.position.currentText()
        attrDict['호봉'] = self.w.w.w.sal.currentText() + self.w.w.w.sal2.text()


        for key, value in attrDict.items():
            if key =='휴대폰번호':
                if len(value) < 11 :
                    QMessageBox.warning(self, "개인정보변경실패", "{} 11자리가 입력되지 않았습니다. {} 입력바랍니다.".format(key, key))
                    return
            elif not (key == '신장' or key == '체중'):
                if value == '':
                    QMessageBox.warning(self, "개인정보변경실패", "{}이(가) 입력되지 않았습니다. {} 입력바랍니다.".format(key, key))
                    return
        
        if attrDict['주민번호'] == '' or len(attrDict['주민번호']) != 13:
            QMessageBox.warning(self, "개인정보변경실패", "주민번호 13자리가 입력되지 않았습니다. 주민번호 입력바랍니다.")
            return
        else:
            if reg_num[6] == '0' or reg_num[6] == '9' :
                QMessageBox.warning(self, "개인정보변경실패", "주민번호 2번째 첫자리는 1~8까지 입력가능합니다.")
                return
            elif reg_num[6] == '1' or reg_num[6] == '2' or reg_num[6] == '5' or reg_num[6] == '6':
                birthYear = 1900 + int(reg_num[:2])
            elif reg_num[6] == '3' or reg_num[6] == '4' or reg_num[6] == '7' or reg_num[6] == '8':
                birthYear = 2000 + int(reg_num[:2])
            

            if int(reg_num[2:4])>12 or reg_num[2:4] =='00' or reg_num[4:6] == '00':
                QMessageBox.warning(self, "개인정보변경실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                return
            elif reg_num[2:4] =='01' or  reg_num[2:4] =='03' or reg_num[2:4] =='05' or reg_num[2:4] == '07' or reg_num[2:4] == '08' or reg_num[2:4] == '10' or reg_num[2:4] == '12':
                if int(reg_num[4:6]) > 31:
                    QMessageBox.warning(self, "개인정보변경실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
            elif reg_num[2:4] =='04' or reg_num[2:4] =='06' or reg_num[2:4] =='09' or reg_num[2:4] =='11':
                if int(reg_num[4:6]) > 30:
                    QMessageBox.warning(self, "개인정보변경실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
            else:
                if int(reg_num[4:6]) > 28:
                    QMessageBox.warning(self, "개인정보변경실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
                
            age =  int(QDate(birthYear,int(reg_num[2:4]),int(reg_num[4:6])).daysTo(QDate.currentDate())/365)
            if age < 19:
                QMessageBox.warning(self, "개인정보변경실패", "나이가 만 19세보다 어립니다.주민번호 확인바랍니다.")
                return
            elif age > 80:
                QMessageBox.warning(self, "개인정보변경실패", "나이가 만 80세보다 많습니다.주민번호 확인바랍니다.")
                return
            else:
                attrDict['나이'] = age

            if int(reg_num[6]) % 2 == 1:
                attrDict['성별'] = '남'
            else : 
                attrDict['성별'] = '여'

        if len(str(attrDict['사번'])) < 8:
            QMessageBox.warning(self,'개인정보변경실패','사번은 8자리를 입력하셔야 합니다.')
            return
        
        if int(str(attrDict['사번'])[:2]) < 12 or int(str(attrDict['사번'])[:2]) > int(QDate.currentDate().year())-2000:
            QMessageBox.warning(self,'개인정보변경실패','사번은 앞 2자리는 12보다 작거나 현재년도보다 클 수 없습니다.')
            return

        
        if not re.match(r"^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", attrDict['메일']):
            QMessageBox.warning(self,'개인정보변경실패','메일 형식이 틀립니다.메일 확인바랍니다.')
            return
        
        if len(str(attrDict['우편번호'])) != 5:
            QMessageBox.warning(self, "개인정보변경실패", "우편번호는 5자리를 입력하셔야 합니다.")
            return
        
        if self.result[5] + self.result[6] != attrDict['주민번호'] or self.result[2] != attrDict['사번'] or self.result[8] + self.result[9] + self.result[10] != attrDict['휴대폰번호']:
            t1 = (attrDict['사번'], attrDict['주민번호'], attrDict['사번'], attrDict['주민번호'], attrDict['휴대폰번호'])
            query = """
            SELECT NULLIF(EMP_NUM, %s), NULLIF(REG_NUM, %s), PHONE FROM MAIN_TABLE WHERE EMP_NUM= %s OR REG_NUM = %s OR PHONE = %s;
            """
            try:
                self.cur.execute(query, t1)
                result = self.cur.fetchone()
                if result :
                    if result[0] is not None:
                        QMessageBox.warning(self, "개인정보변경실패", "이미 등록된 사번입니다.")
                        return
                    elif result[1] is not None: 
                        QMessageBox.warning(self, "개인정보변경실패", "이미 등록된 주민번호입니다.")
                        return
                    else: 
                        QMessageBox.warning(self, "개인정보변경실패", "이미 등록된 휴대폰번호입니다.")
                        return
            except Exception as e:
                QMessageBox.warning(self, "개인정보변경실패", "Error: " + str(e))
                return        

        query = """
        UPDATE MAIN_TABLE 
        SET REG_NUM = %s, MAIL = %s, PHONE = %s, ADDRESS_NUM = %s, ADDRESS = %s, HEIGHT = %s, WEIGHT = %s, MILITARY = %s, 
        MARRY = %s, LAST_EDU = %s, PIC = %s, NAME_KOR = %s, NAME_ENG = %s, EMP_NUM = %s, DATE_JOIN =%s, EMP_RANK = %s, 
        DEPT_BIZ = %s, WORK_POS = %s, DEPT_GROUP = %s, POSITION = %s, SALARY =%s, AGE = %s, GENDER = %s
        WHERE EMP_NUM = %s; 
        """
        reply = QMessageBox.question(self, '변경 확인', '변경하시겠습니까??', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.execute(query,tuple(attrDict.values()) + (self.emp_num,))
                self.conn.commit()
                self.w.w.w.familyTab.saveFamily(self.emp_num,self.cur,self.conn)
                self.w.w.w.contactTab.saveContact(self.emp_num,self.cur,self.conn)
                self.w.w.w.schoolTab.saveSchool(self.emp_num,self.cur,self.conn)
                self.w.w.w.certificationTab.saveCertification(self.emp_num,self.cur,self.conn)
                self.w.w.w.careerTab.saveCareer(self.emp_num,self.cur,self.conn)
                self.w.w.w.technicalTab.saveTechnical(self.emp_num,self.cur,self.conn)
                self.w.w.w.rpTab.saveRP(self.emp_num,self.cur,self.conn)
                self.w.w.w.rsTab.saveRS(self.emp_num,self.cur,self.conn)
                QMessageBox.information(self, "개인정보변경성공", "개인정보가 변경되었습니다.")
                self.w.w.w.close()

                self.showMyInfo()

                data = attrDict['사진']
                self.img = QPixmap()
                self.img.loadFromData(data, 'PNG')
                icon = QIcon(self.img)        
                self.w.chgBtn.setIcon(icon)                

            except Exception as e:
                QMessageBox.warning(self, "개인정보변경실패", "Error: " + str(e))
                print("Query:", query)
                print("Values:", tuple(attrDict.values()) + (self.emp_num,))
                return 

    def showAddImg(self):
        self.w1 = QDialog(self)
        addImg = uic.loadUi(resource_path('add_img.ui'), self.w1)
        self.w1.searchbutton.clicked.connect(self.openImage)
        self.w1.savebtn.clicked.connect(self.save_img)
        self.w1.cnlBtn.clicked.connect(self.w1.accept)
        result = self.w1.exec_()  
    
    # 231130 이미지 선택하고 다이알로그 텍스트 라인 에디트에 파일경로 세팅 by 정현아
    def openImage(self):
        self.path = None
        self.fname = None
        self.fname, _ = QFileDialog.getOpenFileName(self, '이미지 파일 찾기', 'C:/Program Files', '이미지 파일(*.jpg *.gif, *.png)')
        if self.fname:
            max_file_size_mb = 1
            max_file_size_bytes = max_file_size_mb * 1024 * 1024
            
            size, self.path = self.getFileSize(self.fname)
            if size >= max_file_size_bytes:
                QMessageBox.warning(self,'사진등록실패','사진 사이즈가 1MB를 초과하였습니다.')
                return
            else:
                self.w1.imgPath_textEdit.setText(self.path)
                self.w1.hide()
                self.w1.show()

    def getFileSize(self, file_path):
        return os.path.getsize(file_path), file_path
    
    # 231130 선택한 이미지 등록화면에 띄우기 by 정현아
    def save_img(self):
        if self.path is None :
            QMessageBox.warning(self,'사진등록실패','선택된 사진이 없습니다.')
            return
        else: 
                self.pixmap = QPixmap(self.fname)
                width = 130
                height = 150
                resize_pixmap = self.pixmap.scaled(width,height)
                self.w.w.w.pic.setPixmap(resize_pixmap)
        self.w1.close()
        
    def back(self):
        self.w.close()
        self.idlineEdit.clear()
        self.passwdlineEdit.clear()
        
    def showFind(self):
        self.w = Find()
        result = self.w.exec_()
        self.w.cnlBtn.clicked.connect(self.w.accept)
        self.w.cnlBtn_2.clicked.connect(self.w.accept)
    
    # 231127 패스워드 변경 페이지 호출 by 정현아
    def showChPw(self):
        self.w2 = QDialog(self)
        addImg = uic.loadUi(resource_path('change_pw.ui'), self.w2)
        self.w2.cnlBtn.clicked.connect(self.w2.accept)
        self.w2.chgBtn.clicked.connect(self.changPw)
        self.w2.oldpwlineEdit.returnPressed.connect(self.changPw)
        result = self.w2.exec_()
        
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
            self.w2.accept()
            
stylesheet = """
    QMenu{
        background-color: white;
        color: black;
        font-family: Malgun Gothic;
    }
    QMenu::item:selected{
        background-color: #c6c6c6; 
    }
    QLabel{
        color: #404040;
    }
"""
            


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Login() 
    myWindow.show() 
    app.exec_() 