import pymysql

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
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
            
            query = "INSERT INTO FAMILY(EMP_NUM, NAME_FAMILY, BIRTH, AGE, REL, LIVE) VALUES(%s, %s, %s, %s, %s, %s)"
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
            
            query = "INSERT INTO CONTACT(EMP_NUM, NAME, REL, PHONE) VALUES(%s, %s, %s, %s)"
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
            
            query = "INSERT INTO SCHOOL_EDUCATION(EMP_NUM, DATE_ADMITION, DATE_GRADUATE, NAME_SCHOOL, LOCATION, MAJOR, SUB_MAJOR, COMMENT) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
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
                
            query = "INSERT INTO CERTIFICATE(EMP_NUM, NAME_LICENSE, DATE_ACQUI) VALUES(%s, %s, %s)"
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

            query = """
                    INSERT INTO CAREER (EMP_NUM, COMPANY, DEPARTMENT, DATE_JOIN, DATE_LEAVE, WORK_PERIOD, FINAL_RANK, WORK_INFO)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
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

            query = "INSERT INTO TECHNICAL (EMP_NUM, TEC_DETAIL, PROFICIENCY, NOTE) VALUES (%s, %s, %s, %s);"
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

            query = "INSERT INTO R_P (EMP_NUM, NAME_REW_PUNI, SCORE, DATE_REW_PUNI, NOTE) VALUES (%s, %s, %s, %s, %s)"
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

            query = "INSERT INTO R_S (EMP_NUM, EMP_RANK, SALARY, DATE_JOIN) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (emp_num, rsRANK, rsSal, rsDate))
            conn.commit()
            
    def initRS(self):
        self.rsRANK_le[0].clear()
        self.rsSal_le[0].clear()
        self.rsDate_de[0].setDate(QDate(2000, 1, 1))
        self.cnt = 0
