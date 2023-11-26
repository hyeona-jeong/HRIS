import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('emp_regist_1122.ui')
form_class = uic.loadUiType(form)[0]

class Regist(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        #그룹박스내에 생성창 리스트
        self.regist.setLayout(self.regLayout)

        self.fcnt = 0
        self.tabWidget.setMovable(True)
        
        self.layout = QVBoxLayout()
        self.family = QScrollArea()
        self.tabWidget.addTab(self.family,'가족관계')
        
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
        
        self.fName_lbl.append(QLabel("가족성명",self))
        self.fName_le.append(QLineEdit(self))
        self.fYear_lbl.append(QLabel("생년월일"))
        self.fYear_de.append(QDateEdit(self))
        self.fRel_lbl.append(QLabel("관계"))
        self.fRel_cb.append(QComboBox())
        self.f_list = ['조부','조모','외조부','외조모','부','모','빙부','빙모','형제','배우자','자녀']
        for i in range(len(self.f_list)):
            self.fRel_cb[0].addItem(self.f_list[i])
        self.fLive_lbl.append(QLabel("동거여부"))
        self.fLive_cb.append(QComboBox())
        self.fLive_cb[0].addItem('Y')
        self.fLive_cb[0].addItem('N')
        self.fAdd_btn = QPushButton("추가")
        
        self.flay.addWidget(self.fName_lbl[0],0,0)
        self.flay.addWidget(self.fName_le[0],0,1)
        self.flay.addWidget(self.fYear_lbl[0],1,0)
        self.flay.addWidget(self.fYear_de[0],1,1)
        self.flay.addWidget(self.fRel_lbl[0],2,0)
        self.flay.addWidget(self.fRel_cb[0],2,1)
        self.flay.addWidget(self.fLive_lbl[0],3,0)
        self.flay.addWidget(self.fLive_cb[0],3,1)
        self.flay.addWidget(self.fAdd_btn,3,2)
        self.flay.setRowStretch((self.flay.rowCount()*(4-self.fcnt)),1)

        self.layout.addWidget(self.tabWidget)
        

        self.fAdd_btn.clicked.connect(self.addfamily)
        
    # 231115 가족 정보 추가작성을 위해 새로운 작성폼 생성 by 정현아        
    def addfamily(self):
        if(self.fcnt<=3):
            self.fcnt+=1;
            
            self.fName_lbl.append(QLabel("가족성명",self))
            self.fName_le.append(QLineEdit(self))
            self.fYear_lbl.append(QLabel("생년월일"))
            self.fYear_de.append(QDateEdit(self))
            self.fRel_lbl.append(QLabel("관계"))
            self.fRel_cb.append(QComboBox())
            self.f_list = ['조부','조모','외조부','외조모','부','모','빙부','빙모','형제','배우자','자녀']
            for i in range(len(self.f_list)):
                self.fRel_cb[self.fcnt].addItem(self.f_list[i])
            self.fLive_lbl.append(QLabel("동거여부"))
            self.fLive_cb.append(QComboBox())
            self.fLive_cb[self.fcnt].addItem('Y')
            self.fLive_cb[self.fcnt].addItem('N')
        
            self.flay.addWidget(self.fName_lbl[self.fcnt],(4*self.fcnt),0)
            self.flay.addWidget(self.fName_le[self.fcnt],(4*self.fcnt),1)
            self.flay.addWidget(self.fYear_lbl[self.fcnt],1+(4*self.fcnt),0)
            self.flay.addWidget(self.fYear_de[self.fcnt],1+(4*self.fcnt),1)
            self.flay.addWidget(self.fRel_lbl[self.fcnt],2+(4*self.fcnt),0)
            self.flay.addWidget(self.fRel_cb[self.fcnt],2+(4*self.fcnt),1)
            self.flay.addWidget(self.fLive_lbl[self.fcnt],3+(4*self.fcnt),0)
            self.flay.addWidget(self.fLive_cb[self.fcnt],3+(4*self.fcnt),1)
            self.flay.addWidget(self.fAdd_btn,3+(4*self.fcnt),2)
            
            self.flay.setRowStretch((self.flay.rowCount()*(4-self.fcnt)),1)
            
        else:
            QMessageBox.information(self,"경고","5명이상 등록하실 수 없습니다.")
        
    
    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Regist() 
    myWindow.show() 
    app.exec_() 