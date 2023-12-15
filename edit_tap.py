import pymysql

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class FamilyTab(QWidget):
    def __init__(self, emp_num, type):
        super(FamilyTab, self).__init__()
        self.cnt = 0
        self.result_num = 0
        self.emp_num = emp_num
        self.type = type
        self.delete_list = []
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
        self.ignored_result = False
        if self.type == 'info':
            self.addFamilyMember()
        else: 
            self.fAdd_btn = QPushButton("추가")
            self.btnGroup = QButtonGroup(self)
            self.del_btn = []
            self.editFamilyMember()
            self.cnt = self.result_num
            self.fAdd_btn.clicked.connect(self.editFamilyMember)
            self.btnGroup.buttonClicked[int].connect(self.disappearFamliy)

    def addFamilyMember(self):
        result = self.setData(self.emp_num)
        if not result :
            return
        else :
            self.cnt = len(result)
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
        if not result or self.ignored_result:
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
                self.cnt+=1
            else:
                QMessageBox.information(self,"경고","5번 이상 등록하실 수 없습니다.")
        # 231205 있을 경우 등록된 데이터를 각 에디터에 세팅 by 정현아
        else :
            self.result_num = len(result)
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
                        self.del_btn.append(QPushButton("삭제",self))
                        self.btnGroup.addButton(self.del_btn[i])
                        
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
                    
                # 라벨 및 에디터 레이아웃에 세팅(홀수번째는 라벨, 짝수번째는 에디터로 각 레이아웃에 배치)
                for j in range(len(result)+self.cnt):
                    for i in range(len(self.familyWidget)):
                        if i == 0:
                            self.flay.addWidget(self.familyWidget[i][j],0 + 4 * j,0)
                        elif i % 2 == 0:
                            self.flay.addWidget(self.familyWidget[i][j],int(i/2) + 4 * j,0)
                            if i % 4 == 2:
                                if j < len(result):
                                    self.flay.addWidget(self.del_btn[j], int(i/2)-1 + 4 * j,2)
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
              
    def disappearFamliy(self,index):
        j=0
        btn = self.btnGroup.button(index)
        for i in range(len(self.del_btn)):
            if btn == self.del_btn[i]:
                j = i
        for i in range(len(self.familyWidget)):
            self.flay.removeWidget(self.familyWidget[i][j])
            self.familyWidget[i].pop(j)
        self.flay.removeWidget(self.del_btn[j])
        self.btnGroup.removeButton(self.del_btn[j])
        self.del_btn.pop(j)
        self.cnt-=1  
        if self.cnt != 0:
            self.flay.addWidget(self.fAdd_btn, 3 + 4 * (self.cnt-1),2)
            print(3 + 4 * (self.cnt-1))
        self.flay.setRowStretch(self.flay.rowCount(), 1)      
        if self.cnt == 0:
            self.ignored_result = True
            self.editFamilyMember()
        
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

                self.rslay.setRowStretch((self.rslay.rowCount()*(4-self.cnt)),1)
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
