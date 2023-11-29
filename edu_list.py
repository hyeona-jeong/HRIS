import os
import sys
import openpyxl
import pymysql

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
        self.eduList.setStyleSheet(stylesheet)
        
        # 변경된 셀값 저장
        self.chLists = []
        self.flag = 0
        self.eduList.setLayout(self.eduListLayout)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  

        self.bizCombo.activated[str].connect(self.searchBiz)
        self.namelineEdit.returnPressed.connect(self.searchEmp)
        self.empSearchBtn.clicked.connect(self.searchEmp)
        
        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)    
        
        self.addBtn.clicked.connect(self.addEdu)
        self.excelBtn.clicked.connect(self.addExcel)

        self.conn = pymysql.connect(
                host='192.168.2.20',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        self.cur = self.conn.cursor()
        
        query = """
        SELECT @rownum:=@rownum+1, MAIN_TABLE.EMP_NUM,DEPT_BIZ,DEPT_GROUP,NAME_KOR,NAME_EDU,EDU_INSTI,COMP_YN 
        FROM MAIN_TABLE,E_C, (SELECT @rownum:=0) TMP
        WHERE MAIN_TABLE.EMP_NUM = E_C.EMP_NUM;
        """
        self.cur.execute(query)
        self.result = self.cur.fetchall()
        # 231128 table 세팅 by 정현아
        self.table.setRowCount(0)
        self.setTableItem(self.result)
        # self.table.itemChanged.connect(self.chCell)
        # self.saveBtn.clicked.connect(self.updateCell)
        
    # 231128 table 세팅함수 by 정현아
    def setTableItem(self,result):
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 0:
                    self.table.setItem(row_number,column_number,QTableWidgetItem(str(int(data))))
                else:
                    self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        
        # 231128 table item 텍스트 중앙 정렬 및 7번 컬럼 제외한 컬럼 편집불가 처리
        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                self.table.item(r,c).setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                if c == 0 or c == 1 or c == 2 or c == 3 or c == 4:
                    self.table.item(r,c).setFlags(self.table.item(r,c).flags() & ~ (Qt.ItemIsEditable))


    # 231129 사업부검색 함수 
    def searchBiz(self,biz):
        self.biz = biz
        query = """
        SELECT @rownum:=@rownum+1, MAIN_TABLE.EMP_NUM,DEPT_BIZ,DEPT_GROUP,NAME_KOR,NAME_EDU,EDU_INSTI,COMP_YN 
        FROM MAIN_TABLE,E_C, (SELECT @rownum:=0) TMP
        WHERE MAIN_TABLE.EMP_NUM = E_C.EMP_NUM AND DEPT_BIZ = \'""" + biz +'\';'
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.setTableItem(result)
        
    # 231129 사원검색 함수
    def searchEmp(self):
        name = self.namelineEdit.text()
        if name == '' : 
            return
        query = """
        SELECT @rownum:=@rownum+1, MAIN_TABLE.EMP_NUM,DEPT_BIZ,DEPT_GROUP,NAME_KOR,NAME_EDU,EDU_INSTI,COMP_YN 
        FROM MAIN_TABLE,E_C, (SELECT @rownum:=0) TMP
        WHERE MAIN_TABLE.EMP_NUM = E_C.EMP_NUM AND DEPT_BIZ = %s AND NAME_KOR LIKE %s;
        """
        self.cur.execute(query,(self.biz,name+'%'))
        result = self.cur.fetchall()
        self.setTableItem(result)
        
    
    def onHeaderClicked(self, logicalIndex):
        if(logicalIndex != 7):
            return
        elif(self.flag == 0):
            self.filter()
        elif(self.flag == 1):
            self.cnlFilter()
            self.flag -=1

    # 231118필터링 팝업창 생성 by 정현아
    def filter(self):
        dialog = QInputDialog(self)
        dialog.setOkButtonText("검색")
        dialog.setCancelButtonText("취소")
        dialog.setLabelText("검색어를 입력하세요(Y,N)")
        dialog.setWindowTitle("이수여부 검색")
        if dialog.exec_() == QDialog.Accepted:
            self.table.setHorizontalHeaderItem(7, QTableWidgetItem('이수여부☑')) 
            text = dialog.textValue()
            self.flag+=1
            query ="""
            SELECT @rownum:=@rownum+1, MAIN_TABLE.EMP_NUM,DEPT_BIZ,DEPT_GROUP,NAME_KOR,NAME_EDU,EDU_INSTI,COMP_YN 
            FROM MAIN_TABLE,E_C, (SELECT @rownum:=0) TMP
            WHERE MAIN_TABLE.EMP_NUM = E_C.EMP_NUM AND COMP_YN = '""" + text + '\';'
            self.cur.execute(query)
            result = self.cur.fetchall()
            self.setTableItem(result)
                    
    # 231118 필터링 해제 by 정현아                
    def cnlFilter(self):
        self.table.setHorizontalHeaderItem(7, QTableWidgetItem('이수여부☐'))   
        query = """
        SELECT @rownum:=@rownum+1, MAIN_TABLE.EMP_NUM,DEPT_BIZ,DEPT_GROUP,NAME_KOR,NAME_EDU,EDU_INSTI,COMP_YN 
        FROM MAIN_TABLE,E_C, (SELECT @rownum:=0) TMP
        WHERE MAIN_TABLE.EMP_NUM = E_C.EMP_NUM;
        """  
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.setTableItem(result)


    # 231120 입력 팝업창 생성 by 정현아
    def addEdu(self):
        self.w = dialogClass()
        self.w.show()
        self.w.cnlBtn.clicked.connect(self.w.close)

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
                    row[5].value,
                    row[6].value
                ])

            self.w = dialogClass()
            self.w.addT.setRowCount(len(data)-1)
            for r in range(1,len(data)):
                for c in range(0,7):
                    self.w.addT.setItem(r-1,c,QTableWidgetItem(str(data[r][c])))
            self.w.show()
        else: pass
    # 231129 셀값 변경시 리스트에 저장 by 정현아
    # def chCell(self, item):
    #     chList = []
    #     chList.append(item.row())
    #     chList.append(item.column())
    #     chList.append(item.text())
    #     item.setBackground(QColor(255,255,127))
    #     self.chLists.append(chList)
    
    # 231129 버튼 클릭시 변경한 셀값 업데이트
    # def updateCell(self):
    #     if not self.chLists:
    #        QMessageBox.warning(self,"Update Item Failed","변경된 정보가 없습니다.") 
    #        return
    
    #     else:
    #         for chList in self.chLists:
    #             r = chList[0]
    #             c = chList[1]
    #             cont = chList[2]
    #         if cont == '' :
    #             QMessageBox.warning(self,"Update Item Failed","빈 값을 넣으실 수 없습니다.")
    #             return
    #         elif c==7 and not(cont == 'Y' or cont == 'N' or cont == 'y'or cont == 'n' ):
    #             QMessageBox.warning(self,"Update Item Failed","이수여부에는 Y 또는 N만 입력가능합니다.")
    #             return
    #         else:
    #             if(c==5):
    #                 query = 'UPDATE E_C SET NAME_EDU = %s WHERE EMP_NUM = %s AND NAME_EDU = %s'
    #                 self.cur.execute(query,(cont,int(self.result[r][1]),self.result[r][5]))
    #             elif(c==6):
    #                 query = 'UPDATE E_C SET EDU_INSTI = %s WHERE EMP_NUM = %s AND NAME_EDU = %s'
    #                 self.cur.execute(query,(cont,int(self.result[r][1]),self.result[r][5]))
    #             elif(c==7):
    #                 if(cont.islower()):
    #                     cont = cont.upper()
    #                 query = 'UPDATE E_C SET COMP_YN = %s WHERE EMP_NUM = %s AND NAME_EDU = %s'
    #                 self.cur.execute(query,(cont,int(self.result[r][1]),self.result[r][5]))
    #             self.conn.commit()
    #         self.chList = []
    #         QMessageBox.information(self,"Update Item Succeed","업데이트 되었습니다.") 
    #         query = """
    #         SELECT @rownum:=@rownum+1, MAIN_TABLE.EMP_NUM,DEPT_BIZ,DEPT_GROUP,NAME_KOR,NAME_EDU,EDU_INSTI,COMP_YN 
    #         FROM MAIN_TABLE,E_C, (SELECT @rownum:=0) TMP
    #         WHERE MAIN_TABLE.EMP_NUM = E_C.EMP_NUM;
    #         """
    #         self.cur.execute(query)
    #         result = self.cur.fetchall()
    #         self.setTableItem(result)
            
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
    myWindow = EduList() 
    myWindow.show() 
    app.exec_() 