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

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('index.ui')
form_class = uic.loadUiType(form)[0]

class Index(QMainWindow, form_class):
    closed = pyqtSignal()
    showedList = pyqtSignal()
    showedInfo = pyqtSignal()
    showedRegist = pyqtSignal()
    showedEdit = pyqtSignal()

    def __init__(self):
        super( ).__init__()
        self.setupUi(self)
        self.auth = None
        self.w = None
        
        self.index.setLayout(self.indexlayout)
        self.index.setStyleSheet(stylesheet)

        # 231125 툴버튼에 메뉴 추가 
        self.menuHr = QMenu()
        self.menuHr.addAction('사원정보검색',self.showPage)
        self.menuHr.addAction('개인정보조회/편집',self.showPage)
        self.menuHr.addAction('사원정보등록',self.showPage)

        self.menuHr.setStyleSheet(stylesheet)
        self.toolhr.setMenu(self.menuHr)

        menuEdu = QMenu()
        menuEdu.addAction('교육이수정보 조회/편집',self.showPage)
        menuEdu.setStyleSheet(stylesheet)

        self.tooledu.setMenu(menuEdu)
        self.empBtn.clicked.connect(self.showPage)
        self.eduBtn.clicked.connect(self.showPage)

        print(self.auth)
        
    # 231126 버튼 별로 화면 페이지 구분하여 페이지 전환 by 정현아
    def showPage(self):
        sender = self.sender().text()
        if sender == '사원정보검색' or sender == '인사':
            self.w = Emplist()
            self.showedList.emit()
            
        elif sender == '개인정보조회/편집': 
            self.w = EmpInfo()
            self.showedInfo.emit()
            self.w.showedEdit.connect(self.sendLogin)
            
        elif sender == '사원정보등록':
            self.w = Regist()
            self.showedRegist.emit()
            
        elif sender == '교육' or sender == '교육이수정보 조회/편집':
            self.w = EduList()
        self.w.show()
        # self.w.center()
        self.hide()
        self.w.cnlBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)            
        
    def sendLogin(self):
        self.showedEdit.emit()

    def back(self):
        self.w.close()
        self.show()

    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)
        
        
        
    # 231126 마우스가 버튼위에 위치하면 자동으로 메뉴가 보이게 하는 함수 by정현아 
    # def eventFilter(self, object, event):
    #     if event.type() == QEvent.HoverEnter:
    #         object.showMenu()
    #         return True
    #     elif event.type() == QEvent.HoverLeave:
    #         print( "mouseout!")
    #     return False

stylesheet = """
    QPushButton::menu-indicator { 
        image: none;
        padding-right: 3px;
    }
    QMenu{
        background-color: #ff5500;
        color: #c6c6c6;
        font-size: 16px;
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


