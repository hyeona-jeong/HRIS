import os
import sys
import openpyxl

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from add_edu import dialogClass

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('edu_list.ui')
form_class = uic.loadUiType(form)[0]

class EduList(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)

        self.header = ['사번','부서','이름','교육명','교육기관','이수여부']
        #flag로 필터링 여부 구분하기 위한 리스트
        self.flag = [0,0,0,0,0,0]
        #각 컬럼별 필터링 로우를 저장하기 위한 리스트
        self.hRow = [0,0,0,0,0,0]
        self.s = []

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents) 
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents) 
        
        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)    
        
        self.addBtn.clicked.connect(self.addEdu)
        self.excelBtn.clicked.connect(self.addExcel)

    # 231120 입력 팝업창 생성 by 정현아
    def addEdu(self):
        self.w = dialogClass()
        self.w.show()
        
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
        
    # 231118필터링 팝업창 생성 by 정현아
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

    # 231122 엑셀 데이터를 받아오는 함수 by 정현아
    def addExcel(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/Program Files', 'Excel file(*xlsx *xls)')
        if fname[0]:
            wb = openpyxl.load_workbook(fname[0],data_only=True)
            sheet = wb['Sheet1']
            data = list()
            for row in sheet.rows:
                data.append([
                    row[0].value,
                    row[1].value,
                    row[2].value,
                    row[3].value,
                    row[4].value,
                    row[5].value
                ])

            self.w = dialogClass()
            self.w.addT.setRowCount(len(data)-1)
            for r in range(1,len(data)):
                for c in range(0,6):
                    print((data[r][c]),end=" ")
                    self.w.addT.setItem(r-1,c,QTableWidgetItem(str(data[r][c])))
            self.w.show()
        else: pass

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
    app.setStyleSheet(stylesheet)
    myWindow = EduList() 
    myWindow.show() 
    app.exec_() 