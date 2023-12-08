import os
import sys
import re
import pymysql
import requests

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
from add_img import AddImg

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('emp_regist.ui')
form_class = uic.loadUiType(form)[0]

# 231203 가족탭 생성 by 정현아
class FamilyTab(QWidget):
    def __init__(self, parent=None):
        super(FamilyTab, self).__init__(parent)
        self.cnt = 0
        self.initUI()

    def initUI(self):
        self.family = QScrollArea()
        self.cnt = 0
        self.fwidget = QWidget()
        self.family.setWidget(self.fwidget)
        self.flay = QGridLayout(self.fwidget)
        self.family.setWidgetResizable(True)

        self.fName_lbl = []
        self.fName_le = []
        self.fYear_lbl = []
        self.fYear_de = []
        self.fRel_lbl = []
        self.fRel_cb = []
        self.fLive_lbl = []
        self.fLive_cb = []
        self.familyWidget = [self.fName_lbl, self.fName_le, self.fYear_lbl, self.fYear_de, self.fRel_lbl, 
                             self.fRel_cb, self.fLive_lbl, self.fLive_cb]
        self.fAdd_btn = QPushButton("추가")
        
        self.addFamilyMember()
        self.fAdd_btn.clicked.connect(self.addFamilyMember)

    def addFamilyMember(self):
        if(self.cnt<=4):
            self.fName_lbl.append(QLabel("가족성명"))
            self.fName_le.append(QLineEdit(self))
            self.fYear_lbl.append(QLabel("생년월일"))
            self.fYear_de.append(QDateEdit(self))
            self.fRel_lbl.append(QLabel("관계"))
            self.fRel_cb.append(QComboBox())
            self.f_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
            for i in range(len(self.f_list)):
                self.fRel_cb[self.cnt].addItem(self.f_list[i])
            self.fLive_lbl.append(QLabel("동거여부"))
            self.fLive_cb.append(QComboBox())
            self.fLive_cb[self.cnt].addItem('Y')
            self.fLive_cb[self.cnt].addItem('N')
            
            for i in range(len(self.familyWidget)):
                if i == 0:
                    self.flay.addWidget(self.familyWidget[i][self.cnt],0 + 4 * self.cnt,0)
                elif i % 2 == 0:
                    self.flay.addWidget(self.familyWidget[i][self.cnt],int(i/2) + 4 * self.cnt,0)
                elif i % 2 == 1:
                    self.flay.addWidget(self.familyWidget[i][self.cnt],int(i/2) + 4 * self.cnt,1)
                    if i % 4 == 3:
                        self.flay.addWidget(self.fAdd_btn,int(i/2) + 4 * self.cnt,2)
            
            self.flay.setRowStretch((self.flay.rowCount()*(4-self.cnt)),1)
            self.cnt+=1
            
        else:
            QMessageBox.information(self,"경고","5번 이상 등록하실 수 없습니다.")
            
    # 231204 가족정보 DB 저장
    def saveFamily(self, emp_num, cur, conn):
        for i in range(self.cnt):
            if self.fName_le[i].text() == '':
                return
            
            fName = self.fName_le[i].text()
            fYear = self.fYear_de[i].date().toString("yyyy-MM-dd")
            birth = self.fYear_de[i].date()
            age = int(birth.daysTo(QDate.currentDate())/365)
            fRel = self.fRel_cb[i].currentText()
            fLive = self.fLive_cb[i].currentText()
            print(emp_num, fName, fYear, age, fRel, fLive)
            
            query = "INSERT INTO FAMILY VALUES(%s, %s, %s, %s, %s, %s)"
            cur.execute(query, (emp_num, fName, fYear, age, fRel, fLive))
            conn.commit()  
            
    def initFamily(self):
        self.fName_le[0].clear()
        self.fYear_de[0].setDate(QDate(2000, 1, 1))
        self.fRel_cb[0].setCurrentIndex(0)
        self.fLive_cb[0].setCurrentIndex(0)
        self.cnt = 0

# 연락처탭
class ContactTab(QWidget):
    def __init__(self, parent=None):
        super(ContactTab, self).__init__(parent)
        self.cnt = 0
        self.initUI()

    def initUI(self):
        self.contact = QScrollArea()
        self.cnt = 0
        self.cwidget = QWidget()
        self.contact.setWidget(self.cwidget)
        self.clay = QGridLayout(self.cwidget)
        self.contact.setWidgetResizable(True)

        self.cName_lbl = []
        self.cName_le = []
        self.cRel_lbl = []
        self.cRel_cb = []
        self.cCont_lbl = []
        self.cCont_le = []
        self.contactWidget = [self.cName_lbl, self.cName_le, self.cRel_lbl, self.cRel_cb, self.cCont_lbl, self.cCont_le]
        self.cAdd_btn = QPushButton("추가")
        
        self.addContact()
        self.cAdd_btn.clicked.connect(self.addContact)

    # 231204 긴급연락처 DB저장
    def addContact(self):
        if(self.cnt<=1):
            self.cName_lbl.append(QLabel("성명"))
            self.cName_le.append(QLineEdit(self))
            self.cRel_lbl.append(QLabel("관계"))
            self.cRel_cb.append(QComboBox())
            self.c_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
            for i in range(len(self.c_list)):
                self.cRel_cb[self.cnt].addItem(self.c_list[i])
            self.cCont_lbl.append(QLabel("연락처"))
            self.cCont_le.append(QLineEdit(self))
            
            for i in range(len(self.contactWidget)):
                if i == 0:
                    self.clay.addWidget(self.contactWidget[i][self.cnt],0 + 3 * self.cnt,0)
                elif i % 2 == 0:
                    self.clay.addWidget(self.contactWidget[i][self.cnt],int(i/2) + 3 * self.cnt,0)
                elif i % 2 == 1:
                    self.clay.addWidget(self.contactWidget[i][self.cnt],int(i/2) + 3 * self.cnt,1)
                    if i % 3 == 2:
                        self.clay.addWidget(self.cAdd_btn,int(i/2) + 3 * self.cnt,2)
            # 연락처 라인에디트에 입력제한 by 정현아
            for i in range(self.cnt+1):
                self.cCont_le[i].setValidator(QIntValidator())
                self.cCont_le[i].setMaxLength(11)
                
            self.clay.setRowStretch((self.clay.rowCount()*(4-self.cnt)),1)
            self.cnt+=1
            
        else:
            QMessageBox.information(self,"경고","2번 이상 등록하실 수 없습니다.")
            
    def saveContact(self, emp_num, cur, conn):
        for i in range(self.cnt):
            if self.cName_le[i].text() == '':
                return
            
            cName = self.cName_le[i].text()
            cRel = self.cRel_cb[i].currentText()
            cCont = self.cCont_le[i].text()
            print(emp_num, cName, cRel, cCont)
            
            query = "INSERT INTO CONTACT VALUES(%s, %s, %s, %s)"
            cur.execute(query, (emp_num, cName, cRel, cCont))
            conn.commit()    
            
    def initContact(self):
        self.cName_le[0].clear()
        self.cRel_cb[0].setCurrentIndex(0)
        self.cCont_le[0].clear()
        self.cnt = 0

