import os
import sys
import pymysql

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
        self.empList.setLayout(self.listLayout)
        self.setStyleSheet(stylesheet)

        self.table.setRowCount(0)
        self.table.setRowCount(8)
        header = ['','부서','이름','직무','직급','직책','휴대폰번호','메일']
        self.table.setHorizontalHeaderLabels(header)

        self.conn = pymysql.connect(
            host='localhost',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
        )
        self.cur = self.conn.cursor()
        query = "SELECT CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_KOR, POSITION, EMP_RANK, WORK_POS, PHONE, MAIL FROM MAIN_TABLE"
        self.cur.execute(query)
        result = self.cur.fetchall()
        for row, row_data in enumerate(result):
            self.table.insertRow(row)

            # 231202 첫열에 체크박스 삽입 및 중앙정렬 by 정현아
            cell_widget = QWidget()
            chk_bx = QCheckBox()
            chk_bx.setCheckState(False) 
            lay_out = QHBoxLayout(cell_widget)
            lay_out.addWidget(chk_bx)
            lay_out.setAlignment(Qt.AlignCenter)
            lay_out.setContentsMargins(0,0,0,0)
            cell_widget.setLayout(lay_out)
            self.table.setCellWidget(row, 0, cell_widget)

            for col, data in enumerate(row_data):
                self.table.setItem(row,col+1,QTableWidgetItem(str(data)))     
                if self.table.item(row,col+1) is not None:
                    self.table.item(row,col+1).setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)           

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   
        self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7,QHeaderView.ResizeToContents)

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