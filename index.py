import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic    
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from emp_list import Emplist      # 사원정보 검색
from emp_info import EmpInfo      # 사원 정보
from emp_regist import Regist     # 사원정보 등록
from edu_list import EduList      # 교육 이수 관리
from sign_up import SignUp        # 사원 ID 등록
from user_auth import UserAuth    # 사용자 권한 관리
from forum_list import Forum      # 게시판
from qa_list import Q_A           # QA
from grade_pychart import Grade_pychart    # 직급별 차트
from age_barchart import Age_barchart      # 연령별 차트
from pm_list import PMList                 # 관제관리
#from edu_pychart import Edu_pychart     # 학력별 차트
#from cert_pychart import Cert_pychart     # 자격증 차트



def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('index.ui')
#form = resource_path('index_test.ui')
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

    def __init__(self, emp_num, auth, user_info):
        super().__init__()
        self.setupUi(self)
        self.auth = None
        self.w = None
        self.emp_num = emp_num
        self.auth = auth
        self.user_info = user_info
        
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
        self.tooltotal = self.menuBar.addAction('통계현황')
        self.toolforum = self.menuBar.addAction('게시판',self.showPage)
        self.toolqa = self.menuBar.addAction('Q&&A',self.showPage)
        self.toolrc = self.menuBar.addAction('채용')
        self.toolbm = self.menuBar.addAction('사업관리')
        self.toolga = self.menuBar.addAction('총무')
        
        
        # 231125 인사 메뉴바에 메뉴 추가 
        self.menuHr = QMenu()
        self.menuHr.addAction('사원정보검색',self.showPage)
        self.menuHr.addAction('개인정보조회/편집',self.showPage)
        self.menuHr.addAction('사원정보등록',self.showPage)
        self.menuHr.addAction('사원ID등록',self.showIDRegist)
        self.menuHr.addAction('사용자권한관리',self.showPage)

        #통계현황 메뉴바에 메뉴 추가
        menuTotal = QMenu()
        menuTotal.addAction('연령별 현황',self.showPage)
        menuTotal.addAction('직급별 현황',self.showPage)
        #menuTotal.addAction('학력별 현황',self.showPage)
        #menuTotal.addAction('자격증 현황',self.showPage)
        menuTotal.setStyleSheet(stylesheet)
        self.tooltotal.setMenu(menuTotal)
        #구분선 추가
        #self.menuHr.addSeparator()
        
        #서브 메뉴 추가
        # file_submenu = self.menuHr.addMenu("조직관리                 ▶")
        # file_submenu.addAction('연령별 현황',self.showPage)
        # file_submenu.addAction('직급별 현황',self.showPage)
                
        self.toolhr.setMenu(self.menuHr)
        self.menuHr.setStyleSheet(stylesheet)

        menuEdu = QMenu()
        menuEdu.addAction('교육이수정보 조회',self.showPage)
        menuEdu.setStyleSheet(stylesheet)
        
        # 사업관리 메뉴바에 하위 메뉴 추가
        self.MenuBm = QMenu()
        self.MenuBm.addAction('과제관리',self.showPage)
        self.MenuBm.setStyleSheet(stylesheet)
        self.toolbm.setMenu(self.MenuBm)

        self.tooledu.setMenu(menuEdu)
        self.empBtn.clicked.connect(self.showPage)
        self.eduBtn.clicked.connect(self.showPage)
        self.pmBtn.clicked.connect(self.showPage)

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
            
        elif sender == '연령별 현황':
            self.w = Age_barchart()
        
        elif sender == '직급별 현황':
            self.w = Grade_pychart()
            
        #elif sender == '학력별 현황':
        #    self.w = Edu_barchart()
        
        #elif sender == '자격증 현황':
        #    self.w = Cert_pychart()
        
        elif sender == '과제관리' or sender == '사업관리':
            self.w = PMList(self.user_info)
        
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
