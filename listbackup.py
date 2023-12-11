import os
import sys
import pymysql
import re

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from emp_regist import Regist
from emp_info import EmpInfo
from add_img import AddImg

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('emp_list11.ui')
form_class = uic.loadUiType(form)[0]

class FamilyTab(QWidget):
    def __init__(self, emp_num, type):
        super(FamilyTab, self).__init__()
        self.cnt = 0
        self.emp_num = emp_num
        self.type = type
        self.initUI()

    def initUI(self):
        self.family = QScrollArea()
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
        if self.type == 'info':
            self.addFamilyMember()
        else: 
            self.fAdd_btn = QPushButton("추가")
            self.editFamilyMember()
            self.fAdd_btn.clicked.connect(self.editFamilyMember)

    def addFamilyMember(self):
        result = self.setData(self.emp_num)
        if not result :
            return
        else :
            self.cnt =len(result)
        
        #데이터 세팅
        for i in range(self.cnt):
            self.fName_lbl.append(QLabel("성명:"))
            self.fName_le.append(QLabel(result[i][0]))
            self.fYear_lbl.append(QLabel("생년월일:"))
            self.fYear_de.append(QLabel(str(result[i][1])))
            self.fRel_lbl.append(QLabel("관계:"))
            self.fRel_cb.append(QLabel(result[i][2]))
            self.fLive_lbl.append(QLabel("동거여부:"))
            self.fLive_cb.append(QLabel(result[i][3]))

        for j in range(self.cnt):
            for i in range(len(self.familyWidget)):
                if i == 0:
                    self.flay.addWidget(self.familyWidget[i][j],0 + 4 * j,0)
                elif i % 2 == 0:
                    self.flay.addWidget(self.familyWidget[i][j],int(i/2) + 4 * j,0)
                elif i % 2 == 1:
                    self.flay.addWidget(self.familyWidget[i][j],int(i/2) + 4 * j,1)
        
        self.flay.setRowStretch(self.flay.rowCount(), 1)
        rightmost_column_index = len(self.familyWidget) - 1
        self.flay.setColumnStretch(rightmost_column_index, 1)

    def editFamilyMember(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result:
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
                
                self.flay.setRowStretch(self.flay.rowCount(), 1)
                self.cnt+=1;
            else:
                QMessageBox.information(self,"경고","5번 이상 등록하실 수 없습니다.")
        # 231205 있을 경우 등록된 데이터를 각 에디터에 세팅 by 정현아
        else :
            if(len(result) + self.cnt<=5):            
                #데이터 세팅
                if self.cnt == 0:
                    for i in range(len(result)):
                        self.fName_lbl.append(QLabel("성명:"))
                        self.fName_le.append(QLineEdit(result[i][0]))
                        self.fYear_lbl.append(QLabel("생년월일:"))
                        self.fYear_de.append(QDateEdit(QDate.fromString(result[i][1].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.fRel_lbl.append(QLabel("관계:"))
                        self.fRel_cb.append(QComboBox())
                        self.f_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
                        for j in range(len(self.f_list)):
                            self.fRel_cb[i].addItem(self.f_list[j])
                        self.fRel_cb[i].setCurrentText(result[i][2])
                        self.fLive_lbl.append(QLabel("동거여부:"))
                        self.fLive_cb.append(QComboBox())
                        self.fLive_cb[i].addItems(['Y', 'N'])
                        self.fLive_cb[i].setCurrentText(result[i][3])
                elif self.cnt != 0:
                    self.fName_lbl.append(QLabel("가족성명"))
                    self.fName_le.append(QLineEdit())
                    self.fYear_lbl.append(QLabel("생년월일"))
                    self.fYear_de.append(QDateEdit())
                    self.fRel_lbl.append(QLabel("관계"))
                    self.fRel_cb.append(QComboBox())
                    self.f_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
                    for i in range(len(self.f_list)):
                        self.fRel_cb[self.cnt+len(result)-1].addItem(self.f_list[i])
                    self.fLive_lbl.append(QLabel("동거여부"))
                    self.fLive_cb.append(QComboBox())
                    self.fLive_cb[self.cnt+len(result)-1].addItem('Y')
                    self.fLive_cb[self.cnt+len(result)-1].addItem('N')
                    
                for j in range(len(result)+self.cnt):
                    for i in range(len(self.familyWidget)):
                        if i == 0:
                            self.flay.addWidget(self.familyWidget[i][j],0 + 4 * j,0)
                        elif i % 2 == 0:
                            self.flay.addWidget(self.familyWidget[i][j],int(i/2) + 4 * j,0)
                        elif i % 2 == 1:
                            self.flay.addWidget(self.familyWidget[i][j],int(i/2) + 4 * j,1)
                            if i % 4 == 3:
                                self.flay.addWidget(self.fAdd_btn,int(i/2) + 4 * j,2)
                
                self.flay.setRowStretch(self.flay.rowCount(), 1)
                self.cnt+=1
            else:
                QMessageBox.information(self,"경고","5번 이상 등록하실 수 없습니다.")
            
    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT NAME_FAMILY, BIRTH, REL, LIVE FROM FAMILY WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    # 231205 변경된 데이터 저장, 기존에 등록된 정보가 있을 경우 UPDATE, 없으면 INSERT
    def saveFamily(self, emp_num, cur, conn):
        result = self.setData(self.emp_num)
        row = len(result)
        if result:
            for i in range(row):
                if self.fName_le[i].text() == '':
                    return
                fName = self.fName_le[i].text()
                fYear = self.fYear_de[i].date().toString("yyyy-MM-dd")
                birth = self.fYear_de[i].date()
                age = int(birth.daysTo(QDate.currentDate())/365)
                fRel = self.fRel_cb[i].currentText()
                fLive = self.fLive_cb[i].currentText()
                
                query = "UPDATE FAMILY SET NAME_FAMILY = %s, BIRTH = %s, AGE = %s, REL = %s, LIVE = %s WHERE EMP_NUM = %s AND NAME_FAMILY = %s;"
                cur.execute(query, (fName, fYear, age, fRel, fLive, emp_num, fName,))
                conn.commit()  
            self.cnt -=1
            
        for i in range(self.cnt):
            if self.fName_le[i+row].text() == '':
                return
            fName = self.fName_le[i+row].text()
            fYear = self.fYear_de[i+row].date().toString("yyyy-MM-dd")
            birth = self.fYear_de[i+row].date()
            age = int(birth.daysTo(QDate.currentDate())/365)
            fRel = self.fRel_cb[i+row].currentText()
            fLive = self.fLive_cb[i+row].currentText()
            
            query = "INSERT INTO FAMILY VALUES(%s, %s, %s, %s, %s, %s)"
            cur.execute(query, (emp_num, fName, fYear, age, fRel, fLive))
            conn.commit()  
    
class ContactTab(QWidget):
    def __init__(self, emp_num, type):
        super(ContactTab, self).__init__()
        self.cnt = 0
        self.emp_num = emp_num
        self.type = type
        self.initUI()

    def initUI(self):
        self.contact = QScrollArea()
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
        
        if self.type =='info':
            self.addContact()
        else:
            self.cAdd_btn = QPushButton("추가")
            self.editContact()
            self.cAdd_btn.clicked.connect(self.editContact)

    def addContact(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.cName_lbl.append(QLabel("성명:"))
            self.cName_le.append(QLabel(result[i][0]))
            self.cRel_lbl.append(QLabel("관계:"))
            self.cRel_cb.append(QLabel(result[i][1]))
            self.cCont_lbl.append(QLabel("연락처:"))
            self.cCont_le.append(QLabel(result[i][2]))

        for j in range(self.cnt):
            for i in range(len(self.contactWidget)):
                if i % 2 == 0:
                    self.clay.addWidget(self.contactWidget[i][j], int(i/2) + 3 * j, 0)
                elif i % 2 == 1:
                    self.clay.addWidget(self.contactWidget[i][j], int(i/2) + 3 * j, 1)

        self.clay.setRowStretch(self.clay.rowCount(), 1)
        rightmost_column_index = len(self.contactWidget) - 1
        self.clay.setColumnStretch(rightmost_column_index, 1)

    def editContact(self):
        result = self.setData(self.emp_num)
        if not result:
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
                    
                self.clay.setRowStretch(self.clay.rowCount(), 1)
                self.cnt+=1
                
            else:
                QMessageBox.information(self,"경고","2번 이상 등록하실 수 없습니다.")
        else:
            if(len(result) + self.cnt <= 2):            
                # 데이터 세팅
                if self.cnt == 0:
                    for i in range(len(result)):
                        self.cName_lbl.append(QLabel("성명"))
                        self.cName_le.append(QLineEdit(result[i][0]))
                        self.cRel_lbl.append(QLabel("관계"))
                        self.cRel_cb.append(QComboBox())
                        self.c_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
                        for j in range(len(self.c_list)):
                            self.cRel_cb[i].addItem(self.c_list[j])
                        self.cRel_cb[i].setCurrentText(result[i][1])
                        self.cCont_lbl.append(QLabel("연락처"))
                        self.cCont_le.append(QLineEdit(result[i][2]))
                        
                elif self.cnt != 0:
                    self.cName_lbl.append(QLabel("성명"))
                    self.cName_le.append(QLineEdit())
                    self.cRel_lbl.append(QLabel("관계"))
                    self.cRel_cb.append(QComboBox())
                    self.c_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
                    for i in range(len(self.c_list)):
                        self.cRel_cb[self.cnt + len(result) - 1].addItem(self.c_list[i])
                    self.cCont_lbl.append(QLabel("연락처"))
                    self.cCont_le.append(QLineEdit())
                    
                for j in range(len(result) + self.cnt):
                    for i in range(len(self.contactWidget)):
                        if i == 0:
                            self.clay.addWidget(self.contactWidget[i][j],0 + 3 * j,0)
                        elif i % 2 == 0:
                            self.clay.addWidget(self.contactWidget[i][j],int(i/2) + 3 * j,0)
                        elif i % 2 == 1:
                            self.clay.addWidget(self.contactWidget[i][j],int(i/2) + 3 * j,1)
                            if i % 3 == 2:
                                self.clay.addWidget(self.cAdd_btn,int(i/2) + 3 * j,2)
                
                for i in range(self.cnt+1):
                    self.cCont_le[i].setValidator(QIntValidator())
                    self.cCont_le[i].setMaxLength(11)
                
                self.clay.setRowStretch(self.clay.rowCount(), 1)
                self.cnt += 1
                
            else:
                QMessageBox.information(self, "경고", "2번 이상 등록하실 수 없습니다.")
            
            
    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT NAME, REL, PHONE FROM CONTACT WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveContact(self, emp_num, cur, conn):
        result = self.setData(self.emp_num)
        row = len(result)

        if result:
            for i in range(row):
                if self.cName_le[i].text() == '':
                    return

                cName = self.cName_le[i].text()
                cRel = self.cRel_cb[i].currentText()
                cCont = self.cCont_le[i].text()

                query = "UPDATE CONTACT SET NAME = %s, REL = %s, PHONE = %s WHERE EMP_NUM = %s AND NAME = %s;"
                cur.execute(query, (cName, cRel, cCont, emp_num, cName,))
                conn.commit()

            self.cnt -= 1

        for i in range(self.cnt):
            if self.cName_le[i + row].text() == '':
                return

            cName = self.cName_le[i + row].text()
            cRel = self.cRel_cb[i + row].currentText()
            cCont = self.cCont_le[i + row].text()

            query = "INSERT INTO CONTACT VALUES(%s, %s, %s, %s)"
            cur.execute(query, (emp_num, cName, cRel, cCont))
            conn.commit()
    
class SchoolTab(QWidget):
    def __init__(self, emp_num, type):
        super(SchoolTab, self).__init__()
        self.cnt = 0
        self.emp_num = emp_num
        self.type = type
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
        if self.type == 'info':
            self.addSchoolInfo()
        else:    
            self.schAdd_btn = QPushButton("추가")
            self.editSchool()
            self.schAdd_btn.clicked.connect(self.editSchool)

    def addSchoolInfo(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.scheadmit_lbl.append(QLabel("입학일:"))
            self.scheadmit_de.append(QLabel(str(result[i][0])))
            self.schgrad_lbl.append(QLabel("졸업일:"))
            self.schgrad_de.append(QLabel(str(result[i][1])))
            self.schname_lbl.append(QLabel("학교명:"))
            self.schname_le.append(QLabel(result[i][2]))
            self.schloc_lbl.append(QLabel("소재지:"))
            self.schloc_le.append(QLabel(result[i][3]))
            self.schmajor_lbl.append(QLabel("전공:"))
            self.schmajor_le.append(QLabel(result[i][4]))
            self.schsubmajor_lbl.append(QLabel("복수전공:"))
            self.schsubmajor_le.append(QLabel(result[i][5]))
            self.comment_lbl.append(QLabel("특기사항:"))
            self.comment_le.append(QLabel(result[i][6]))

        for j in range(self.cnt):
            for i in range(len(self.schWidget)):
                if i % 2 == 0:
                    self.schlay.addWidget(self.schWidget[i][j], int(i / 2) + 7 * j, 0)
                elif i % 2 == 1:
                    self.schlay.addWidget(self.schWidget[i][j], int(i / 2) + 7 * j, 1)

        self.schlay.setRowStretch(self.schlay.rowCount(), 1)
        rightmost_column_index = len(self.schWidget) - 1
        self.schlay.setColumnStretch(rightmost_column_index, 1)
 
    def editSchool(self):
        result = self.setData(self.emp_num)
        if not result:
            if self.cnt <= 3:
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
                        self.schlay.addWidget(self.schWidget[i][self.cnt], 0 + 7 * self.cnt, 0)
                    elif i % 2 == 0:
                        self.schlay.addWidget(self.schWidget[i][self.cnt], int(i / 2) + 7 * self.cnt, 0)
                    elif i % 2 == 1:
                        self.schlay.addWidget(self.schWidget[i][self.cnt], int(i / 2) + 7 * self.cnt, 1)
                        if i % 7 == 6:
                            self.schlay.addWidget(self.schAdd_btn, int(i / 2) + 7 * self.cnt, 2)

                self.schlay.setRowStretch(self.schlay.rowCount(), 1)
                self.cnt += 1

            else:
                QMessageBox.information(self, "경고", "4번 이상 등록하실 수 없습니다.")
        else:
            if len(result) + self.cnt <= 4:
                # 데이터 세팅
                if self.cnt == 0:
                    for i in range(len(result)):
                        self.scheadmit_lbl.append(QLabel("입학일:"))
                        self.scheadmit_de.append(QDateEdit(QDate.fromString(result[i][0].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.schgrad_lbl.append(QLabel("졸업일:"))
                        self.schgrad_de.append(QDateEdit(QDate.fromString(result[i][1].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.schname_lbl.append(QLabel("학교명:"))
                        self.schname_le.append(QLineEdit(result[i][2]))
                        self.schloc_lbl.append(QLabel("소재지:"))
                        self.schloc_le.append(QLineEdit(result[i][3]))
                        self.schmajor_lbl.append(QLabel("전공:"))
                        self.schmajor_le.append(QLineEdit(result[i][4]))
                        self.schsubmajor_lbl.append(QLabel("복수전공:"))
                        self.schsubmajor_le.append(QLineEdit(result[i][5]))
                        self.comment_lbl.append(QLabel("특기사항:"))
                        self.comment_le.append(QLineEdit(result[i][6]))

                elif self.cnt != 0:
                    self.scheadmit_lbl.append(QLabel("입학일"))
                    self.scheadmit_de.append(QDateEdit(self))
                    self.schgrad_lbl.append(QLabel("졸업일"))
                    self.schgrad_de.append(QDateEdit(self))
                    self.schname_lbl.append(QLabel("학교명"))
                    self.schname_le.append(QLineEdit())
                    self.schloc_lbl.append(QLabel("소재지"))
                    self.schloc_le.append(QLineEdit())
                    self.schmajor_lbl.append(QLabel("전공"))
                    self.schmajor_le.append(QLineEdit())
                    self.schsubmajor_lbl.append(QLabel("복수전공"))
                    self.schsubmajor_le.append(QLineEdit())
                    self.comment_lbl.append(QLabel("특기사항"))
                    self.comment_le.append(QLineEdit())

                for j in range(len(result) + self.cnt):
                    for i in range(len(self.schWidget)):
                        if i == 0:
                            self.schlay.addWidget(self.schWidget[i][j], 0 + 7 * j, 0)
                        elif i % 2 == 0:
                            self.schlay.addWidget(self.schWidget[i][j], int(i / 2) + 7 * j, 0)
                        elif i % 2 == 1:
                            self.schlay.addWidget(self.schWidget[i][j], int(i / 2) + 7 * j, 1)
                            if i % 7 == 6:
                                self.schlay.addWidget(self.schAdd_btn, int(i / 2) + 7 * j, 2)

                self.schlay.setRowStretch(self.schlay.rowCount(), 1)
                self.cnt += 1

            else:
                QMessageBox.information(self, "경고", "4번 이상 등록하실 수 없습니다.")

    def updateSchoolLayout(self):
        # Add the widgets to the layout similar to addSchoolInfo
        for j in range(self.cnt):
            for i in range(len(self.schWidget)):
                if i % 2 == 0:
                    self.schlay.addWidget(self.schWidget[i][j], int(i / 2) + 7 * j, 0)
                elif i % 2 == 1:
                    self.schlay.addWidget(self.schWidget[i][j], int(i / 2) + 7 * j, 1)

        self.schlay.setRowStretch(self.schlay.rowCount(), 1)
        rightmost_column_index = len(self.schWidget) - 1
        self.schlay.setColumnStretch(rightmost_column_index, 1)       

    
    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT DATE_ADMITION, DATE_GRADUATE, NAME_SCHOOL, LOCATION, MAJOR, SUB_MAJOR, COMMENT FROM SCHOOL_EDUCATION WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveSchool(self, emp_num, cur, conn):
        result = self.setData(emp_num)
        row = len(result)

        if result:
            for i in range(row):
                if self.schname_le[i].text() == '':
                    return

                sAdmit = self.scheadmit_de[i].date().toString("yyyy-MM-dd")
                sGrad = self.schgrad_de[i].date().toString("yyyy-MM-dd")
                sName = self.schname_le[i].text()
                sLoc = self.schloc_le[i].text()
                sMajor = self.schmajor_le[i].text()
                sSubMajor = self.schsubmajor_le[i].text()
                sComment = self.comment_le[i].text()

                query = "UPDATE SCHOOL_EDUCATION SET DATE_ADMITION = %s, DATE_GRADUATE = %s, NAME_SCHOOL = %s, LOCATION = %s, MAJOR = %s, SUB_MAJOR = %s, COMMENT = %s WHERE EMP_NUM = %s AND NAME_SCHOOL = %s;"
                cur.execute(query, (sAdmit, sGrad, sName, sLoc, sMajor, sSubMajor, sComment, emp_num, sName,))
                conn.commit()

            self.cnt -= 1

        for i in range(self.cnt):
            if self.schname_le[i + row].text() == '':
                return

            sAdmit = self.scheadmit_de[i + row].date().toString("yyyy-MM-dd")
            sGrad = self.schgrad_de[i + row].date().toString("yyyy-MM-dd")
            sName = self.schname_le[i + row].text()
            sLoc = self.schloc_le[i + row].text()
            sMajor = self.schmajor_le[i + row].text()
            sSubMajor = self.schsubmajor_le[i + row].text()
            sComment = self.comment_le[i + row].text()

            query = "INSERT INTO SCHOOL_EDUCATION VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (emp_num, sAdmit, sGrad, sName, sLoc, sMajor, sSubMajor, sComment))
            conn.commit()
    
class CertificationTab(QWidget):
    def __init__(self, emp_num, type):
        super(CertificationTab, self).__init__()
        self.cnt = 0
        self.type = type
        self.emp_num = emp_num
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
        
        if self.type == 'info':
            self.addCertification()
        else:
            self.certAdd_btn = QPushButton("추가")   
            self.editCertification()
            self.certAdd_btn.clicked.connect(self.editCertification)

    def addCertification(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        for i in range(self.cnt):
            self.certName_lbl.append(QLabel("자격증명:"))
            self.certName_le.append(QLabel(result[i][0]))

            self.certDate_lbl.append(QLabel("취득일:"))
            self.certDate_de.append(QLabel(str(result[i][1])))

        for j in range(self.cnt):
            for i in range(len(self.certwidget)):
                if i % 2 == 0:
                    self.certlay.addWidget(self.certwidget[i][j], int(i/2) + 2 * j, 0)
                elif i % 2 == 1:
                    self.certlay.addWidget(self.certwidget[i][j], int(i/2) + 2 * j, 1)

        self.certlay.setRowStretch(self.certlay.rowCount(), 1)
        rightmost_column_index = len(self.certwidget) - 1
        self.certlay.setColumnStretch(rightmost_column_index, 1)
        
    def editCertification(self):
        result = self.setData(self.emp_num)
        if not result :
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
                
                self.certlay.setRowStretch(self.certlay.rowCount(), 1)
                self.cnt+=1
            else:
                QMessageBox.information(self, "경고", "10번 이상 등록하실 수 없습니다.")
        else:
            if len(result) + self.cnt <= 9:
                # 데이터 세팅
                if self.cnt == 0:
                    for i in range(len(result)):
                        self.certName_lbl.append(QLabel("자격증명"))
                        self.certName_le.append(QLineEdit(result[i][0]))
                        self.certDate_lbl.append(QLabel("취득일"))
                        self.certDate_de.append(QDateEdit(QDate.fromString(result[i][1].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                elif self.cnt != 0:
                    self.certName_lbl.append(QLabel("자격증명"))
                    self.certName_le.append(QLineEdit())
                    self.certDate_lbl.append(QLabel("취득일"))
                    self.certDate_de.append(QDateEdit())

                for j in range(len(result) + self.cnt):
                    for i in range(len(self.certwidget)):
                        if i == 0:
                            self.certlay.addWidget(self.certwidget[i][j], 0 + 2 * j, 0)
                        elif i % 2 == 0:
                            self.certlay.addWidget(self.certwidget[i][j], int(i / 2) + 2 * j, 0)
                        elif i % 2 == 1:
                            self.certlay.addWidget(self.certwidget[i][j], int(i / 2) + 2 * j, 1)
                            self.certlay.addWidget(self.certAdd_btn, int(i / 2) + 2 * j, 2)

                self.certlay.setRowStretch(self.certlay.rowCount(), 1)
                self.cnt += 1
            else:
                QMessageBox.information(self, "경고", "10번 이상 등록하실 수 없습니다.")

    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT NAME_LICENSE, DATE_ACQUI FROM CERTIFICATE WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveCertification(self, emp_num, cur, conn):
        result = self.setData(emp_num)
        row = len(result)

        if result:
            for i in range(row):
                if self.certName_le[i].text() == '':
                    return

                certName = self.certName_le[i].text()
                certDate = self.certDate_de[i].date().toString("yyyy-MM-dd")

                query = "UPDATE CERTIFICATE SET NAME_LICENSE = %s, DATE_ACQUI = %s WHERE EMP_NUM = %s AND NAME_LICENSE = %s;"
                cur.execute(query, (certName, certDate, emp_num, certName))
                conn.commit()

            self.cnt -= 1

        for i in range(self.cnt):
            if self.certName_le[i + row].text() == '':
                return

            certName = self.certName_le[i + row].text()
            certDate = self.certDate_de[i + row].date().toString("yyyy-MM-dd")

            query = "INSERT INTO CERTIFICATE VALUES(%s, %s, %s)"
            cur.execute(query, (emp_num, certName, certDate))
            conn.commit()

class CareerTab(QWidget):
    def __init__(self, emp_num, type):
        super(CareerTab, self).__init__()
        self.cnt = 0
        self.emp_num = emp_num
        self.type = type
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

        if self.type == 'info':
            self.addCareerInfo()
        else: 
            self.carAdd_btn = QPushButton("추가")
            self.editCareerInfo()
            self.carAdd_btn.clicked.connect(self.editCareerInfo)

    def addCareerInfo(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.company_lbl.append(QLabel("근무회사:"))
            self.company_le.append(QLabel(result[i][0]))
            self.dept_lbl.append(QLabel("근무부서:"))
            self.dept_le.append(QLabel(result[i][1]))
            self.datejoin_lbl.append(QLabel("입사일:"))
            self.datejoin_de.append(QLabel(str(result[i][2])))
            self.dateleave_lbl.append(QLabel("퇴사일:"))
            self.dateleave_de.append(QLabel(str(result[i][3])))
            self.finalrank_lbl.append(QLabel("최종 직급:"))
            self.finalrank_le.append(QLabel(result[i][4]))
            self.workinfo_lbl.append(QLabel("근무 내용:"))
            self.workinfo_le.append(QLabel(result[i][5]))

        for j in range(self.cnt):
            for i in range(len(self.carWidget)):
                if i % 2 == 0:
                    self.carlay.addWidget(self.carWidget[i][j], int(i/2) + 6 * j, 0)
                elif i % 2 == 1:
                    self.carlay.addWidget(self.carWidget[i][j], int(i/2) + 6 * j, 1)

        self.carlay.setRowStretch(self.carlay.rowCount(), 1)
        rightmost_column_index = len(self.carWidget) - 1
        self.carlay.setColumnStretch(rightmost_column_index, 1)
        
    def editCareerInfo(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result:
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
                
                self.carlay.setRowStretch(self.carlay.rowCount(), 1)
                self.cnt+=1     
            else:
                QMessageBox.information(self, "경고", "10번 이상 등록하실 수 없습니다.")
                
        else:
            if len(result) + self.cnt <= 9:
                print(self.cnt, len(result) + self.cnt)
                # 데이터 세팅
                if self.cnt == 0:
                    for i in range(len(result)):
                        self.company_lbl.append(QLabel("근무회사:"))
                        self.company_le.append(QLineEdit(result[i][0]))
                        self.dept_lbl.append(QLabel("근무부서:"))
                        self.dept_le.append(QLineEdit(result[i][1]))
                        self.datejoin_lbl.append(QLabel("입사일:"))
                        self.datejoin_de.append(QDateEdit(QDate.fromString(result[i][2].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.dateleave_lbl.append(QLabel("퇴사일:"))
                        self.dateleave_de.append(QDateEdit(QDate.fromString(result[i][3].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.finalrank_lbl.append(QLabel("최종 직급:"))
                        self.finalrank_le.append(QLineEdit(result[i][4]))
                        self.workinfo_lbl.append(QLabel("근무 내용:"))
                        self.workinfo_le.append(QLineEdit(result[i][5]))

                elif self.cnt != 0:
                    self.company_lbl.append(QLabel("근무회사"))
                    self.company_le.append(QLineEdit())
                    self.dept_lbl.append(QLabel("근무부서"))
                    self.dept_le.append(QLineEdit())
                    self.datejoin_lbl.append(QLabel("입사일"))
                    self.datejoin_de.append(QDateEdit())
                    self.dateleave_lbl.append(QLabel("퇴사일"))
                    self.dateleave_de.append(QDateEdit())
                    self.finalrank_lbl.append(QLabel("최종직급"))
                    self.finalrank_le.append(QLineEdit())
                    self.workinfo_lbl.append(QLabel("업무내용"))
                    self.workinfo_le.append(QLineEdit())

                for j in range(len(result)+self.cnt):
                    for i in range(len(self.carWidget)):
                        if i == 0:
                            self.carlay.addWidget(self.carWidget[i][j], 0 + 6 * j, 0)
                        elif i % 2 == 0:
                            self.carlay.addWidget(self.carWidget[i][j], int(i / 2) + 6 * j, 0)
                        elif i % 2 == 1:
                            self.carlay.addWidget(self.carWidget[i][j], int(i / 2) + 6 * j, 1)
                            if i % 6 == 5:
                                self.carlay.addWidget(self.carAdd_btn, int(i / 2) + 6 * j, 2)

                self.carlay.setRowStretch(self.carlay.rowCount(), 1)
                self.cnt += 1
            else:
                QMessageBox.information(self, "경고", "10번 이상 등록하실 수 없습니다.")
                
    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT COMPANY, DEPARTMENT, DATE_JOIN, DATE_LEAVE, FINAL_RANK, WORK_INFO FROM CAREER WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveCareer(self, emp_num, cur, conn):
        result = self.setData(emp_num)
        row = len(result)
        if result:
            for i in range(row):
                if self.company_le[i].text() == '':
                    return
                company = self.company_le[i].text()
                dept = self.dept_le[i].text()
                datejoin = self.datejoin_de[i].date().toString("yyyy-MM-dd")
                dateleave = self.dateleave_de[i].date().toString("yyyy-MM-dd")
                workdays = self.datejoin_de[i].date().daysTo(self.dateleave_de[i].date())
                years, months = divmod(workdays, 365)
                months = months/30.44/12
                workperiod = round(years + months, 1)
                finalrank = self.finalrank_le[i].text()
                workinfo = self.workinfo_le[i].text()

                query = """
                    UPDATE CAREER
                    SET COMPANY = %s, DEPARTMENT = %s, DATE_JOIN = %s, DATE_LEAVE = %s, WORK_PERIOD = %s, FINAL_RANK = %s, WORK_INFO = %s
                    WHERE EMP_NUM = %s AND COMPANY = %s;
                """
                values = (company, dept, datejoin, dateleave, workperiod, finalrank, workinfo, emp_num, company)
                cur.execute(query, values)
                conn.commit()
            self.cnt -= 1

        for i in range(self.cnt):
            if self.company_le[i+row].text() == '':
                return
            company = self.company_le[i+row].text()
            dept = self.dept_le[i+row].text()
            date_join = self.datejoin_de[i+row].date().toString("yyyy-MM-dd")
            date_leave = self.dateleave_de[i+row].date().toString("yyyy-MM-dd")
            workdays = self.datejoin_de[i+row].date().daysTo(self.dateleave_de[i+row].date())
            years, months = divmod(workdays, 365)
            months = months/30.44/12
            workperiod = round(years + months, 1)
            final_rank = self.finalrank_le[i+row].text()
            work_info = self.workinfo_le[i+row].text()

            query = """
                INSERT INTO CAREER (EMP_NUM, COMPANY, DEPARTMENT, DATE_JOIN, DATE_LEAVE, WORK_PERIOD, FINAL_RANK, WORK_INFO)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            values = (emp_num, company, dept, date_join, date_leave, workperiod, final_rank, work_info)
            cur.execute(query, values)
            conn.commit()
    
class TechnicalTab(QWidget):
    def __init__(self, emp_num, type):
        super(TechnicalTab, self).__init__()
        self.cnt = 0
        self.emp_num = emp_num
        self.type = type
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
        
        if self.type == 'info':
            self.addTechMember()
        else:
            self.techAdd_btn = QPushButton("추가")
            self.editTechMember()
            self.techAdd_btn.clicked.connect(self.editTechMember)

    def addTechMember(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.techDet_lbl.append(QLabel("기술사항:"))
            self.techDet_le.append(QLabel(result[i][0]))
            self.pro_lbl.append(QLabel("숙련도:"))
            self.pro_cb.append(QLabel(result[i][1]))
            self.note_lbl.append(QLabel("비고:"))
            self.note_le.append(QLabel(result[i][2]))

        for j in range(self.cnt):
            for i in range(len(self.techWidget)):
                if i % 2 == 0:
                    self.techlay.addWidget(self.techWidget[i][j], int(i/2) + 3 * j, 0)
                elif i % 2 == 1:
                    self.techlay.addWidget(self.techWidget[i][j], int(i/2) + 3 * j, 1)

        self.techlay.setRowStretch(self.techlay.rowCount(), 1)
        rightmost_column_index = len(self.techWidget) - 1
        self.techlay.setColumnStretch(rightmost_column_index, 1)
        
    def editTechMember(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result:
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
        else : 
            if len(result) + self.cnt <= 9:
                if self.cnt == 0:
                    for i in range(len(result)):
                        self.techDet_lbl.append(QLabel("기술사항:"))
                        self.techDet_le.append(QLineEdit(result[i][0]))
                        self.pro_lbl.append(QLabel("숙련도:"))
                        self.pro_cb.append(QComboBox())
                        self.pro_cb[i].addItem('상')
                        self.pro_cb[i].addItem('중')
                        self.pro_cb[i].addItem('하')
                        self.pro_cb[i].setCurrentText(result[i][1])
                        self.note_lbl.append(QLabel("비고:"))
                        self.note_le.append(QLineEdit(result[i][2]))

                elif self.cnt != 0:
                    self.techDet_lbl.append(QLabel("기술사항"))
                    self.techDet_le.append(QLineEdit())
                    self.pro_lbl.append(QLabel("숙련도"))
                    self.pro_cb.append(QComboBox())
                    self.pro_cb[self.cnt+len(result)-1].addItem('상')
                    self.pro_cb[self.cnt+len(result)-1].addItem('중')
                    self.pro_cb[self.cnt+len(result)-1].addItem('하')
                    self.note_lbl.append(QLabel("비고"))
                    self.note_le.append(QLineEdit())

                for j in range(len(result) + self.cnt):
                    for i in range(len(self.techWidget)):
                        if i == 0:
                            self.techlay.addWidget(self.techWidget[i][j], 0 + 3 * j, 0)
                        elif i % 2 == 0:
                            self.techlay.addWidget(self.techWidget[i][j], int(i / 2) + 3 * j, 0)
                        elif i % 2 == 1:
                            self.techlay.addWidget(self.techWidget[i][j], int(i / 2) + 3 * j, 1)
                            if i % 3 == 2:
                                self.techlay.addWidget(self.techAdd_btn, int(i / 2) + 3 * j, 2)

                self.techlay.setRowStretch(self.techlay.rowCount(), 1)
                self.cnt += 1
            else:
                QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")
        

    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT TEC_DETAIL, PROFICIENCY,NOTE FROM TECHNICAL WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveTechnical(self, emp_num, cur, conn):
        result = self.setData(emp_num)
        row = len(result)
        if result:
            for i in range(self.cnt):
                if self.techDet_le[i].text() == '':
                    return

                techDet = self.techDet_le[i].text()
                proficiency = self.pro_cb[i].currentText()
                note = self.note_le[i].text()

                if result:
                    # Update existing data
                    query = "UPDATE TECHNICAL SET TEC_DETAIL = %s, PROFICIENCY = %s, NOTE = %s WHERE EMP_NUM = %s AND TEC_DETAIL = %s;"
                    cur.execute(query, (techDet, proficiency, note, emp_num, techDet))
                    conn.commit()
                else:
                    # Insert new data
                    query = "INSERT INTO TECHNICAL (EMP_NUM, TEC_DETAIL, PROFICIENCY, NOTE) VALUES (%s, %s, %s, %s);"
                    cur.execute(query, (emp_num, techDet, proficiency, note))
                    conn.commit()
            
            self.cnt -= 1

        for i in range(self.cnt):
            if self.techDet_le[i+row].text() == '':
                return

            techDet = self.techDet_le[i+row].text()
            proficiency = self.pro_cb[i+row].currentText()
            note = self.note_le[i+row].text()

            # Insert new data
            query = "INSERT INTO TECHNICAL (EMP_NUM, TEC_DETAIL, PROFICIENCY, NOTE) VALUES (%s, %s, %s, %s);"
            cur.execute(query, (emp_num, techDet, proficiency, note))
            conn.commit()
    
class RPTab(QWidget):
    def __init__(self, emp_num, type):
        super(RPTab, self).__init__()
        self.emp_num = emp_num
        self.cnt = 0
        self.type = type
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
        if self.type == 'info':
            self.addRPMember()
        else: 
            self.rpAdd_btn = QPushButton("추가")
            self.editRPMember()
            self.rpAdd_btn.clicked.connect(self.editRPMember)            

    def addRPMember(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.rpName_lbl.append(QLabel("상벌명:"))
            self.rpName_le.append(QLabel(result[i][0]))

            self.rpScore_lbl.append(QLabel("점수:"))
            self.rpScore_le.append(QLabel(str(result[i][1])))

            self.rpDate_lbl.append(QLabel("일자:"))
            self.rpDate_de.append(QLabel(str(result[i][2])))

            self.rpNote_lbl.append(QLabel("상벌내용:"))
            self.rpNote_le.append(QLabel(result[i][3]))

        for j in range(self.cnt):
            for i in range(len(self.rpWidget)):
                if i % 2 == 0:
                    self.rplay.addWidget(self.rpWidget[i][j], int(i/2) + 4 * j, 0)
                elif i % 2 == 1:
                    self.rplay.addWidget(self.rpWidget[i][j], int(i/2) + 4 * j, 1)

        self.rplay.setRowStretch(self.rplay.rowCount(), 1)
        rightmost_column_index = len(self.rpWidget) - 1
        self.rplay.setColumnStretch(rightmost_column_index, 1)
        
    def editRPMember(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result:
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
        
        else:
            if(len(result) + self.cnt<=19):            
                #데이터 세팅
                if self.cnt == 0:
                    for i in range(len(result)):
                        self.rpName_lbl.append(QLabel("상벌명:"))
                        self.rpName_le.append(QLineEdit(result[i][0]))

                        self.rpScore_lbl.append(QLabel("점수:"))
                        self.rpScore_le.append(QLineEdit(str(result[i][1])))

                        self.rpDate_lbl.append(QLabel("일자:"))
                        self.rpDate_de.append(QDateEdit(QDate.fromString(result[i][2].strftime("%Y-%m-%d"), "yyyy-MM-dd")))

                        self.rpNote_lbl.append(QLabel("상벌내용:"))
                        self.rpNote_le.append(QLineEdit(result[i][3]))                        
                        
                elif self.cnt != 0:    
                    for i in range(len(result)):
                        self.rpName_lbl.append(QLabel("상벌명"))
                        self.rpName_le.append(QLineEdit())
                        self.rpScore_lbl.append(QLabel("점수"))
                        self.rpScore_le.append(QLineEdit())
                        self.rpDate_lbl.append(QLabel("상벌일"))
                        self.rpDate_de.append(QDateEdit())
                        self.rpNote_lbl.append(QLabel("상벌내용"))
                        self.rpNote_le.append(QLineEdit())        

                for j in range(len(result)+self.cnt):
                    for i in range(len(self.rpWidget)):
                        if i == 0:
                            self.rplay.addWidget(self.rpWidget[i][j], 0 + 4 * j, 0)
                        elif i % 2 == 0:
                            self.rplay.addWidget(self.rpWidget[i][j], int(i / 2) + 4 * j, 0)
                        elif i % 2 == 1:
                            self.rplay.addWidget(self.rpWidget[i][j], int(i / 2) + 4 * j, 1)
                            if i % 4 == 3:
                                self.rplay.addWidget(self.rpAdd_btn, int(i / 2) + 4 * j, 2)
                                
                for i in range(self.cnt+1):
                    self.rpScore_le[i].setValidator(QIntValidator())
                self.rplay.setRowStretch(self.rplay.rowCount(), 1)
                self.cnt+=1
            else:
                QMessageBox.information(self,"경고","20번 이상 등록하실 수 없습니다.")        

    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT NAME_REW_PUNI, SCORE, DATE_REW_PUNI, NOTE PROFICIENCY,NOTE FROM R_P WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveRP(self, emp_num, cur, conn):
        result = self.setData(self.emp_num)
        row = len(result)
        if result:
            for i in range(row):
                if self.rpName_le[i].text() == '':
                    return

            for i in range(row):
                rpName = self.rpName_le[i].text()
                rpScore = int(self.rpScore_le[i].text())
                rpDate = self.rpDate_de[i].date().toString("yyyy-MM-dd")
                rpNote = self.rpNote_le[i].text()

                query = "UPDATE R_P SET NAME_REW_PUNI = %s, SCORE = %s, DATE_REW_PUNI = %s, NOTE = %s WHERE EMP_NUM = %s AND NAME_REW_PUNI = %s;"
                cur.execute(query, (rpName, rpScore, rpDate, rpNote, emp_num, rpName,))
                conn.commit()
            self.cnt -= 1

        for i in range(self.cnt):
            if self.rpName_le[i + row].text() == '':
                return

            rpName = self.rpName_le[i + row].text()
            rpScore = int(self.rpScore_le[i + row].text())
            rpDate = self.rpDate_de[i + row].date().toString("yyyy-MM-dd")
            rpNote = self.rpNote_le[i + row].text()

            query = "INSERT INTO R_P VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query, (emp_num, rpName, rpScore, rpDate, rpNote))
            conn.commit()
    
class RSTab(QWidget):
    def __init__(self, emp_num, type):
        super(RSTab, self).__init__()
        self.cnt = 0
        self.emp_num = emp_num
        self.type = type
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
        if self.type == 'info':
            self.addRSMember()
        else:
            self.rsAdd_btn = QPushButton("추가")
            self.editRSMember()
            self.rsAdd_btn.clicked.connect(self.editRSMember)

    def addRSMember(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.rsRANK_lbl.append(QLabel("직급:"))
            self.rsRANK_le.append(QLabel(result[i][0]))

            self.rsSal_lbl.append(QLabel("호봉:"))
            self.rsSal_le.append(QLabel(str(result[i][1])))

            self.rsDate_lbl.append(QLabel("시작일:"))
            self.rsDate_de.append(QLabel(str(result[i][2])))

        for j in range(self.cnt):
            for i in range(len(self.rsWidget)):
                if i % 2 == 0:
                    self.rslay.addWidget(self.rsWidget[i][j], int(i/2) + 3 * j, 0)
                elif i % 2 == 1:
                    self.rslay.addWidget(self.rsWidget[i][j], int(i/2) + 3 * j, 1)

        self.rslay.setRowStretch(self.rslay.rowCount(), 1)
        rightmost_column_index = len(self.rsWidget) - 1
        self.rslay.setColumnStretch(rightmost_column_index, 1)
        
    def editRSMember(self):
                # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result:
            if(self.cnt<=29):
                self.rsRANK_lbl.append(QLabel("직급"))
                self.rsRANK_le.append(QLineEdit(self))
                self.rsSal_lbl.append(QLabel("호봉"))
                self.rsSal_le.append(QLineEdit(self))
                self.rsDate_lbl.append(QLabel("시작일"))
                self.rsDate_de.append(QDateEdit(self))
                
                for i in range(len(self.rsWidget)):
                    if i == 0:
                        self.rslay.addWidget(self.rsWidget[i][self.cnt],0 + 3 * self.cnt,0)
                    elif i % 2 == 0:
                        self.rslay.addWidget(self.rsWidget[i][self.cnt],int(i/2) + 3 * self.cnt,0)
                    elif i % 2 == 1:
                        self.rslay.addWidget(self.rsWidget[i][self.cnt],int(i/2) + 3 * self.cnt,1)
                        if i % 3 == 2:
                            self.rslay.addWidget(self.rsAdd_btn,int(i/2) + 3 * self.cnt,2)
                
                self.rslay.setRowStretch((self.rslay.rowCount()*(4-self.cnt)),1)
                self.cnt+=1
            else:
                QMessageBox.information(self,"경고","30번 이상 등록하실 수 없습니다.")
        # 231205 있을 경우 등록된 데이터를 각 에디터에 세팅 by 정현아
        else :
            if(len(result) + self.cnt<=29):            
                #데이터 세팅
                if self.cnt == 0:
                    for i in range(len(result)):
                        self.rsRANK_lbl.append(QLabel("직급:"))
                        self.rsRANK_le.append(QLineEdit(result[i][0]))

                        self.rsSal_lbl.append(QLabel("호봉:"))
                        self.rsSal_le.append(QLineEdit(str(result[i][1])))

                        self.rsDate_lbl.append(QLabel("시작일:"))
                        self.rsDate_de.append(QDateEdit(QDate.fromString(result[i][2].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                
                elif self.cnt != 0:
                    self.rsRANK_lbl.append(QLabel("직급"))
                    self.rsRANK_le.append(QLineEdit())
                    self.rsSal_lbl.append(QLabel("호봉"))
                    self.rsSal_le.append(QLineEdit())
                    self.rsDate_lbl.append(QLabel("시작일"))
                    self.rsDate_de.append(QDateEdit())
                        
                for j in range(len(result) + self.cnt):
                    for i in range(len(self.rsWidget)):
                        if i == 0:
                            self.rslay.addWidget(self.rsWidget[i][j], 0 + 4 * j, 0)
                        elif i % 2 == 0:
                            self.rslay.addWidget(self.rsWidget[i][j], int(i / 2) + 4 * j, 0)
                        elif i % 2 == 1:
                            self.rslay.addWidget(self.rsWidget[i][j], int(i / 2) + 4 * j, 1)
                            if i % 3 == 2:
                                self.rslay.addWidget(self.rsAdd_btn, int(i / 2) + 4 * j, 2)

                self.rslay.setRowStretch(self.rslay.rowCount(), 1)
                self.cnt += 1
            else:
                QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")
            

    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT EMP_RANK, SALARY, DATE_JOIN FROM R_S WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveRS(self, emp_num, cur, conn):
        result = self.setData(self.emp_num)
        row = len(result)
        if result:
            for i in range(row):
                if self.rsRANK_le[i].text() == '':
                    return
                rsRANK = self.rsRANK_le[i].text()
                rsSal = self.rsSal_le[i].text()
                rsDate = self.rsDate_de[i].date().toString("yyyy-MM-dd")
            
                query = "UPDATE R_S SET EMP_RANK = %s, SALARY = %s, DATE_JOIN = %s WHERE EMP_NUM = %s AND EMP_RANK = %s;"
                cur.execute(query, (rsRANK, rsSal, rsDate, emp_num, rsRANK))
                conn.commit()  
            self.cnt -=1
        
        for i in range(self.cnt):
            if self.rsRANK_le[i + row].text() == '':
                return

            rsRANK = self.rsRANK_le[i + row].text()
            rsSal = self.rsSal_le[i + row].text()
            rsDate = self.rsDate_de[i + row].date().toString("yyyy-MM-dd")

            # Insert new data
            query = "INSERT INTO R_S VALUES (%s, %s, %s, %s)"
            cur.execute(query, (emp_num, rsRANK, rsSal, rsDate))
            conn.commit()

class Emplist(QMainWindow, form_class):
    closed = pyqtSignal()
    listToInfo = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.empList.setLayout(self.listLayout)
        self.setStyleSheet(stylesheet)

        # 231202 체크박스 체크된 ROWW저장 리스트, 사업부검색 콤보박스, 이름검색 라인에딧초기화 by 정현아
        self.delRowList = list()
        self.biz = '전체'
        self.name = ''
        self.w = None
        self.emp_num =None
        self.result = None
        self.path = None
        self.fname = None
        self.pixmap = None
        self.TSP = ['생산실행IT G','생산스케쥴IT G','생산품질IT G','TSP운영 1G','TSP운영 2G','TSP고객총괄','']
        self.FAB = ['빅데이터 G','인프라 G','스마트팩토리 G','']
        self.MIS = ['전기운영 G','PLM G','']
        self.TC = ['TC/TPSS개발파트','화성 TC2.5','SAS TC2.5','']
        self.SP = ['사업기획팀','기술전략팀','']
        self.BS = ['경영지원','']

        self.table.setRowCount(0)
        header = ['','부서','이름','직무','직급','직책','휴대폰번호','메일']
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)

        chk_bx_header = QTableWidgetItem()
        chk_bx_header.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        chk_bx_header.setCheckState(Qt.Unchecked)
        self.table.setHorizontalHeaderItem(0, chk_bx_header)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.conn = pymysql.connect(
            host='localhost',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
        )

        # 231202 사원전체 테이블 세팅 by 정현아
        self.cur = self.conn.cursor()
        self.main_query = "SELECT CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_KOR, POSITION, EMP_RANK, WORK_POS, PHONE, MAIL FROM MAIN_TABLE"
        self.setTables(self.main_query)

        # 231202 사원전체 수 라벨에 세팅 by 정현아
        countQuery = "SELECT COUNT(*) FROM MAIN_TABLE;"
        self.cur.execute(countQuery)
        count = self.cur.fetchone()[0]
        self.countLabel.setText("총 "+ str(count) + "건")
        
        # 체크박스와 메일은 컬럼 내용에 맞게 사이즈 설정, 그외 컬럼은 stretch로 설정 by 정현아
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)

        # 콤보박스 및 버튼 클릭 이벤트 by 정현아
        self.bizCombo.activated[str].connect(self.searchBiz)
        self.namelineEdit.returnPressed.connect(self.searchEmp)
        self.empSearchBtn.clicked.connect(self.searchEmp)

        self.table.itemChanged.connect(self.delChk)
        self.listDelBtn.clicked.connect(self.delChkList)
        self.listRegBtn.clicked.connect(self.showRegsit)

        self.table.cellDoubleClicked.connect(self.showEmpInfo)

    # 231202 테이블 세팅 함수 쿼리값 변경시 테이블위젯에 세팅된 테이블 값도 변경 by 정현아
    def setTables(self, query):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.table.setSortingEnabled(False)
        for row, row_data in enumerate(result):
            self.table.insertRow(row)

            chk_bx = QTableWidgetItem()
            chk_bx.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chk_bx.setCheckState(Qt.Unchecked)
            self.table.setItem(row, 0, chk_bx)

            for col, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                self.table.setItem(row, col + 1, item)
        self.table.sortByColumn(1,Qt.AscendingOrder)
        self.table.setSortingEnabled(True)
        self.table.blockSignals(False)

    # 231202 체크된 로우 확인 및 저장, 해당 이벤트는 테이블 아이템이 변화될 때마다 호출되므로 다른 테이블 변경 이벤트는 시그널 블록처리 by 정현아
    def delChk(self, item):
        if item.column() == 0 and item.checkState() == Qt.Checked:
            self.delRowList.append(item.row())
        elif item.column() == 0 and item.checkState() == Qt.Unchecked:
            self.delRowList.remove(item.row())

    # 231202 사원정보 삭제
    def delChkList(self):
        self.table.blockSignals(True)
        delData = []
        if not self.delRowList :
            QMessageBox.warning(self, "사원삭제실패", "선택된 사원이 없습니다.")
        else:
            # 231202 리스트에 선택된 로우의 이름과 핸드폰 정보를 리스트에 저장
            for i in self.delRowList :
                colData = []
                colData.append(self.table.item(i,2).text())
                colData.append(self.table.item(i,6).text())
                delData.append(colData)

        query = 'DELETE FROM MAIN_TABLE WHERE NAME_KOR = %s AND PHONE = %s;'
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.executemany(query,delData)
                self.conn.commit()
                QMessageBox.information(self,"사원삭제성공","삭제 되었습니다.") 
                self.setTables(self.main_query)
                self.delRowList = list()
            except Exception as e:
                QMessageBox.warning(self, "사원등록실패", "Error: " + str(e))
                return       
        self.table.blockSignals(False)

    # 231129 사업부검색 함수 이름 검색란이 비어있는지 체크하고 비어있으면 사업부 콤보박스 체크하여 조건에 맞게 필터링 by 정현아
    def searchBiz(self,biz):
        self.table.blockSignals(True)
        self.biz = biz 
        if self.name == '' :
            if self.biz == '전체':
                self.setTables(self.main_query)
                countQuery = "SELECT COUNT(*) FROM MAIN_TABLE;"
                self.cur.execute(countQuery)
                count = self.cur.fetchone()[0]
                self.countLabel.setText("총 "+ str(count) + "건")
            else:
                query = """SELECT 
                CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_KOR, POSITION, EMP_RANK, WORK_POS, PHONE, MAIL 
                FROM MAIN_TABLE 
                WHERE DEPT_BIZ = '""" + biz +"';"
                self.setTables(query)
                countQuery = "SELECT COUNT(*) FROM MAIN_TABLE WHERE DEPT_BIZ = '" + biz +"';"
                self.cur.execute(countQuery)
                count = self.cur.fetchone()[0]
                self.countLabel.setText("총 "+ str(count) + "건")
        else : 
            self.searchEmp()
        self.table.blockSignals(False)

    # 231129 이름 함수 이름 검색란이 비어있는지 체크하고 비어있지 않으면 사업부 콤보박스 체크하여 조건에 맞게 필터링 by 정현아
    def searchEmp(self):
        self.table.blockSignals(True)
        self.name = self.namelineEdit.text()
        if self.name != '':
            if self.biz == '전체':
                query = """SELECT 
                CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_KOR, POSITION, EMP_RANK, WORK_POS, PHONE, MAIL 
                FROM MAIN_TABLE 
                WHERE NAME_KOR LIKE '%""" + self.name +"%';"
                self.setTables(query)
                countQuery = "SELECT COUNT(*) FROM MAIN_TABLE WHERE NAME_KOR LIKE '%""" + self.name +"%';"
                self.cur.execute(countQuery)
                count = self.cur.fetchone()[0]
                self.countLabel.setText("총 "+ str(count) + "건")
            else :
                query = """SELECT 
                CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_KOR, POSITION, EMP_RANK, WORK_POS, PHONE, MAIL 
                FROM MAIN_TABLE 
                WHERE NAME_KOR LIKE '%""" + self.name +"%' AND DEPT_BIZ = '" + self.biz + "';"
                self.setTables(query)
                countQuery = "SELECT COUNT(*) FROM MAIN_TABLE WHERE NAME_KOR LIKE '%""" + self.name +"%' AND DEPT_BIZ = '" + self.biz + "';"
                self.cur.execute(countQuery)
                count = self.cur.fetchone()[0]
                self.countLabel.setText("총 "+ str(count) + "건")
        else:
            self.searchBiz(self.biz)
        self.table.blockSignals(False)
        
    # 핸드폰 정보를 읽어와 사원 정보를 추출하여 개인정보 조회화면과 연결 by 정현아
    def showEmpInfo(self, row, col):
        phone = self.table.item(row, 6).text()
        query = "SELECT EMP_NUM FROM MAIN_TABLE WHERE PHONE = %s;"
        self.cur.execute(query, (phone,))
        self.emp_num = self.cur.fetchone()[0]
        if self.emp_num is not None:
            self.w = EmpInfo()
            self.listToInfo.emit()
            self.w.show()
            self.hide()
            self.showInfo(self.emp_num)
            self.w.showedEdit.connect(self.showEdit)
            self.w.cnlBtn.clicked.connect(self.back)
            
    # 개인정보조회 화면 출력 by 정현아
    def showInfo(self, emp):
        familyTab = FamilyTab(emp,'info')
        self.w.familyTab = familyTab
        self.w.tabWidget.addTab(self.w.familyTab.family, '가족관계')

        contactTab = ContactTab(emp,'info')
        self.w.contactTab = contactTab
        self.w.tabWidget.addTab(self.w.contactTab.contact, '비상연락처')

        schoolTab = SchoolTab(emp,'info')
        self.w.schoolTab = schoolTab
        self.w.tabWidget.addTab(self.w.schoolTab.school, '학력')

        certificationTab = CertificationTab(emp,'info')
        self.w.certificationTab = certificationTab
        self.w.tabWidget.addTab(self.w.certificationTab.certificate, '자격증')
        
        careerTab = CareerTab(emp,'info')
        self.w.careerTab = careerTab
        self.w.tabWidget.addTab(self.w.careerTab.career, '경력')

        technicalTab = TechnicalTab(emp,'info')
        self.w.technicalTab = technicalTab
        self.w.tabWidget.addTab(self.w.technicalTab.technical, '기술사항')

        rpTab = RPTab(emp,'info')
        self.w.rpTab = rpTab
        self.w.tabWidget.addTab(self.w.rpTab.rp, '상벌')

        rsTab = RSTab(emp,'info')
        self.w.rsTab = rsTab
        self.w.tabWidget.addTab(self.w.rsTab.rs, '호봉')
        
        self.w.layout = QVBoxLayout()
        self.w.layout.addWidget(self.w.tabWidget)

        query = """
        SELECT 
        NAME_KOR, EMP_NUM, EMP_RANK, POSITION, PHONE, MAIL, CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_ENG, 
        ADDRESS, WORK_POS, SALARY, DATE_JOIN, IFNULL(HEIGHT,''), IFNULL(WEIGHT,''), MILITARY, MARRY, LAST_EDU,ADDRESS_NUM, PIC 
        FROM MAIN_TABLE 
        WHERE EMP_NUM = %s; 
        """
        self.cur.execute(query,(emp,))
        result = self.cur.fetchone()
        
        self.w.namekor.setText(result[0])
        self.w.empnum.setText(str(result[1]))
        self.w.emprank.setText(result[2])
        self.w.position.setText(result[3])
        self.w.phone.setText(result[4])
        self.w.mail.setText(result[5])
        self.w.dept.setText(result[6])
        self.w.nameeng.setText(result[7])
        self.w.address.setText(result[8])
        self.w.work_pos.setText(result[9])
        self.w.sal.setText(result[10])
        self.w.joindate.setText(str(result[11]))
        self.w.height.setText(str(result[12]))
        self.w.weight.setText(str(result[13]))
        self.w.militay.setText(result[14])
        self.w.marry.setText(result[15])
        self.w.lastedu.setText(result[16])
        self.w.addressnum.setText(str(result[17]))

        data = result[18]
        img = QPixmap()
        img.loadFromData(data, 'PNG')

        resize_pixmap = img.scaled(130,150)
        self.w.pic.setPixmap(resize_pixmap) 

    # 개인정보편집화면으로 이동
    def showEdit(self):
        familyTab = FamilyTab(self.emp_num,'edit')
        self.w.w.familyTab = familyTab
        self.w.w.tabWidget.addTab(self.w.w.familyTab.family, '가족관계')

        contactTab = ContactTab(self.emp_num,'edit')
        self.w.w.contactTab = contactTab
        self.w.w.tabWidget.addTab(self.w.w.contactTab.contact, '비상연락처')

        schoolTab = SchoolTab(self.emp_num,'edit')
        self.w.w.schoolTab = schoolTab
        self.w.w.tabWidget.addTab(self.w.w.schoolTab.school, '학력')

        certificationTab = CertificationTab(self.emp_num,'edit')
        self.w.w.certificationTab = certificationTab
        self.w.w.tabWidget.addTab(self.w.w.certificationTab.certificate, '자격증')
        
        careerTab = CareerTab(self.emp_num,'edit')
        self.w.w.careerTab = careerTab
        self.w.w.tabWidget.addTab(self.w.w.careerTab.career, '경력')

        technicalTab = TechnicalTab(self.emp_num,'edit')
        self.w.w.technicalTab = technicalTab
        self.w.w.tabWidget.addTab(self.w.w.technicalTab.technical, '기술사항')

        rpTab = RPTab(self.emp_num,'edit')
        self.w.w.rpTab = rpTab
        self.w.w.tabWidget.addTab(self.w.w.rpTab.rp, '상벌')

        rsTab = RSTab(self.emp_num,'edit')
        self.w.w.rsTab = rsTab
        self.w.w.tabWidget.addTab(self.w.w.rsTab.rs, '호봉')
        
        self.w.w.layout = QVBoxLayout()
        self.w.w.layout.addWidget(self.w.w.tabWidget)
        
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

        self.w.w.dept.activated[str].connect(self.changeGroup)
        self.w.w.addImgBtn.clicked.connect(self.showAddImg)
        self.w.w.regnum_lineEdit2.setEchoMode(QLineEdit.Password)

        # 231201 입력 제한 by 정현아
        self.w.w.regnum_lineEdit.setValidator(QIntValidator(1,100000,self))
        self.w.w.regnum_lineEdit2.setValidator(QIntValidator(1,1000000,self))
        self.w.w.phone_lineEdit2.setValidator(QIntValidator(1,1000,self))
        self.w.w.phone_lineEdit3.setValidator(QIntValidator(1,1000,self))
        self.w.w.addressnum_lineEdit.setValidator(QIntValidator(1,10000,self))
        rep = QRegExp("[가-힣0-9\\s,()]{0,49}")
        self.w.w.address_lineEdit.setValidator(QRegExpValidator(rep))
        self.w.w.height_lineEdit.setValidator(QIntValidator(1,100,self))
        self.w.w.weight_lineEdit.setValidator(QIntValidator(1,100,self))

        # 231201 저장된 사원정보가져와 라벨 및 에디트에 세팅 by 정현아
        self.w.w.namekor.setText(self.result[0])
        self.w.w.nameeng.setText(self.result[1])
        self.w.w.empnum.setText(str(self.result[2]))
        date_str = self.result[3].strftime("%Y-%m-%d")
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        self.w.w.joindate.setDate(date)
        self.w.w.emprank.setCurrentText(self.result[4])
        self.w.w.regnum_lineEdit.setText(self.result[5])
        self.w.w.regnum_lineEdit2.setText(self.result[6])
        self.w.w.mail_lineEdit.setText(self.result[7])
        self.w.w.phone_combo.setCurrentText(self.result[8])
        self.w.w.phone_lineEdit2.setText(self.result[9])
        self.w.w.phone_lineEdit3.setText(self.result[10])
        self.w.w.dept.setCurrentText(self.result[11])

        self.w.w.work_pos.setCurrentText(self.result[12])
        self.w.w.position.setCurrentText(self.result[13])
        self.w.w.addressnum_lineEdit.setText(str(self.result[14]))
        self.w.w.address_lineEdit.setText(self.result[15])
        self.w.w.sal.setCurrentText(self.result[16])
        self.w.w.height_lineEdit.setText(str(self.result[17]))
        self.w.w.weight_lineEdit.setText(str(self.result[18]))
        mil = self.result[19]
        if mil == '군필':
            self.w.w.milBtn.setChecked(True)
        elif mil == '미필':
            self.w.w.milBtn2.setChecked(True)
        else:
            self.w.w.milBtn3.setChecked(True)
        
        marry = self.result[20]
        if marry == '기혼':
            self.w.w.maryyBtn.setChecked(True)
        else : 
            self.w.w.maryyBtn2.setChecked(True)
            
        self.w.w.lastedu_combo.setCurrentText(self.result[21])

        img = QPixmap()
        img.loadFromData(self.result[22], 'PNG')
        resize_pixmap = img.scaled(130,150)
        self.w.w.pic.setPixmap(resize_pixmap) 
        self.w.w.saveBtn.clicked.connect(self.saveEdit)
        
        self.changeGroup(self.result[11])
        self.w.w.dept_g.setCurrentText(self.result[23])
        self.w.w.sal2.setText(self.result[24])
    
    # 사업부 선택시 그룹명 동적으로 세팅
    def changeGroup(self,biz):
        self.w.w.dept_g.clear()
        if biz == '경영지원실':
            self.w.w.dept_g.addItems(self.BS)
        elif biz == 'TSP':
            self.w.w.dept_g.addItems(self.TSP)
            return
        elif biz == 'FAB':
            self.w.w.dept_g.addItems(self.FAB)
            return
        elif biz == 'MIS':
            self.w.w.dept_g.addItems(self.MIS)
            return
        elif biz == 'TC':
            self.w.w.dept_g.addItems(self.TC)
            return
        elif biz == '전략기획실':    
            self.w.w.dept_g.addItems(self.SP) 
            return        

    # 개인정보편집에서 수정한 내용 DB에 저장
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
        attrDict['주민번호'] = self.w.w.regnum_lineEdit.text() + self.w.w.regnum_lineEdit2.text()
        reg_num = self.w.w.regnum_lineEdit.text() + self.w.w.regnum_lineEdit2.text()
        attrDict['메일'] = self.w.w.mail_lineEdit.text()
        attrDict['휴대폰번호'] = self.w.w.phone_combo.currentText() + self.w.w.phone_lineEdit2.text() + self.w.w.phone_lineEdit3.text()
        if self.w.w.addressnum_lineEdit.text() == '':
            QMessageBox.warning(self, "사원등록실패", "우편번호가 입력되지 않았습니다. 우편번호 입력바랍니다.")
            return
        else:
            attrDict['우편번호'] = int(self.w.w.addressnum_lineEdit.text())
        attrDict['주소'] = self.w.w.address_lineEdit.text()

        height = self.w.w.height_lineEdit.text()
        weight = self.w.w.weight_lineEdit.text()

        if height == '': 
            attrDict['신장'] = None
        else:
            attrDict['신장'] = int(height)

        if weight == '': 
            attrDict['체중'] = None
        else:
            attrDict['체중'] = int(weight)       


        if self.w.w.milBtn.isChecked():
            attrDict['군필여부'] = self.w.w.milBtn.text()
        elif self.w.w.milBtn2.isChecked():
            attrDict['군필여부'] = self.w.w.milBtn2.text()
        else:
            attrDict['군필여부'] = self.w.w.milBtn3.text()
            
        if self.w.w.maryyBtn.isChecked():
            attrDict['결혼여부'] = self.w.w.maryyBtn.text()
        else:
            attrDict['결혼여부'] = self.w.w.maryyBtn2.text()    
        attrDict['최종학력'] = self.w.w.lastedu_combo.currentText()

        if self.pixmap is not None:
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            self.pixmap.toImage().save(buffer, 'PNG')
            attrDict['사진'] = byte_array.data()  

        attrDict['한글성명'] = self.w.w.namekor.text()
        attrDict['영문성명'] = self.w.w.nameeng.text()
        # 사번은 int type
        if self.w.w.empnum.text() != '' :
            attrDict['사번'] = int(self.w.w.empnum.text())
        attrDict['입사일'] = self.w.w.joindate.date().toString("yyyy-MM-dd")
        attrDict['직급'] = self.w.w.emprank.currentText()
        attrDict['사업부'] = self.w.w.dept.currentText()
        attrDict['직책'] = self.w.w.work_pos.currentText()
        attrDict['그룹'] = self.w.w.dept_g.currentText()
        attrDict['직무'] = self.w.w.position.currentText()
        attrDict['호봉'] = self.w.w.sal.currentText() + self.w.w.sal2.text()


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
        
        if self.result[5] + self.result[6] != attrDict['주민번호'] or self.result[2] != attrDict['사번']:
            t1 = (self.result[2], attrDict['사번'], self.result[5] + self.result[6],attrDict['주민번호'])
            query = """
            SELECT NULLIF(EMP_NUM, %s), NULLIF(REG_NUM , %s) FROM MAIN_TABLE WHERE EMP_NUM=%s OR  REG_NUM =%s;
            """
            try:
                self.cur.execute(query, t1)
                result = self.cur.fetchone()
                if result is not None :
                    if result[0] is not None:
                        QMessageBox.warning(self, "개인정보변경실패", "이미 등록된 사번입니다.")
                        return
                    elif result[1] is not None: 
                        QMessageBox.warning(self, "개인정보변경실패", "이미 등록된 주민번호입니다.")
                        return
            except Exception as e:
                QMessageBox.warning(self, "사원등록실패", "Error: " + str(e))
                return        

        query = """
        UPDATE MAIN_TABLE 
        SET REG_NUM = %s, MAIL = %s, PHONE = %s, ADDRESS_NUM = %s, ADDRESS = %s, HEIGHT = %s, WEIGHT = %s, MILITARY = %s, 
        MARRY = %s, LAST_EDU = %s, PIC = %s, NAME_KOR = %s, NAME_ENG = %s, EMP_NUM = %s, DATE_JOIN =%s, EMP_RANK = %s, 
        DEPT_BIZ = %s, WORK_POS = %s, DEPT_GROUP = %s, POSITION = %s, SALARY =%s, AGE = %s, GENDER = %s
        WHERE EMP_NUM = %s; 
        """
        reply = QMessageBox.question(self, '변경 확인', '변경하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.execute(query,tuple(attrDict.values()) + (self.emp_num,))
                self.conn.commit()
                self.w.w.familyTab.saveFamily(self.emp_num,self.cur,self.conn)
                QMessageBox.information(self, "개인정보변경성공", "개인정보가 변경되었습니다.")
                self.w.w.close()

                self.showInfo(self.emp_num)              

            except Exception as e:
                QMessageBox.warning(self, "개인정보변경실패", "Error: " + str(e))
                return 

    # 이미지 저장 팝업창 생성
    def showAddImg(self):
        self.w1 = AddImg()
        self.w1.show()
        self.w1.searchbutton.clicked.connect(self.openImage)
        self.w1.savebtn.clicked.connect(self.save_img)
        self.w1.cnlBtn.clicked.connect(self.w1.close)
    
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

    # 이미지 파일 사이즈 확인
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
                self.w.w.pic.setPixmap(resize_pixmap)
        self.w1.close()

    # 231122 페이지 전환 함수 by정현아
    def showRegsit(self):
        self.w = Regist()
        self.w.show()
        self.hide()
        self.w.cnlBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)

    def back(self):
        self.w.hide()
        self.show()

    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

stylesheet = """
    QTableWidget {
        border-radius: 10px;
        background-color: #eeeeee;
        margin-top:10px;   
        margin-bottom:10px;       
        padding-left:10px;          
        padding-right:10px;
    }
    QTableWidget::item {
        background-color: #ffffff;
        margin-top: 5px;    
        margin-bottom:5px;      
        border-radius: 9px;
    }
    QTableWidget::item:selected {
        color: black;
    }
    QHeaderView::section{
        Background-color:#c6c6c6;
        border-radius:5px;
        margin-top:25px; 
        margin-bottom:5px;
    }
"""

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Emplist() 
    myWindow.show() 
    app.exec_()