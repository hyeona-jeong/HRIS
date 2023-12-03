import os
import sys
import re
import pymysql

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

class Regist(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.regist.setLayout(self.regLayout)
        self.addImgBtn.clicked.connect(self.showAddImg)
        self.tabWidget.setMovable(True)

        # 231203 가족관계 탭 생성 by 정현아
        self.layout = QVBoxLayout()
        self.family = QScrollArea()
        self.tabWidget.addTab(self.family,'가족관계')
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
        
        self.addfamily()
        self.fAdd_btn.clicked.connect(self.addfamily)

        # 231203 연락처 탭 생성 by 정현아
        self.contact = QScrollArea()
        self.tabWidget.addTab(self.contact,'연락처')
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
        
        self.addcontact()
        self.cAdd_btn.clicked.connect(self.addcontact)

        # 231203 학력 탭 생성 by 정현아
        self.school = QScrollArea()
        self.tabWidget.addTab(self.school,'학력')
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
        
        self.addschool()
        self.schAdd_btn.clicked.connect(self.addschool)

        # 231203 자격증 탭 생성 by 정현아
        self.certificate = QScrollArea()
        self.tabWidget.addTab(self.certificate,'자격증')
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
        
        self.addcert()
        self.certAdd_btn.clicked.connect(self.addcert)

        self.layout.addWidget(self.tabWidget)

    # 231123 페이지 전환 함수 by 정현아    
    def showAddImg(self):
        self.w = AddImg()
        self.w.show()
        self.w.cnlBtn.clicked.connect(self.w.close)
        
    # 231115 가족 정보 추가작성을 위해 새로운 작성폼 생성 by 정현아        
    def addfamily(self):
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
            
            self.flay.setRowStretch((self.flay.rowCount()*(5-self.fcnt)),1)
            self.fcnt+=1;
            
        else:
            QMessageBox.information(self,"경고","5번 이상 등록하실 수 없습니다.")

    def addcontact(self):
        if(self.ccnt<=1):
            self.cName_lbl.append(QLabel("성명"))
            self.cName_le.append(QLineEdit(self))
            self.cRel_lbl.append(QLabel("관계"))
            self.cRel_cb.append(QComboBox())
            for i in range(len(self.f_list)):
                self.cRel_cb[self.ccnt].addItem(self.f_list[i])
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
            
            self.clay.setRowStretch((self.clay.rowCount()*(2-self.ccnt)),1)
            self.ccnt+=1;
            
        else:
            QMessageBox.information(self,"경고","2번 이상 등록하실 수 없습니다.")


    def addschool(self):
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


    def addcert(self):
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
            
            self.certlay.setRowStretch((self.certlay.rowCount()*(10-self.certcnt)),1)
            self.certcnt+=1;
            
        else:
            QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")
        
    
    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Regist() 
    myWindow.show() 
    app.exec_() 