# 학력 탭
class SchoolTab(QWidget):
    def __init__(self, parent=None):
        super(SchoolTab, self).__init__(parent)
        self.cnt = 0
        self.initUI()

    def initUI(self):
        self.school = QScrollArea()
        self.cnt = 0
        self.schwidget = QWidget()
        self.school.setWidget(self.schwidget)
        self.schlay = QGridLayout(self.schwidget)
        self.school.setWidgetResizable(True)

        self.scheadmit_lbl = []
        self.scheadmit_de = []
        self.schgrad_lbl = []
        self.schgrad_de = []
        self.schname_lbl = []
        self.schname_le = []
        self.schloc_lbl = []
        self.schloc_le = []
        self.schmajor_lbl = []
        self.schmajor_le = []
        self.schsubmajor_lbl = []
        self.schsubmajor_le = []
        self.comment_lbl = []
        self.comment_le = []
        self.schWidget = [self.scheadmit_lbl, self.scheadmit_de, self.schgrad_lbl, self.schgrad_de, self.schname_lbl, self.schname_le, self.schloc_lbl , self.schloc_le ,
                          self.schmajor_lbl , self.schmajor_le , self.schsubmajor_lbl , self.schsubmajor_le , self.comment_lbl , self.comment_le ]
        self.schAdd_btn = QPushButton("추가")

        self.addSchoolInfo()
        self.schAdd_btn.clicked.connect(self.addSchoolInfo)

    def addSchoolInfo(self):
        if(self.cnt<=3):
            self.scheadmit_lbl.append(QLabel("입학일"))
            self.scheadmit_de.append(QDateEdit(self))
            self.schgrad_lbl.append(QLabel("졸업일"))
            self.schgrad_de.append(QDateEdit(self))
            self.schname_lbl.append(QLabel("학교명"))
            self.schname_le.append(QLineEdit(self))
            self.schloc_lbl.append(QLabel("소재지"))
            self.schloc_le.append(QLineEdit(self))
            self.schmajor_lbl.append(QLabel("전공"))
            self.schmajor_le.append(QLineEdit(self))
            self.schsubmajor_lbl.append(QLabel("복수전공"))
            self.schsubmajor_le.append(QLineEdit(self))
            self.comment_lbl.append(QLabel("특기사항"))
            self.comment_le.append(QLineEdit(self))
            
            for i in range(len(self.schWidget)):
                if i == 0:
                    self.schlay.addWidget(self.schWidget[i][self.cnt],0 + 7 * self.cnt,0)
                elif i % 2 == 0:
                    self.schlay.addWidget(self.schWidget[i][self.cnt],int(i/2) + 7 * self.cnt,0)
                elif i % 2 == 1:
                    self.schlay.addWidget(self.schWidget[i][self.cnt],int(i/2) + 7 * self.cnt,1)
                    if i % 7 == 6:
                        self.schlay.addWidget(self.schAdd_btn,int(i/2) + 7 * self.cnt,2)
            
            self.schlay.setRowStretch((self.schlay.rowCount()*(4-self.cnt)),1)
            self.cnt+=1;
            
        else:
            QMessageBox.information(self,"경고","4번 이상 등록하실 수 없습니다.")
            
    def saveSchool(self, emp_num, cur, conn):
        for i in range(self.cnt):
            if self.schname_le[i].text() == '':
                return
            
            schAdmitDate = self.scheadmit_de[i].date().toString("yyyy-MM-dd")
            schGradDate = self.schgrad_de[i].date().toString("yyyy-MM-dd")
            schName = self.schname_le[i].text()
            schLoc = self.schloc_le[i].text()
            schMajor = self.schmajor_le[i].text()
            schSubMajor = self.schsubmajor_le[i].text()
            schComment = self.comment_le[i].text()
            
            query = "INSERT INTO SCHOOL_EDUCATION VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (emp_num, schAdmitDate, schGradDate, schName, schLoc, schMajor, schSubMajor, schComment))
            conn.commit()
            
    def initSchool(self):
        self.scheadmit_de[0].setDate(QDate(2000, 1, 1))
        self.schgrad_de[0].setDate(QDate(2000, 1, 1))
        self.schname_le[0].clear()
        self.schloc_le[0].clear()
        self.schmajor_le[0].clear()
        self.schsubmajor_le[0].clear()
        self.comment_le[0].clear()
        self.cnt = 0

