import os
import sys
import typing

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from emp_list import Emplist
from emp_info import EmpInfo
from emp_regist import Regist
from edu_list import EduList
from sign_up import SignUp

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('Index.ui')
form_class = uic.loadUiType(form)[0]

class Index(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        
        self.flag = 0
        
        self.tree.expandAll()
        self.Index.setLayout(self.indexLayout)

        self.empBtn.clicked.connect(self.showList)
        self.eduBtn.clicked.connect(self.showEdu)
        self.tree.itemClicked.connect(self.onItemClicked)
        
        self.userRegBtn.clicked.connect(self.showSign)
        
    
    # 231122 페이지 전환 함수 by정현아    
    def showList(self):
        self.w = Emplist()
        self.w .show()
        self.hide()
        self.w.listCnlBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)

        
    def showInfo(self):
        self.w = EmpInfo()
        self.w .show()
        self.hide()
        self.w.infoCnlBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)

    def showReg(self):
        self.w = Regist()
        self.w .show()
        self.hide()
        self.w.regCnlBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)

    def showEdu(self):
        self.w = EduList()
        self.w .show()
        self.hide()
        self.w.eduCnlBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)
        
    def showSign(self):
        self.w = SignUp()
        self.w.show()
        self.w.cnlBtn.clicked.connect(self.w.close)

    def back(self):
        self.w.hide()
        self.show()
    
    # 231122 트리뷰 선택시 페이저 변경 by 정현아
    def onItemClicked(self, item, row):
        text = item.text(row)     
        if text == '사원정보목록':
            self.showList()
        elif text == '나의 정보':
            self.showInfo()
        elif text == '사원정보편집':
            self.showReg()
        else: 
            self.showEdu()
            
    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)


         
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Index() 
    myWindow.show() 
    app.exec_() 