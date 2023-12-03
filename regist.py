import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
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
        self.fcnt = 0
        self.initUI()

    def initUI(self):
        self.family = QScrollArea()
        self.fcnt = 0
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
        if(self.fcnt<=4):
            self.fName_lbl.append(QLabel("가족성명"))
            self.fName_le.append(QLineEdit(self))
            self.fYear_lbl.append(QLabel("생년월일"))
            self.fYear_de.append(QDateEdit(self))
            self.fRel_lbl.append(QLabel("관계"))
            self.fRel_cb.append(QComboBox())
            self.f_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
            for i in range(len(self.f_list)):
                self.fRel_cb[self.fcnt].addItem(self.f_list[i])
            self.fLive_lbl.append(QLabel("동거여부"))
            self.fLive_cb.append(QComboBox())
            self.fLive_cb[self.fcnt].addItem('Y')
            self.fLive_cb[self.fcnt].addItem('N')
            
            for i in range(len(self.familyWidget)):
                if i == 0:
                    self.flay.addWidget(self.familyWidget[i][self.fcnt],0 + 4 * self.fcnt,0)
                elif i % 2 == 0:
                    self.flay.addWidget(self.familyWidget[i][self.fcnt],int(i/2) + 4 * self.fcnt,0)
                elif i % 2 == 1:
                    self.flay.addWidget(self.familyWidget[i][self.fcnt],int(i/2) + 4 * self.fcnt,1)
                    if i % 4 == 3:
                        self.flay.addWidget(self.fAdd_btn,int(i/2) + 4 * self.fcnt,2)
            
            self.flay.setRowStretch((self.flay.rowCount()*(4-self.fcnt)),1)
            self.fcnt+=1;
            
        else:
            QMessageBox.information(self,"경고","5번 이상 등록하실 수 없습니다.")

# 연락처탭
class ContactTab(QWidget):
    def __init__(self, parent=None):
        super(ContactTab, self).__init__(parent)
        self.ccnt = 0
        self.initUI()

    def initUI(self):
        self.contact = QScrollArea()
        self.ccnt = 0
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

    def addContact(self):
        if(self.ccnt<=1):
            self.cName_lbl.append(QLabel("성명"))
            self.cName_le.append(QLineEdit(self))
            self.cRel_lbl.append(QLabel("관계"))
            self.cRel_cb.append(QComboBox())
            self.c_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
            for i in range(len(self.c_list)):
                self.cRel_cb[self.ccnt].addItem(self.c_list[i])
            self.cCont_lbl.append(QLabel("연락처"))
            self.cCont_le.append(QLineEdit(self))
            
            for i in range(len(self.contactWidget)):
                if i == 0:
                    self.clay.addWidget(self.contactWidget[i][self.ccnt],0 + 3 * self.ccnt,0)
                elif i % 2 == 0:
                    self.clay.addWidget(self.contactWidget[i][self.ccnt],int(i/2) + 3 * self.ccnt,0)
                elif i % 2 == 1:
                    self.clay.addWidget(self.contactWidget[i][self.ccnt],int(i/2) + 3 * self.ccnt,1)
                    if i % 3 == 2:
                        self.clay.addWidget(self.cAdd_btn,int(i/2) + 3 * self.ccnt,2)
            
            self.clay.setRowStretch((self.clay.rowCount()*(4-self.ccnt)),1)
            self.ccnt+=1;
            
        else:
            QMessageBox.information(self,"경고","2번 이상 등록하실 수 없습니다.")

# 학력 탭
class SchoolTab(QWidget):
    def __init__(self, parent=None):
        super(SchoolTab, self).__init__(parent)
        self.schcnt = 0
        self.initUI()

    def initUI(self):
        self.school = QScrollArea()
        self.schcnt = 0
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
        if(self.schcnt<=3):
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
                    self.schlay.addWidget(self.schWidget[i][self.schcnt],0 + 7 * self.schcnt,0)
                elif i % 2 == 0:
                    self.schlay.addWidget(self.schWidget[i][self.schcnt],int(i/2) + 7 * self.schcnt,0)
                elif i % 2 == 1:
                    self.schlay.addWidget(self.schWidget[i][self.schcnt],int(i/2) + 7 * self.schcnt,1)
                    if i % 7 == 6:
                        self.schlay.addWidget(self.schAdd_btn,int(i/2) + 7 * self.schcnt,2)
            
            self.schlay.setRowStretch((self.schlay.rowCount()*(4-self.schcnt)),1)
            self.schcnt+=1;
            
        else:
            QMessageBox.information(self,"경고","4번 이상 등록하실 수 없습니다.")

