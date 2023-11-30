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
        
        #DB 연결
        #self.conn = pymysql.connect(
        #    host='localhost',
        #    user='dev',
        #    password='nori1234',
        #    db='dev',
        #    port=3306,
        #    charset='utf8'
        #)
        #self.cur = self.conn.cursor()
        

    
    #편집 저장완료시 필수정보 확인 by김태균
    def userReg(self):
        self.namekr = self.namekr_lineEdit.text()
        self.personnum = self.personnum_lineEdit.text()
        self.nameEng = self.nameEng_lineEdit.text()
        self.Emp_Number = self.Emp_Number_lineEdit.text()
        self.phonennum = self.phonennum_lineEdit.text()
        self.address1 = self.address1_lineEdit.text()
        self.address2 = self.address2_lineEdit.text()
        
        if(len(self.namekr)==0 or len(self.personnum)==0 or len(self.nameEng)==0 or len(self.Emp_Number)==0 or len(self.phonennum)==0 or len(self.address1)==0 or len(self.address2)==0 ):
            QMessageBox.warning(self, 'Regist failed','모든 항목을 입력하셔야 합니다.')
        else:
            if (len(self.namekr)<2): # 이름 글자수 조건
                QMessageBox.warning(self,'Sign up Failed','이름은 최소 두 글자입니다.')
                return
            elif (len(self.namekr)>4):
                QMessageBox.warning(self,'Sign up Failed','이름은 최대 네 글자입니다.')
                return
            elif (re.sub(r"[가-힣]","",self.namekr) != ''):
                QMessageBox.warning(self,'Sign up Failed','이름은 영문자, 자음, 모음이 입력될 수 없습니다. ')
                return
            else:
                if (len(self.personnum)<13): #주민등록번호 글자수 조건
                    QMessageBox.warning(self,'Person number Failed','하이폰(-) 없이 주민번호 13자리를 입력해야 합니다. ')
                    return
                else:
                    if(len(self.phonennum)>11): #휴대폰번호 글자수 조건
                        QMessageBox.warning(self,'Phone number Failed','하이폰(-) 없이 휴대폰번호 11자리를 입력해야 합니다. ')
                        return
                    else:
                        if emptyYN is None: #사번 밑으로는 권한 확인차 미완성
                            QMessageBox.warning(self,'Sign up Failed','등록되지 않은 사번입니다.\n관리자에게 문의바랍니다.')
                            return
                        else: 
                            query ='select id from login_data where emp_num = ' + self.emp_num +';'
                            self.cur.execute(query)
                            emptyYN = self.cur.fetchone()
                            if emptyYN is not None:
                                QMessageBox.warning(self,'Sign up Failed','사원님의 ID가 이미 존재합니다.')
                                return
                            else:
                                query ='insert into login_data values(%s,%s,%s,%s);'
                                self.cur.execute(query, (self.id,self.passwd,self.emp_num,'user'))
                                # self.conn.commit()
                                self.conn.close()   
                    
                        
                
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
    myWindow = Regist() 
    myWindow.show() 
    app.exec_() 