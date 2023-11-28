import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from emp_edit import Edit

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('emp_info.ui')
form_class = uic.loadUiType(form)[0]

class EmpInfo(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.flag = 0;
        
        self.empinfo.setLayout(self.empinfolayout)
        self.listChgbtn.clicked.connect(self.showRegist)
    #     self.tabWidget.hide()
    #     self.pushButton.clicked.connect(self.tab_show)
        
        
    # def tab_show(self):
    #     if(self.flag == 0):
    #         self.tabWidget.show()
    #         self.flag+=1
    #     else:
    #         self.tabWidget.hide()
    #         self.flag-=1
    
    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def back(self):
        self.w.hide()
        self.show()

    #편집 화면으로 전환
    def showRegist(self):
        self.w = Edit()
        self.w .show()
        self.hide()
        self.w.cnlBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)
        
    def back(self):
        self.w.hide()
        self.show()
         
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = EmpInfo( ) 
    myWindow.show( ) 
    app.exec_( ) 


