import os
import sys
import pymysql
import pandas as pd

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from emp_regist import Regist
from emp_info import EmpInfo

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
        
        self.header = ['사업부','그룹','이름','직책','직급','직무','휴대폰번호','메일']
        self.flag = [0,0,0,0,0,0,0,0]
        #각 컬럼별 필터링 로우를 저장하기 위한 리스트
        self.hRow = [0,0,0,0,0,0,0,0]
        self.s = []
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   
        self.table.horizontalHeader().setSectionResizeMode(6,QHeaderView.ResizeToContents)
        self.table.cellClicked.connect(self.Cell_Click) # 셀 클릭시 함수 이벤트
        self.table.cellDoubleClicked.connect(self.Cell_DoubleClick) # 셀 더블클릭시 함수 이벤트
        self.centralwidget.setLayout(self.listLayout)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)# 목록 편집 막기
        self.setStyleSheet(stylesheet)
        #self.searchlineEdit.set
        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)
        
    def onHeaderClicked(self, logicalIndex):
        if(logicalIndex == 0):
            self.cnlFilter(logicalIndex)
        for i in range(1,7):
            if (logicalIndex == i):
                if (self.flag[logicalIndex-1] == 0):
                    self.filter(logicalIndex)
                else: 
                    self.flag[logicalIndex-1]-=1
                    self.cnlFilter(logicalIndex)
    def filter(self,index):
        self.s = []
        dialog = QInputDialog(self)
        dialog.setOkButtonText("검색")
        dialog.setCancelButtonText("취소")
        dialog.setLabelText("검색어를 입력하세요")
        dialog.setWindowTitle("상세검색")
        if dialog.exec_() == QDialog.Accepted:
            text = dialog.textValue()
            self.flag[index-1]+=1
            for r in range(self.table.rowCount()):
                item = self.table.item(r,index).text()
                self.table.setHorizontalHeaderItem(index, QTableWidgetItem(str(self.header[index-1]+'☑')))

                if(str(text) not in item):
                    self.s.append(r)
                    self.table.setRowHidden(r,True)
            self.hRow[index-1] = self.s

        # 이름 검색 필터
        # layout = QVBoxLayout()
        # layout.addWidget(self.table_widget)

        # central_widget = QWidget()
        # central_widget.setLayout(layout)
        # self.setCentralWidget(central_widget)

        # self.searchlineEdit = QLineEdit()
        # self.searchlineEdit.setPlaceholderText('이름을 입력하세요...')
        # self.searchlineEdit.textChanged.connect(self.filter_items)
        # self.layout.addWidget(self.searchlineEdit)

    # def filter_items(self):
    #     search_text = self.search_input.text().lower()
    #     self.list_widget.clear()

    #     names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva']  # 이름 목록을 원래의 목록으로 변경하세요.

    #     for name in names:
    #         if search_text in name.lower():
    #             self.list_widget.addItem(name)        

    # 231118 필터링 해제 by 정현아                
    def cnlFilter(self,index):
        if(index == 0):
            for r in range(self.table.rowCount()):
                self.table.setRowHidden(r,False)
            for c in range(1,self.table.columnCount()):
                self.table.setHorizontalHeaderItem(c, QTableWidgetItem(str(self.header[c-1]+'☐')))
                
        
        else:
            if(self.flag.count(1)>=1):
                self.table.setHorizontalHeaderItem(index, QTableWidgetItem(str(self.header[index-1]+'☐')))
                s1 = set(self.hRow[index-1])
                s2 = set()
                for i in range(0,6):
                    if(self.flag[i] == 1 and i != index-1):
                        s2 = set(self.hRow[i])
                        s2 = s1 - (s2 - (s1 - (s2&s1)))
                    for r in s2:
                        self.table.setRowHidden(r,False) 
            else:
                for r in range(self.table.rowCount()):
                    self.table.setRowHidden(r,False)
                for c in range(1,self.table.columnCount()):
                    self.table.setHorizontalHeaderItem(c, QTableWidgetItem(str(self.header[c-1]+'☐')))
                    
        
        #data = self.table


        self.listRegBtn.clicked.connect(self.showRegist)

        
        #테이블위젯 내에 모든 데이터 추출
        # self.conn = pymysql.connect(
        #     host='192.168.2.20',
        #     user='dev',
        #     password='nori1234',
        #     db='dev',
        #     port=3306,
        #     charset='utf8'
        # )
        # self.cur = self.conn.cursor()
        # self
        # query = "select (department, name_kor, postion, emp_rank, work_pos, phone, mail) from main_table"
        # self.cur.execute(query)
        # self.conn.commit()

        
                
    #셀 클릭시     
    def Cell_Click(self, row):
        #data = self.table.item(row,i-1)
        pass
        
    #231124 셀 더블클릭시 개인정보 페이지로 전환함수 by김태균    
    def Cell_DoubleClick(self):
        self.w = EmpInfo()
        self.w .show()
        self.hide()       
        self.w.cnlBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)
        
    def back(self):
        self.w.hide()
        self.show()

    # 231122 페이지 전환 함수 by정현아
    def showRegist(self):
        self.w = Regist()
        self.w .show()
        self.hide()
        self.w.cnlBtn.clicked.connect(self.back)

        
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