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
from user_auth import UserAuth
from forum_list import Forum
from qa_list import Q_A


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
    listToInfo = pyqtSignal()
    indexToForum = pyqtSignal()
    indextToQA = pyqtSignal()

    def __init__(self, emp_num, auth):
        super().__init__()
        self.setupUi(self)
        self.auth = None
        self.w = None
        self.emp_num = emp_num
        self.auth = auth
        
        self.index.setStyleSheet(stylesheet)

        # 메뉴바 생성
        self.menuBar = QMenuBar()
        font = QFont("Malgun Gothic", 16)
        font.setBold(True)
        self.menuBar.setFont(font)
        self.menuBar.setStyleSheet("QMenu { spacing: 40px; }")
        self.hbox.insertWidget(0, self.menuBar)

        # 231125 메뉴바에 액션 추가
        self.toolhr = self.menuBar.addAction('인사')
        self.tooledu = self.menuBar.addAction('교육')
        self.toolforum = self.menuBar.addAction('게시판',self.showPage)
        self.toolqa = self.menuBar.addAction('Q&&A',self.showPage)
        self.toolrc = self.menuBar.addAction('채용')
        self.toolbm = self.menuBar.addAction('사업관리')
        self.toolga = self.menuBar.addAction('총무')
        
        # 231125 메뉴바에 메뉴 추가 
        self.menuHr = QMenu()
        self.menuHr.addAction('사원정보검색',self.showPage)
        self.menuHr.addAction('개인정보조회/편집',self.showPage)
        self.menuHr.addAction('사원정보등록',self.showPage)
        self.menuHr.addAction('사원ID등록',self.showIDRegist)
        self.menuHr.addAction('사용자권한관리',self.showPage)
        self.toolhr.setMenu(self.menuHr)
        self.menuHr.setStyleSheet(stylesheet)

        menuEdu = QMenu()
        menuEdu.addAction('교육이수정보 조회',self.showPage)
        menuEdu.setStyleSheet(stylesheet)

        self.tooledu.setMenu(menuEdu)
        self.empBtn.clicked.connect(self.showPage)
        self.eduBtn.clicked.connect(self.showPage)

        # 스타일 시트 설정
        self.menuBar.setStyleSheet(stylesheet)
        
    # 231126 버튼 별로 화면 페이지 구분하여 페이지 전환 by 정현아
    def showPage(self):
        sender = self.sender().text()

        if sender == '사원정보검색' or sender == '인사':
            self.w = Emplist()
            self.showedList.emit()
            self.w.listToInfo.connect(self.listToInfo.emit)
            
        elif sender == '개인정보조회/편집': 
            self.w = EmpInfo()
            self.showedInfo.emit()
            self.w.showedEdit.connect(self.showedEdit.emit)
            
        elif sender == '사원정보등록':
            self.w = Regist()
            self.showedRegist.emit()
            
        elif sender == '교육' or sender == '교육이수정보 조회':
            self.w = EduList()
            
        elif sender == '사용자권한관리':
            self.w = UserAuth()
        
        elif sender == '게시판':
            self.w = Forum(self.emp_num)
            self.indexToForum.emit()
            self.w.forumToWrite.connect(self.indexToForum.emit)
            self.w.forumToRead.connect(self.indexToForum.emit)
        
        elif sender == 'Q&&A':
            self.w = Q_A(self.emp_num, self.auth)
            self.indextToQA.emit()
            self.w.qaToWrite.connect(self.indextToQA.emit)
            self.w.qaToRead.connect(self.indextToQA.emit)
            
        self.w.show()
        self.hide()
        self.w.cnlBtn.clicked.connect(self.w.close)
        self.w.closed.connect(self.show)            
    
    def showIDRegist(self):
        self.w = SignUp()
        self.w.cnlBtn.clicked.connect(self.w.accept)
        result = self.w.exec_()  

    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

stylesheet = """
    QMenuBar {
        color: #161616;
    }
    QMenuBar::item {
        padding-left: 20px;
        padding-right: 20px;
        padding-bottom: 15px;
        margin-right: 5px;
        margin-left: 5px;
    }
    QMenuBar::item::selected {
        border-bottom: 3px solid ;
    }
    QMenu{
        background-color:#c8c8c8;
        color: #404040;
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


