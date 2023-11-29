import os
import sys
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('add_edu.ui')
form_class = uic.loadUiType(form)[0]

class dialogClass(QDialog, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.addT.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        
        self.conn = pymysql.connect(
                host='192.168.2.20',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        self.cur = self.conn.cursor()
        
        # 231129 변경된 정보를 저장하기 위한 리스트
        self.chLists = []
        
        # self.addT.itemChanged.connect(self.chCell)
        # self.saveBtn.clicked.connect(self.updateCell)
        
    # 231129 셀 업데이트마다 정보저장 by 정현아
    # def chCell(self, item):
    #     chList = []
    #     chList.append(item.row())
    #     chList.append(item.column())
    #     chList.append(item.text())
    #     self.chLists.append(chList)
        
    #     if item.column() == 0:
    #         emp_num = item.text()
    #         query = 'SELECT EMP_NUM, DEPT_BIZ, DEPT_GROUP, NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM =%s;'
    #         self.cur.execute(query,(emp_num))
    #         result = self.cur.fetchone()
    #         if(result is not None):
    #             for col, data in enumerate(result):
    #                 self.addT.setItem(item.row(),col,QTableWidgetItem(str(data)))
            
    # # 231129 셀 변경내용 DB Insert by 정현아
    # def updateCell(self):
    #     if not self.chLists:
    #        QMessageBox.warning(self,"Update Item Failed","변경된 정보가 없습니다.") 
    #        return
    
    #     else:
    #         r = 0
    #         c = 0
    #         cont = ''
    #         for chList in self.chLists:
    #             r = chList[0]
    #             c = chList[1]
    #             cont = chList[2]
    #         for row in r:
    #             for col in self.addT.columnCount():
    #                 if self.addT.item(row,col) == '':
    #                     QMessageBox.warning(self,"Add Information Failed","모든 정보를 입력해주셔야 합니다.")
            
                    
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = dialogClass( ) 
    myWindow.show( ) 
    app.exec_( ) 