# 자격증 탭
class CertificationTab(QWidget):
    def __init__(self, parent=None):
        super(CertificationTab, self).__init__(parent)
        self.cnt = 0
        self.initUI()

    def initUI(self):
        self.certificate = QScrollArea()
        self.cnt = 0
        self.certwidget = QWidget()
        self.certificate.setWidget(self.certwidget)
        self.certlay = QGridLayout(self.certwidget)
        self.certificate.setWidgetResizable(True)

        self.certName_lbl = []
        self.certName_le = []
        self.certDate_lbl = []
        self.certDate_de = []
        self.certwidget = [self.certName_lbl, self.certName_le, self.certDate_lbl, self.certDate_de]
        self.certAdd_btn = QPushButton("추가")
        
        self.addCertification()
        self.certAdd_btn.clicked.connect(self.addCertification)

    def addCertification(self):
        if(self.cnt<=9):
            self.certName_lbl.append(QLabel("자격증명"))
            self.certName_le.append(QLineEdit(self))
            self.certDate_lbl.append(QLabel("취득일"))
            self.certDate_de.append(QDateEdit(self))
            
            for i in range(len(self.certwidget)):
                if i == 0:
                    self.certlay.addWidget(self.certwidget[i][self.cnt],0 + 2 * self.cnt,0)
                elif i % 2 == 0:
                    self.certlay.addWidget(self.certwidget[i][self.cnt],int(i/2) + 2 * self.cnt,0)
                elif i % 2 == 1:
                    self.certlay.addWidget(self.certwidget[i][self.cnt],int(i/2) + 2 * self.cnt,1)
                    self.certlay.addWidget(self.certAdd_btn,int(i/2) + 2 * self.cnt,2)
            
            self.certlay.setRowStretch((self.certlay.rowCount()*(4-self.cnt)),1)
            self.cnt+=1;
            
        else:
            QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")
            
    def saveCertification(self, emp_num, cur, conn):
        for i in range(self.cnt):
            if self.certName_le[i].text() == '':
                return
            certName = self.certName_le[i].text()
            certDate = self.certDate_de[i].date().toString("yyyy-MM-dd")
                
            query = "INSERT INTO CERTIFICATE VALUES (%s, %s, %s)"
            cur.execute(query, (emp_num, certName, certDate))
            conn.commit() 
            
    def initCertification(self):
        self.certName_le[0].clear()
        self.certDate_de[0].setDate(QDate(2000, 1, 1))
        self.cnt = 0

# 경력탭
class CareerTab(QWidget):
    def __init__(self, parent=None):
        super(CareerTab, self).__init__(parent)
        self.cnt = 0
        self.initUI()

    def initUI(self):
        self.career = QScrollArea()
        self.cnt = 0
        self.carwidget = QWidget()
        self.career.setWidget(self.carwidget)
        self.carlay = QGridLayout(self.carwidget)
        self.career.setWidgetResizable(True)

        self.company_lbl = []
        self.company_le = []
        self.dept_lbl = []
        self.dept_le = []
        self.datejoin_lbl = []
        self.datejoin_de = []
        self.dateleave_lbl = []
        self.dateleave_de = []
        self.finalrank_lbl = []
        self.finalrank_le = []
        self.workinfo_lbl = []
        self.workinfo_le = []
        self.carWidget = [self.company_lbl, self.company_le, self.dept_lbl, self.dept_le, self.datejoin_lbl, self.datejoin_de, self.dateleave_lbl , self.dateleave_de ,
                          self.finalrank_lbl , self.finalrank_le , self.workinfo_lbl , self.workinfo_le ]
        self.carAdd_btn = QPushButton("추가")

        self.addCareerInfo()
        self.carAdd_btn.clicked.connect(self.addCareerInfo)

    def addCareerInfo(self):
        if(self.cnt<=9):
            self.company_lbl.append(QLabel("근무회사"))
            self.company_le.append(QLineEdit(self))
            self.dept_lbl.append(QLabel("근무부서"))
            self.dept_le.append(QLineEdit(self))
            self.datejoin_lbl.append(QLabel("입사일"))
            self.datejoin_de.append(QDateEdit(self))
            self.dateleave_lbl.append(QLabel("퇴사일"))
            self.dateleave_de.append(QDateEdit(self))
            self.finalrank_lbl.append(QLabel("최종직급"))
            self.finalrank_le.append(QLineEdit(self))
            self.workinfo_lbl.append(QLabel("업무내용"))
            self.workinfo_le.append(QLineEdit(self))

            for i in range(len(self.carWidget)):
                if i == 0:
                    self.carlay.addWidget(self.carWidget[i][self.cnt],0 + 6 * self.cnt,0)
                elif i % 2 == 0:
                    self.carlay.addWidget(self.carWidget[i][self.cnt],int(i/2) + 6 * self.cnt,0)
                elif i % 2 == 1:
                    self.carlay.addWidget(self.carWidget[i][self.cnt],int(i/2) + 6 * self.cnt,1)
                    if i % 6 == 5:
                        self.carlay.addWidget(self.carAdd_btn,int(i/2) + 6 * self.cnt,2)
            
            self.carlay.setRowStretch((self.carlay.rowCount()*(4-self.cnt)),1)
            self.cnt+=1;
            
        else:
            QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")
            
    def saveCareer(self, emp_num, cur, conn):
        for i in range(self.cnt):
            if self.company_le[i].text() == '':
                return
            company = self.company_le[i].text()
            dept = self.dept_le[i].text()
            datejoin = self.datejoin_de[i].date().toString("yyyy-MM-dd")
            dateleave = self.dateleave_de[i].date().toString("yyyy-MM-dd")
            workdays = self.datejoin_de[i].date().daysTo(self.dateleave_de[i].date())
            years, months = divmod(workdays, 365)
            months = months/30.44/12
            workperiod = round(years + months,1)
            finalrank = self.finalrank_le[i].text()
            workinfo = self.workinfo_le[i].text()

            query = "INSERT INTO CAREER VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (emp_num, company, dept, datejoin, dateleave, workperiod, finalrank, workinfo))
            conn.commit()

    def initCareer(self):
        self.company_le[0].clear()
        self.dept_le[0].clear()
        self.datejoin_de[0].setDate(QDate(2000, 1, 1))
        self.dateleave_de[0].setDate(QDate(2000, 1, 1))
        self.finalrank_le[0].clear()
        self.workinfo_le[0].clear()
        self.cnt = 0

