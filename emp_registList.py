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
        self.tabWidget.setMovable(True)

        # 231203 가족관계탭 생성 및 스크롤 영억 세팅 by 정현아
        self.layout = QVBoxLayout()
        self.family = QScrollArea()
        self.tabWidget.addTab(self.family,'가족관계')
        
        # 231203 가족 관계 생성창이 몇개있는지 카운트. by 정현아
        self.fcnt = 0
        # 231203 스크롤 영역에 위젯 세팅 및 girdlayout세팅 
        self.fwidget = QWidget()
        self.family.setWidget(self.fwidget)
        self.flay = QGridLayout(self.fwidget)
        self.family.setWidgetResizable(True)
        self.widget_attributes = []
        self.fAdd_btn = QPushButton("추가")
        self.initFamilyInfo()

        self.fAdd_btn.clicked.connect(self.addfamily)
        
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
                        
                
    # 231123 페이지 전환 함수 by 정현아    
    def showAddImg(self):
        self.w = AddImg()
        self.w.show()
        self.w.cnlBtn.clicked.connect(self.w.close)
        
    # 231115 가족 정보 추가작성을 위해 새로운 작성폼 생성 by 정현아        
    def initFamilyInfo(self):
        widget_types = [
            ("가족성명", QLineEdit, None),
            ("생년월일", QDateEdit, None),
            ("관계", QComboBox, ['부', '모', '형제', '배우자', '자녀', '조부', '조모', '외조부', '외조모', '빙부', '빙모']),
            ("동거여부", QComboBox, ['Y', 'N']),
        ]

        for i, (label_text, widget_type, items) in enumerate(widget_types):
            label = QLabel(label_text, self)
            widget = widget_type(self)
            if widget_type == QComboBox and items:
                widget.addItems(items)

            setattr(self, f'f{label_text}_lbl', label)
            setattr(self, f'f{label_text}_le', widget)

            row = i * 4
            self.flay.addWidget(label, row, 0)
            self.flay.addWidget(widget, row, 1)
            if  i == 3:
                self.flay.addWidget(self.fAdd_btn, row, 2)
            self.widget_attributes.append({'label': label, 'widget': widget})
        
        self.flay.setRowStretch((self.flay.rowCount() * (4 - self.fcnt)), 1)

    def addfamily(self):
        if self.fcnt <= 3:
            self.fcnt += 1
            print(self.fcnt)

    def addFamilyInfo(self):
        
    
    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Regist() 
    myWindow.show() 
    app.exec_() 