# 자격증 탭
class CertificationTab(QWidget):
    def __init__(self, parent=None):
        super(CertificationTab, self).__init__(parent)
        self.certcnt = 0
        self.initUI()

    def initUI(self):
        self.certificate = QScrollArea()
        self.certcnt = 0
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
        if(self.certcnt<=9):
            self.certName_lbl.append(QLabel("자격증명"))
            self.certName_le.append(QLineEdit(self))
            self.certDate_lbl.append(QLabel("취득일"))
            self.certDate_de.append(QDateEdit(self))
            
            for i in range(len(self.certwidget)):
                if i == 0:
                    self.certlay.addWidget(self.certwidget[i][self.certcnt],0 + 2 * self.certcnt,0)
                elif i % 2 == 0:
                    self.certlay.addWidget(self.certwidget[i][self.certcnt],int(i/2) + 2 * self.certcnt,0)
                elif i % 2 == 1:
                    self.certlay.addWidget(self.certwidget[i][self.certcnt],int(i/2) + 2 * self.certcnt,1)
                    self.certlay.addWidget(self.certAdd_btn,int(i/2) + 2 * self.certcnt,2)
            
            self.certlay.setRowStretch((self.certlay.rowCount()*(4-self.certcnt)),1)
            self.certcnt+=1;
            
        else:
            QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")

# 경력탭
class CareerTab(QWidget):
    def __init__(self, parent=None):
        super(CareerTab, self).__init__(parent)
        self.carcnt = 0
        self.initUI()

    def initUI(self):
        self.career = QScrollArea()
        self.carcnt = 0
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
        if(self.carcnt<=9):
            self.company_lbl.append(QLabel("근무회사"))
            self.company_le.append(QLineEdit(self))
            self.dept_lbl.append(QLabel("근무부서"))
            self.dept_le.append(QDateEdit(self))
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
                    self.carlay.addWidget(self.carWidget[i][self.carcnt],0 + 6 * self.carcnt,0)
                elif i % 2 == 0:
                    self.carlay.addWidget(self.carWidget[i][self.carcnt],int(i/2) + 6 * self.carcnt,0)
                elif i % 2 == 1:
                    self.carlay.addWidget(self.carWidget[i][self.carcnt],int(i/2) + 6 * self.carcnt,1)
                    if i % 6 == 5:
                        self.carlay.addWidget(self.carAdd_btn,int(i/2) + 6 * self.carcnt,2)
            
            self.carlay.setRowStretch((self.carlay.rowCount()*(4-self.carcnt)),1)
            self.carcnt+=1;
            
        else:
            QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")
# 기술사항탭
class TechnicalTab(QWidget):
    def __init__(self, parent=None):
        super(TechnicalTab, self).__init__(parent)
        self.techcnt = 0
        self.initUI()

    def initUI(self):
        self.technical = QScrollArea()
        self.techcnt = 0
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
        if(self.techcnt<=9):
            self.techDet_lbl.append(QLabel("기술사항"))
            self.techDet_le.append(QLineEdit(self))
            self.pro_lbl.append(QLabel("숙련도"))
            self.pro_cb.append(QComboBox())
            self.pro_cb[self.techcnt].addItem('상')
            self.pro_cb[self.techcnt].addItem('중')
            self.pro_cb[self.techcnt].addItem('하')
            self.note_lbl.append(QLabel("비고"))
            self.note_le.append(QLineEdit(self))
            
            for i in range(len(self.techWidget)):
                if i == 0:
                    self.techlay.addWidget(self.techWidget[i][self.techcnt],0 + 3 * self.techcnt,0)
                elif i % 2 == 0:
                    self.techlay.addWidget(self.techWidget[i][self.techcnt],int(i/2) + 3 * self.techcnt,0)
                elif i % 2 == 1:
                    self.techlay.addWidget(self.techWidget[i][self.techcnt],int(i/2) + 3 * self.techcnt,1)
                    if i % 3 == 2:
                        self.techlay.addWidget(self.techAdd_btn,int(i/2) + 3 * self.techcnt,2)
            
            self.techlay.setRowStretch((self.techlay.rowCount()*(4-self.techcnt)),1)
            self.techcnt+=1;
            
        else:
            QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")

