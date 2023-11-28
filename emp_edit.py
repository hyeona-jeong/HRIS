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

form = resource_path('emp_edit.ui')
form_class = uic.loadUiType(form)[0]

class Edit(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        #그룹박스내에 생성창 리스트
        self.regist.setLayout(self.regLayout)
        
        
        self.addImgBtn.clicked.connect(self.showAddImg)

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
        self.saveBtn.clicked.connect(self.userReg)
        
        #주민번호, 휴대폰번호 정수만 입력되게 제한
        #regExp = QRegExp("[0-9]*")
        #self.personnum_lineEdit.setValidator(QIntValidator(regExp, self))
        #self.phoneNum_lineEdit.setValidator(QIntValidator(regExp, self))
        
        #self.conn = pymysql.connect(
        #    host='192.168.2.20',
        #    user='dev',
        #    password='nori1234',
        #    db='dev',
        #    port=3306,
        #    charset='utf8'
        #)
        


    
    #편집 저장완료시 필수정보 확인 by김태균
    def userReg(self):
        self.phoneNum = self.phoneNum_lineEdit.text()
        self.address1 = self.address1_lineEdit.text()
        self.address2 = self.address2_lineEdit.text()
        
        if(len(self.phoneNum)==0 or len(self.address1)==0 or len(self.address2)==0 ):
            QMessageBox.warning(self, 'Regist failed','모든 항목을 입력하셔야 합니다.')
            return
        else:
            query ='update into main_table values(%s,%s,%s,%s);'
            self.cur.execute(query, (self.phoneNum,self.address1,self.address2,'user'))
            # self.conn.commit()
            self.conn.close()
            QMessageBox.information(self,'Edit Succeed','편집 완료되었습니다.')
            
 
                    
                        
                
    # 231123 페이지 전환 함수 by 정현아    
    def showAddImg(self):
        self.w = AddImg()
        self.w.show()
        self.w.cnlBtn.clicked.connect(self.w.close)
        
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


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Edit() 
    myWindow.show() 
    app.exec_() 