import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from emp_regist import Regist

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('emp_list.ui')
form_class = uic.loadUiType(form)[0]

class Emplist(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   
        self.table.horizontalHeader().setSectionResizeMode(6,QHeaderView.ResizeToContents)
        self.centralwidget.setLayout(self.listLayout)
        
        self.setStyleSheet(stylesheet)

        # 231122 행의 첫 열에 체크박스 생성함수 by 정현아
        # for r in range(self.table.rowCount()):
        #     cell_widget = QWidget()
        #     chk_bx = QCheckBox()
        #     chk_bx.setCheckState(Qt.Checked) 
        #     lay_out = QHBoxLayout(cell_widget)
        #     lay_out.addWidget(chk_bx)
        #     lay_out.setAlignment(Qt.AlignCenter)
        #     lay_out.setContentsMargins(0,0,0,0)
        #     cell_widget.setLayout(lay_out)
        #     self.table.setCellWidget(r, 0, cell_widget)


        self.listRegBtn.clicked.connect(self.showRegsit)

    # 231122 페이지 전환 함수 by정현아
    def showRegsit(self):
        self.w = Regist()
        self.w .show()
        self.hide()
        self.w.regCnlBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)
        
    def back(self):
        self.w.hide()
        self.show()

    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)
   
stylesheet = """
    QTableWidget {
        border-radius: 10px;
        background-color: #eeeeee;
        margin-top:20px;   
        margin-bottom:20px;       
        padding-left:20px;          
        padding-right:20px;
    }

    QTableWidget::item {
        background-color: #ffffff;
        margin-top: 5px;    
        margin-bottom:5px;      
        border-radius: 9px;
    }

    QTableWidget::item:selected {
        color: black;
    }

    QHeaderView::section{
        Background-color:#c6c6c6;
        border-radius:5px;
        margin-top:25px; 
        margin-bottom:5px;
    }
"""

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Emplist() 
    myWindow.show() 
    app.exec_() 