# 231203 상벌탭 생성 by 정현아
class RPTab(QWidget):
    def __init__(self, parent=None):
        super(RPTab, self).__init__(parent)
        self.rpcnt = 0
        self.initUI()

    def initUI(self):
        self.rp = QScrollArea()
        self.rpcnt = 0
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
        if(self.rpcnt<=19):
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
                    self.rplay.addWidget(self.rpWidget[i][self.rpcnt],0 + 4 * self.rpcnt,0)
                elif i % 2 == 0:
                    self.rplay.addWidget(self.rpWidget[i][self.rpcnt],int(i/2) + 4 * self.rpcnt,0)
                elif i % 2 == 1:
                    self.rplay.addWidget(self.rpWidget[i][self.rpcnt],int(i/2) + 4 * self.rpcnt,1)
                    if i % 4 == 3:
                        self.rplay.addWidget(self.rpAdd_btn,int(i/2) + 4 * self.rpcnt,2)
            
            self.rplay.setRowStretch((self.rplay.rowCount()*(4-self.rpcnt)),1)
            self.rpcnt+=1;
            
        else:
            QMessageBox.information(self,"경고","20번 이상 등록하실 수 없습니다.")
# 호봉 탭
class RSTab(QWidget):
    def __init__(self, parent=None):
        super(RSTab, self).__init__(parent)
        self.rscnt = 0
        self.initUI()

    def initUI(self):
        self.rs = QScrollArea()
        self.rscnt = 0
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
        if(self.rscnt<=29):
            self.rsRANK_lbl.append(QLabel("상벌명"))
            self.rsRANK_le.append(QLineEdit(self))
            self.rsSal_lbl.append(QLabel("점수"))
            self.rsSal_le.append(QLineEdit(self))
            self.rsDate_lbl.append(QLabel("상벌일"))
            self.rsDate_de.append(QDateEdit(self))
            
            for i in range(len(self.rsWidget)):
                if i == 0:
                    self.rslay.addWidget(self.rsWidget[i][self.rscnt],0 + 4 * self.rscnt,0)
                elif i % 2 == 0:
                    self.rslay.addWidget(self.rsWidget[i][self.rscnt],int(i/2) + 4 * self.rscnt,0)
                elif i % 2 == 1:
                    self.rslay.addWidget(self.rsWidget[i][self.rscnt],int(i/2) + 4 * self.rscnt,1)
                    if i % 3 == 2:
                        self.rslay.addWidget(self.rsAdd_btn,int(i/2) + 4 * self.rscnt,2)
            
            self.rslay.setRowStretch((self.rslay.rowCount()*(4-self.rscnt)),1)
            self.rscnt+=1;
            
        else:
            QMessageBox.information(self,"경고","30번 이상 등록하실 수 없습니다.")


class Regist(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.regist.setLayout(self.regLayout)
        self.addImgBtn.clicked.connect(self.showAddImg)
        self.tabWidget.setMovable(True)

        self.familyTab = FamilyTab(self)
        self.contactTab = ContactTab(self)
        self.schoolTab = SchoolTab(self)
        self.certificationTab = CertificationTab(self)
        self.careerTab = CareerTab(self)
        self.technicalTab = TechnicalTab(self)
        self.rpTab = RPTab(self)
        self.rsTab = RSTab(self)

        self.tabWidget.addTab(self.familyTab.family, '가족관계')
        self.tabWidget.addTab(self.contactTab.contact, '연락처')
        self.tabWidget.addTab(self.schoolTab.school, '학력')
        self.tabWidget.addTab(self.certificationTab.certificate, '자격증')
        self.tabWidget.addTab(self.careerTab.career, '경력')
        self.tabWidget.addTab(self.technicalTab.technical, '기술사항')
        self.tabWidget.addTab(self.rpTab.rp, '상벌')
        self.tabWidget.addTab(self.rsTab.rs, '호봉')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabWidget)

        self.show()

    # 231123 페이지 전환 함수 by 정현아    
    def showAddImg(self):
        self.w = AddImg()
        self.w.show()
        self.w.cnlBtn.clicked.connect(self.w.close)

    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Regist()
    myWindow.show()
    app.exec_()