# 기술사항탭
class TechnicalTab(QWidget):
    def __init__(self, parent=None):
        super(TechnicalTab, self).__init__(parent)
        self.cnt = 0
        self.initUI()

    def initUI(self):
        self.technical = QScrollArea()
        self.cnt = 0
        self.techwidget = QWidget()
        self.technical.setWidget(self.techwidget)
        self.techlay = QGridLayout(self.techwidget)
        self.technical.setWidgetResizable(True)

        self.techDet_lbl = []
        self.techDet_le = []
        self.pro_lbl = []
        self.pro_cb = []
        self.note_lbl = []
        self.note_le = []
        self.techWidget = [self.techDet_lbl, self.techDet_le, self.pro_lbl, self.pro_cb, self.note_lbl, self.note_le]
        self.techAdd_btn = QPushButton("추가")
        
        self.addTechMember()
        self.techAdd_btn.clicked.connect(self.addTechMember)

    def addTechMember(self):
        if(self.cnt<=9):
            self.techDet_lbl.append(QLabel("기술사항"))
            self.techDet_le.append(QLineEdit(self))
            self.pro_lbl.append(QLabel("숙련도"))
            self.pro_cb.append(QComboBox())
            self.pro_cb[self.cnt].addItem('상')
            self.pro_cb[self.cnt].addItem('중')
            self.pro_cb[self.cnt].addItem('하')
            self.note_lbl.append(QLabel("비고"))
            self.note_le.append(QLineEdit(self))
            
            for i in range(len(self.techWidget)):
                if i == 0:
                    self.techlay.addWidget(self.techWidget[i][self.cnt],0 + 3 * self.cnt,0)
                elif i % 2 == 0:
                    self.techlay.addWidget(self.techWidget[i][self.cnt],int(i/2) + 3 * self.cnt,0)
                elif i % 2 == 1:
                    self.techlay.addWidget(self.techWidget[i][self.cnt],int(i/2) + 3 * self.cnt,1)
                    if i % 3 == 2:
                        self.techlay.addWidget(self.techAdd_btn,int(i/2) + 3 * self.cnt,2)
            
            self.techlay.setRowStretch((self.techlay.rowCount()*(4-self.cnt)),1)
            self.cnt+=1;
            
        else:
            QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")
            
    def saveTechnical(self, emp_num, cur, conn):
        for i in range(self.cnt):
            if self.techDet_le[i].text() == '':
                return
            techDet = self.techDet_le[i].text()
            proficiency = self.pro_cb[i].currentText()
            note = self.note_le[i].text()

        query = "INSERT INTO TECHNICAL VALUES (%s, %s, %s, %s)"
        cur.execute(query, (emp_num, techDet, proficiency, note))
        conn.commit()
        
    def initTechnical(self):
        self.techDet_le[0].clear()
        self.pro_cb[0].setCurrentIndex(0)
        self.note_le[0].clear()
        self.cnt = 0

# 231203 상벌탭 생성 by 정현아
class RPTab(QWidget):
    def __init__(self, parent=None):
        super(RPTab, self).__init__(parent)
        self.cnt = 0
        self.initUI()

    def initUI(self):
        self.rp = QScrollArea()
        self.cnt = 0
        self.rpwidget = QWidget()
        self.rp.setWidget(self.rpwidget)
        self.rplay = QGridLayout(self.rpwidget)
        self.rp.setWidgetResizable(True)

        self.rpName_lbl = []
        self.rpName_le = []
        self.rpScore_lbl = []
        self.rpScore_le = []
        self.rpDate_lbl = []
        self.rpDate_de = []
        self.rpNote_lbl = []
        self.rpNote_le = []
        self.rpWidget = [self.rpName_lbl, self.rpName_le, self.rpScore_lbl, self.rpScore_le, 
                             self.rpDate_lbl, self.rpDate_de, self.rpNote_lbl, self.rpNote_le]
        self.rpAdd_btn = QPushButton("추가")
        
        self.addRPMember()
        self.rpAdd_btn.clicked.connect(self.addRPMember)

    def addRPMember(self):
        if(self.cnt<=19):
            self.rpName_lbl.append(QLabel("상벌명"))
            self.rpName_le.append(QLineEdit(self))
            self.rpScore_lbl.append(QLabel("점수"))
            self.rpScore_le.append(QLineEdit(self))
            self.rpDate_lbl.append(QLabel("상벌일"))
            self.rpDate_de.append(QDateEdit(self))
            self.rpNote_lbl.append(QLabel("상벌내용"))
            self.rpNote_le.append(QLineEdit(self))
            
            for i in range(len(self.rpWidget)):
                if i == 0:
                    self.rplay.addWidget(self.rpWidget[i][self.cnt],0 + 4 * self.cnt,0)
                elif i % 2 == 0:
                    self.rplay.addWidget(self.rpWidget[i][self.cnt],int(i/2) + 4 * self.cnt,0)
                elif i % 2 == 1:
                    self.rplay.addWidget(self.rpWidget[i][self.cnt],int(i/2) + 4 * self.cnt,1)
                    if i % 4 == 3:
                        self.rplay.addWidget(self.rpAdd_btn,int(i/2) + 4 * self.cnt,2)
                        
            for i in range(self.cnt+1):
                self.rpScore_le[i].setValidator(QIntValidator())
            
            self.rplay.setRowStretch((self.rplay.rowCount()*(4-self.cnt)),1)
            self.cnt+=1;
            
        else:
            QMessageBox.information(self,"경고","20번 이상 등록하실 수 없습니다.")

    def saveRP(self, emp_num, cur, conn):
        for i in range(self.cnt):
            if self.rpName_le[i].text() == '':
                return
            rpName = self.rpName_le[i].text()
            rpScore = int(self.rpScore_le[i].text())
            rpDate = self.rpDate_de[i].date().toString("yyyy-MM-dd")
            rpNote = self.rpNote_le[i].text()

        query = "INSERT INTO R_P VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (emp_num, rpName, rpScore, rpDate, rpNote))
        conn.commit()
        
    def initRP(self):
        self.rpName_le[0].clear()
        self.rpScore_le[0].clear()
        self.rpDate_de[0].setDate(QDate(2000, 1, 1))
        self.rpNote_le[0].clear()
        self.cnt = 0
        
