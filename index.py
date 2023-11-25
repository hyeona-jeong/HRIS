import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
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

form = resource_path('index.ui')
form_class = uic.loadUiType(form)[0]

class Index(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__()
        self.setupUi(self)

        self.index.setLayout(self.indexlayout)
        self.setStyleSheet(stylesheet)

        # 231125 툴버튼에 메뉴 추가 
        menuHr = QMenu()
        menuHr.addAction('사원정보목록',self.showList)
        menuHr.addAction('사원개인정보',self.showInfo)
        menuHr.addAction('사원정보편집',self.showReg)

        menuHr.setStyleSheet(stylesheet)
        self.toolhr.setMenu(menuHr)

        menuEdu = QMenu()
        menuEdu.addAction('교육이수정보')
        menuEdu.setStyleSheet(stylesheet)

        self.tooledu.setMenu(menuEdu)

        self.toolhr.setPopupMode(QToolButton.InstantPopup)

        self.toolhr.triggered.connect(self.action)

        self.empBtn.clicked.connect(self.showList)
        self.eduBtn.clicked.connect(self.showEdu)



                
        


    def action(self):
        print('action bim')


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
        
    # def showSign(self):
    #     self.w = SignUp()
    #     self.w.show()
    #     self.w.cnlBtn.clicked.connect(self.w.close)

    def back(self):
        self.w.hide()
        self.show()

    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)
         

stylesheet = """
    QToolButton::menu-indicator { 
        image: none;
        padding-right: 3px
    }
    QMenu{
        background-color: #ff5500;
        color: #c6c6c6;
        font-size: 20px;
        font-family: Malgun Gothic;
        width: 200px;
    }
    QMenu::item:selected{
        color: white; 
    }
"""
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Index( ) 
    myWindow.show( ) 
    app.exec_( ) 