# 호봉 탭
class RSTab(QWidget):
    def __init__(self, parent=None):
        super(RSTab, self).__init__(parent)
        self.cnt = 0
        self.initUI()

    def initUI(self):
        self.rs = QScrollArea()
        self.cnt = 0
        self.rswidget = QWidget()
        self.rs.setWidget(self.rswidget)
        self.rslay = QGridLayout(self.rswidget)
        self.rs.setWidgetResizable(True)

        self.rsRANK_lbl = []
        self.rsRANK_le = []
        self.rsSal_lbl = []
        self.rsSal_le = []
        self.rsDate_lbl = []
        self.rsDate_de = []
        self.rsWidget = [self.rsRANK_lbl, self.rsRANK_le, self.rsSal_lbl, self.rsSal_le, self.rsDate_lbl, self.rsDate_de]
        self.rsAdd_btn = QPushButton("추가")
        
        self.addRSMember()
        self.rsAdd_btn.clicked.connect(self.addRSMember)

    def addRSMember(self):
        if(self.cnt<=29):
            self.rsRANK_lbl.append(QLabel("직급"))
            self.rsRANK_le.append(QLineEdit(self))
            self.rsSal_lbl.append(QLabel("호봉"))
            self.rsSal_le.append(QLineEdit(self))
            self.rsDate_lbl.append(QLabel("시작일"))
            self.rsDate_de.append(QDateEdit(self))
            
            for i in range(len(self.rsWidget)):
                if i == 0:
                    self.rslay.addWidget(self.rsWidget[i][self.cnt],0 + 4 * self.cnt,0)
                elif i % 2 == 0:
                    self.rslay.addWidget(self.rsWidget[i][self.cnt],int(i/2) + 4 * self.cnt,0)
                elif i % 2 == 1:
                    self.rslay.addWidget(self.rsWidget[i][self.cnt],int(i/2) + 4 * self.cnt,1)
                    if i % 3 == 2:
                        self.rslay.addWidget(self.rsAdd_btn,int(i/2) + 4 * self.cnt,2)
            
            self.rslay.setRowStretch((self.rslay.rowCount()*(4-self.cnt)),1)
            self.cnt+=1;
            
        else:
            QMessageBox.information(self,"경고","30번 이상 등록하실 수 없습니다.")
            
    def saveRS(self, emp_num, cur, conn):
        for i in range(self.cnt):
            if self.rsRANK_le[i].text() == '':
                return
            rsRANK = self.rsRANK_le[i].text()
            rsSal = self.rsSal_le[i].text()
            rsDate = self.rsDate_de[i].date().toString("yyyy-MM-dd")

            query = "INSERT INTO R_S VALUES (%s, %s, %s, %s)"
            cur.execute(query, (emp_num, rsRANK, rsSal, rsDate))
            conn.commit()
            
    def initRS(self):
        self.rsRANK_le[0].clear()
        self.rsSal_le[0].clear()
        self.rsDate_de[0].setDate(QDate(2000, 1, 1))
        self.cnt = 0

class Regist(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)

        self.path = None
        self.fname = None
        self.pixmap = None
        self.post_num = ''
        self.post_address = ''
        self.regist.setLayout(self.regLayout)

        # 231203 메인 탭 외의 정보 탭들 생성 by 정현아
        self.familyTab = FamilyTab(self)
        self.contactTab = ContactTab(self)
        self.schoolTab = SchoolTab(self)
        self.certificationTab = CertificationTab(self)
        self.careerTab = CareerTab(self)
        self.technicalTab = TechnicalTab(self)
        self.rpTab = RPTab(self)
        self.rsTab = RSTab(self)

        self.tabWidget.addTab(self.familyTab.family, '가족관계')
        self.tabWidget.addTab(self.contactTab.contact, '비상연락처')
        self.tabWidget.addTab(self.schoolTab.school, '학력')
        self.tabWidget.addTab(self.certificationTab.certificate, '자격증')
        self.tabWidget.addTab(self.careerTab.career, '경력')
        self.tabWidget.addTab(self.technicalTab.technical, '기술사항')
        self.tabWidget.addTab(self.rpTab.rp, '상벌')
        self.tabWidget.addTab(self.rsTab.rs, '직급 및 호봉')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabWidget)
        
        # 각 입력항목들 입력 제한
        self.namekr_lineEdit.textChanged.connect(self.setValKor)
        rep = QRegExp("[a-zA-Z\\s]{0,19}")
        self.nameEng_lineEdit.setValidator(QRegExpValidator(rep))
        self.regnum_lineEdit.setValidator(QIntValidator())
        self.regnum_lineEdit.setMaxLength(6)
        self.regnum_lineEdit2.setValidator(QIntValidator(1,1000000,self))
        # rep = QRegExp("[a-z0-9]+@[a-z]+.[a-z]+.[a-z]{,2}")
        # self.email_lineEdit.setValidator(QRegExpValidator(rep))
        rep = QRegExp("[가-힣0-9\\s,()]{0,49}")
        self.addre_lineEdit.setValidator(QRegExpValidator(rep))
        self.empNum_lineEdit.setValidator(QIntValidator(1,10000000,self))
        self.phone_lineEdit2.setValidator(QIntValidator())
        self.phone_lineEdit2.setMaxLength(4)
        self.phone_lineEdit3.setValidator(QIntValidator())
        self.phone_lineEdit3.setMaxLength(4)
        self.sal_lineEdit.setMaxLength(2)
        self.height_lineEdit.setValidator(QIntValidator(1,100,self))
        self.weight_lineEdit.setValidator(QIntValidator(1,100,self))
        self.lastEdu_combo.setCurrentIndex(1)
        self.dateEdit.setDate(QDate.currentDate())
        
        # 231206 우편번호는 찾기를 통해서만 입력가능 by 정현아
        self.addressNum_lineEdit.setReadOnly(True) 

        # 231201 사번에 맞춰 기본세팅된 입사일 데이트 에디트 변경 by 정현아
        self.empNum_lineEdit.textEdited.connect(self.setJoinDate)
        # 231204 주민번호 뒷자리에 맞춰서 여자일 경우 무관 세팅 by 정현아
        self.regnum_lineEdit2.textEdited.connect(self.setMilitary)
        
        self.TSP = ['생산실행IT G','생산스케쥴IT G','생산품질IT G','TSP운영 1G','TSP운영 2G','TSP고객총괄','']
        self.FAB = ['빅데이터 G','인프라 G','스마트팩토리 G','']
        self.MIS = ['전기운영 G','PLM G','']
        self.TC = ['TC/TPSS개발파트','화성 TC2.5','SAS TC2.5','']
        self.SP = ['사업기획팀','기술전략팀','']
        self.BS = ['경영지원','']
        self.group_combo.addItems(self.TSP)
        self.biz_combo.activated[str].connect(self.changeGroup)

        self.conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        self.cur = self.conn.cursor()        

        self.addImgBtn.clicked.connect(self.showAddImg)
        self.saveBtn.clicked.connect(self.saveEmp)
        self.searchAddress.clicked.connect(self.searchPost)  

        
    # 231130 한글성명입력제한 함수 by 정현아
    def setValKor(self):
        text = self.namekr_lineEdit.text()
        if text == '':
            return
        elif not re.match("[가-힣]", text):
            QMessageBox.warning(self,'입력오류','한글을 입력해주세요')
            self.namekr_lineEdit.clear()
            return
        rep = QRegExp("[가-힣]{3,4}")
        self.namekr_lineEdit.setValidator(QRegExpValidator(rep))
    
    # 231130 사업부별 그룹 콤보박스 생성
    def changeGroup(self,biz):
        self.group_combo.clear()
        if biz == '경영지원실':
            self.group_combo.addItems(self.BS)
        elif biz == 'TSP':
            self.group_combo.addItems(self.TSP)
        elif biz == 'FAB':
            self.group_combo.addItems(self.FAB)
        elif biz == 'MIS':
            self.group_combo.addItems(self.MIS)
        elif biz == 'TC':
            self.group_combo.addItems(self.TC)
        elif biz == '전략기획실':    
            self.group_combo.addItems(self.SP) 
    
    # 231130 사원정보저장 함수 by 정현아
    def saveEmp(self):
        birthYear = 0
        attrDict ={
            '한글성명':'',  
            '영문성명':'',             
            '사번':'', 
            '주민번호':'',
            '사진':'',  
            '메일':'', 
            '휴대폰번호':'',  
            '입사일':'',             
            '사업부':'',  
            '그룹':'',   
            '직급':'',  
            '직책':'',  
            '직무':'',    
            '우편번호':'',
            '주소':'', 
            '호봉':'',  
            '신장': None,  
            '체중': None,             
            '군필여부':'', 
            '결혼여부':'',  
            '최종학력':'',            
            'age':'',
            'gender':'',  
                    }
        if self.pixmap is not None:
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            self.pixmap.toImage().save(buffer, 'PNG')
            attrDict['사진'] = byte_array.data()
            
        if self.empNum_lineEdit.text() == '':
            QMessageBox.warning(self, "사원등록실패", "사번이 입력되지 않았습니다.사번 입력바랍니다.")
            return
        else:
            attrDict['사번'] = int(self.empNum_lineEdit.text())
        attrDict['한글성명'] = self.namekr_lineEdit.text()
        attrDict['영문성명'] = self.nameEng_lineEdit.text()
        attrDict['주민번호'] = self.regnum_lineEdit.text() + self.regnum_lineEdit2.text()
        reg_num = self.regnum_lineEdit.text() + self.regnum_lineEdit2.text()
        attrDict['메일'] = self.email_lineEdit.text()
        attrDict['휴대폰번호'] = self.phone_combo.currentText() + self.phone_lineEdit2.text() + self.phone_lineEdit3.text()
        attrDict['주소'] = self.addre_lineEdit.text()
        attrDict['사업부'] = self.biz_combo.currentText()
        attrDict['그룹'] = self.group_combo.currentText()
        attrDict['입사일'] = self.dateEdit.date().toString("yyyy-MM-dd")
        attrDict['직급'] = self.rank_combo.currentText()
        attrDict['직책'] = self.workPos_combo.currentText()
        attrDict['직무'] = self.position_combo.currentText()
        attrDict['호봉'] = self.sal_combo.currentText() + self.sal_lineEdit.text()
        attrDict['최종학력'] = self.lastEdu_combo.currentText() 

        if self.height_lineEdit.text() != '':
            attrDict['신장'] = int(self.height_lineEdit.text())
        if self.weight_lineEdit.text() != '':
            attrDict['체중'] = int(self.weight_lineEdit.text())
        
        if self.military_btn.isChecked():
            attrDict['군필여부'] = self.military_btn.text()
        elif self.military_btn2.isChecked():
            attrDict['군필여부'] = self.military_btn2.text()
        else:
            attrDict['군필여부'] = self.military_btn3.text()
            
        if self.marry_btn.isChecked():
            attrDict['결혼여부'] = self.marry_btn.text()
        elif self.marry_btn2.isChecked():
            attrDict['결혼여부'] = self.marry_btn2.text()
        
        # 231130 만나이계산 및 성별 by 정현아
        if attrDict['주민번호'] == '' or len(attrDict['주민번호']) != 13:
            QMessageBox.warning(self, "사원등록실패", "주민번호 13자리가 입력되지 않았습니다. 주민번호 입력바랍니다.")
            return
        else:
            if reg_num[6] == '0' or reg_num[6] == '9' :
                QMessageBox.warning(self, "사원등록실패", "주민번호 2번째 첫자리는 1~8까지 입력가능합니다.")
                return
            elif reg_num[6] == '1' or reg_num[6] == '2' or reg_num[6] == '5' or reg_num[6] == '6':
                birthYear = 1900 + int(reg_num[:2])
            elif reg_num[6] == '3' or reg_num[6] == '4' or reg_num[6] == '7' or reg_num[6] == '8':
                birthYear = 2000 + int(reg_num[:2])
            

            if int(reg_num[2:4])>12 or reg_num[2:4] =='00' or reg_num[4:6] == '00':
                QMessageBox.warning(self, "사원등록실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                return
            elif reg_num[2:4] =='01' or  reg_num[2:4] =='03' or reg_num[2:4] =='05' or reg_num[2:4] == '07' or reg_num[2:4] == '08' or reg_num[2:4] == '10' or reg_num[2:4] == '12':
                if int(reg_num[4:6]) > 31:
                    QMessageBox.warning(self, "사원등록실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
            elif reg_num[2:4] =='04' or reg_num[2:4] =='06' or reg_num[2:4] =='09' or reg_num[2:4] =='11':
                if int(reg_num[4:6]) > 30:
                    QMessageBox.warning(self, "사원등록실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
            else:
                if int(reg_num[4:6]) > 28:
                    QMessageBox.warning(self, "사원등록실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
                
            age =  int(QDate(birthYear,int(reg_num[2:4]),int(reg_num[4:6])).daysTo(QDate.currentDate())/365)
            if age < 19:
                QMessageBox.warning(self, "사원등록실패", "나이가 만 19세보다 어립니다.주민번호 확인바랍니다.")
                return
            elif age > 80:
                QMessageBox.warning(self, "사원등록실패", "나이가 만 80세보다 많습니다.주민번호 확인바랍니다.")
                return
            else:
                attrDict['age'] = age

            if int(reg_num[6]) % 2 == 1:
                attrDict['gender'] = '남'
            else : 
                attrDict['gender'] = '여'

        if not re.match(r"^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", attrDict['메일']):
            QMessageBox.warning(self,'사원등록실패','메일 형식이 틀립니다.메일 확인바랍니다.')
            return
        
        if len(str(attrDict['사번'])) < 8:
            QMessageBox.warning(self,'사원등록실패','사번은 8자리를 입력하셔야 합니다.')
            return
        
        if int(str(attrDict['사번'])[:2]) < 12 or int(str(attrDict['사번'])[:2]) > int(QDate.currentDate().year())-2000:
            QMessageBox.warning(self,'사원등록실패','사번은 앞 2자리는 12보다 작거나 현재년도보다 클 수 없습니다.')
            return
        
        if self.addressNum_lineEdit.text() == '':
            QMessageBox.warning(self, "사원등록실패", "우편번호가 입력되지 않았습니다. 우편번호 입력바랍니다.")
            return
        else:
            attrDict['우편번호'] = int(self.addressNum_lineEdit.text())        

        if len(str(attrDict['우편번호'])) != 5:
            QMessageBox.warning(self, "사원등록실패", "우편번호는 5자리를 입력하셔야 합니다.")
            return
        
            
        for key, value in attrDict.items():
            if key == '호봉':
                if len(value) != 3 :
                    QMessageBox.warning(self, "사원등록실패", "{}이(가) 입력되지 않았습니다. {} 입력바랍니다.".format(key, key))
                    return
            elif key =='휴대폰번호':
                if len(value) < 11 :
                    QMessageBox.warning(self, "사원등록실패", "{}이(가) 입력되지 않았습니다. {} 입력바랍니다.".format(key, key))
                    return
            elif not (key == '신장' or key == '체중' or key == '그룹' or key == '직무' or key == 'age' or key == 'gender' or key == '휴대폰번호'):
                if value == '':
                    QMessageBox.warning(self, "사원등록실패", "{}이(가) 입력되지 않았습니다. {} 입력바랍니다.".format(key, key))
                    return
        t1 = (attrDict['사번'], attrDict['사번'], attrDict['주민번호'])
        query = """
        SELECT NULLIF(EMP_NUM, %s), REG_NUM FROM MAIN_TABLE WHERE EMP_NUM= %s OR REG_NUM = %s;
        """
        try:
            self.cur.execute(query, t1)
            result = self.cur.fetchone()
            if result is not None :
                if result[0] is None:
                    QMessageBox.warning(self, "사원등록실패", "이미 등록된 사번입니다.")
                    return
                else : 
                    QMessageBox.warning(self, "사원등록실패", "이미 등록된 주민번호입니다.")
                    return
        except Exception as e:
            QMessageBox.warning(self, "사원등록실패", "Error: " + str(e))
            return
        
        query = """
        INSERT INTO MAIN_TABLE (
            NAME_KOR,
            NAME_ENG,
            EMP_NUM,
            REG_NUM,
            PIC,
            MAIL,
            PHONE,
            DATE_JOIN,
            DEPT_BIZ,
            DEPT_GROUP,
            EMP_RANK,
            WORK_POS,
            POSITION,
            ADDRESS_NUM,
            ADDRESS,
            SALARY,
            HEIGHT,
            WEIGHT,
            MILITARY,
            MARRY,
            LAST_EDU,
            AGE,
            GENDER
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """  
        reply = QMessageBox.question(self, '저장 확인', '저장하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.execute(query, tuple(attrDict.values()))
                self.conn.commit()
                self.familyTab.saveFamily(attrDict['사번'],self.cur,self.conn)
                self.contactTab.saveContact(attrDict['사번'],self.cur,self.conn)
                self.schoolTab.saveSchool(attrDict['사번'],self.cur,self.conn)
                self.certificationTab.saveCertification(attrDict['사번'],self.cur,self.conn)
                self.careerTab.saveCareer(attrDict['사번'],self.cur,self.conn)
                self.technicalTab.saveTechnical(attrDict['사번'],self.cur,self.conn)
                self.rpTab.saveRP(attrDict['사번'],self.cur,self.conn)
                self.rsTab.saveRS(attrDict['사번'],self.cur,self.conn)
                QMessageBox.information(self, "사원등록성공", "사원정보가 등록되었습니다.")
            
                # 231201 등록된 내용 초기화 by 정현아
                self.namekr_lineEdit.clear()
                self.regnum_lineEdit.clear()
                self.regnum_lineEdit2.clear()
                self.nameEng_lineEdit.clear()
                self.email_lineEdit.clear()
                self.empNum_lineEdit.clear()
                self.phone_lineEdit2.clear()
                self.phone_lineEdit3.clear()
                self.addressNum_lineEdit.clear()
                self.addre_lineEdit.clear()
                self.sal_lineEdit.clear()
                self.height_lineEdit.clear()
                self.weight_lineEdit.clear()
                self.biz_combo.setCurrentIndex(0)
                self.rank_combo.setCurrentIndex(0)
                self.workPos_combo.setCurrentIndex(0)
                self.position_combo.setCurrentIndex(0)
                self.sal_combo.setCurrentIndex(0)
                self.lastEdu_combo.setCurrentIndex(1)
                self.dateEdit.setDate(QDate.currentDate())
                self.group_combo.addItems(self.TSP)
                
                self.pixmap = QPixmap('C:/Users/정현아/.ssh/HRIS/unknown.png')
                width = 130
                height = 150
                resize_pixmap = self.pixmap.scaled(width,height)
                self.img_label.setPixmap(resize_pixmap)   
                
                self.familyTab.initFamily()
                self.contactTab.initContact()
                self.schoolTab.initSchool()
                self.certificationTab.initCertification()
                self.careerTab.initCareer()
                self.technicalTab.initTechnical()
                self.rpTab.initRP()
                self.rsTab.initRS()
                self.tabWidget.setCurrentIndex(0)
                         
            except Exception as e:
                QMessageBox.warning(self, "사원등록실패", "Error: " + str(e))
                return                        
                
    # 231201 사번에 맞춰 입사일 디폴트값 세팅 by 정현아
    def setJoinDate(self):
        year_str = "20"  + self.empNum_lineEdit.text()[:2]
        year = int(year_str)
        
        date = QDate(year, 1, 1)        
        self.dateEdit.setDate(date)
        
    # 231204 주민번호 뒷자리에 맞춰서 여자일 경우 무관 세팅 by 정현아
    def setMilitary(self):
        if self.regnum_lineEdit2.text() == '':
            return
        gender = self.regnum_lineEdit2.text()[0]
        if int(gender) % 2 == 0:
            self.military_btn3.setChecked(True)
        else:
            self.military_btn.setChecked(True)
    
    # 231123 이미지 등록화면 전환 및 버튼이벤트 등록 함수 by 정현아    
    def showAddImg(self):
        self.w = AddImg()
        self.w.show()
        self.w.searchbutton.clicked.connect(self.openImage)
        self.w.savebtn.clicked.connect(self.save_img)
        self.w.cnlBtn.clicked.connect(self.w.close)
    
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
                self.w.imgPath_textEdit.setText(self.path)
                self.w.hide()
                self.w.show()

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
                self.img_label.setPixmap(resize_pixmap)
        self.w.close()

    # 231206 우편번호 찾기 팝업창 생성 by 정현아
    def searchPost(self):
        self.w = QDialog(self)
        searchPost = uic.loadUi(resource_path('search_post.ui'), self.w)
        self.w.address_lineEdit.returnPressed.connect(self.findAddress)
        self.w.searchBtn.clicked.connect(self.findAddress)
        self.w.table.cellDoubleClicked.connect(self.selectPost)
        
        self.w.saveBtn.clicked.connect(self.acceptDialogResult)
        self.w.cnlBtn.clicked.connect(self.w.close)
        
        if self.w.exec_() == QDialog.Accepted:
            pass
        
    # 231206 우편번호 찾기 후 찾은 내용 라인에디터에 세팅 by 정현아
    def acceptDialogResult(self):
        self.w.setResult(QDialog.Accepted)
        self.addressNum_lineEdit.setText(self.post_num)
        self.addre_lineEdit.setText(self.post_address)    
        self.w.close()
        
    # 231206 오픈 API를 통해 우편번호 찾기 by 정현아
    def findAddress(self):
        post_num = []
        post_address = []
        self.w.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
        self.w.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)

        address = self.w.address_lineEdit.text()
        # 도로명 주소로 검색하고 도로명 주소 결과가 없으면 지번 주소로 다시 검색 by 정현아
        url = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd'
        params = {
            'serviceKey': '7kEsxVN9P4SCOTTBAmWPvKJQDrhW4i08XbJe98mkPpthjKeB6bQjiDMSEJuNHVroSg3sx8OUYLaeSIe1J1tSsw==',
            'searchSe': 'road',
            'srchwrd': '',
            'countPerPage': '50',
            'currentPage': '1'
        }
        params['srchwrd'] = address

        response = requests.get(url, params=params).text.encode('utf-8')
        xmlobj = BeautifulSoup(response, 'lxml-xml')

        post = xmlobj.find_all('zipNo')
        post2 = xmlobj.find_all('lnmAdres')
        row = len(post)

        if(row != 0):
            self.w.table.setRowCount(row)
            for p in post:
                post_num.append(p.getText())
            for p in post2 :
                post_address.append(p.getText())
            for r in range(row):
                self.w.table.setItem(r, 0, QTableWidgetItem(str(post_num[r])))
                self.w.table.setItem(r, 1, QTableWidgetItem(str(post_address[r])))
        else:
            params['searchSe'] = 'dong'
            response = requests.get(url, params=params).text.encode('utf-8')
            xmlobj = BeautifulSoup(response, 'lxml-xml')

            post = xmlobj.find_all('zipNo')
            post2 = xmlobj.find_all('lnmAdres')
            row = len(post)

            if(row != 0):
                self.w.table.setRowCount(row)
                for p in post:
                    post_num.append(p.getText())
                for p in post2 :
                    post_address.append(p.getText())
                for r in range(row):
                    self.w.table.setItem(r, 0, QTableWidgetItem(str(post_num[r])))
                    self.w.table.setItem(r, 1, QTableWidgetItem(str(post_address[r])))
                    
    # 231206 목록에서 찾은 우편번호 및 주소 라인에디트에 세팅 by 정현아
    def selectPost(self, row, col):
        self.post_num = self.w.table.item(row, 0).text() 
        self.post_address = self.w.table.item(row, 1).text()
        self.w.address_lineEdit.setText(self.post_num + " " + self.post_address)

    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Regist() 
    myWindow.show() 
    app.exec_() 