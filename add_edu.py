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

class DialogClass(QDialog, form_class):
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
        self.addT.setStyleSheet(stylesheet)
        self.saveBtn.clicked.connect(self.saveData)

    # 231211 테이블에 입력된 정보 리스트에 저장 by 정현아
    def saveData(self):
        rows = self.addT.rowCount()
        cols = self.addT.columnCount()

        for row in range(rows):
            data = []
            for col in range(cols):
                item = self.addT.item(row, col)
                if item is None or item.text() == '':
                    if col == 0:
                        return
                    else : 
                        QMessageBox.warning(self, "입력실패", "모든 내용을 입력해주셔야합니다.")
                        return
                else:
                    if col == 0 and row != 0:
                        if not(item.text().isdigit()):
                            QMessageBox.warning(self, "입력실패", "숫자를 입력해주셔야합니다.")
                            return
                        else: 
                            query = "SELECT * FROM MAIN_TABLE WHERE EMP_NUM = %s"
                            self.cur.execute(query,(int(item.text())))
                            result = self.cur.fetchone()
                            if not result :
                                QMessageBox.warning(self, "입력실패", f"{row+1}행 {col+1}열의 {item.text()} 존재하는 사번이 없습니다.")
                                return
                            else:
                                data.append(int(item.text()))
                    elif col == 3:
                        if not(item.text() == 'Y' or item.text() == 'N' or item.text() == 'y' or item.text() == 'n') :
                            QMessageBox.warning(self, "입력실패", f"{row+1}행 {col+1}열의 교육이수 여부값이 잘못 입력됐습니다. \n Y 또는 N을 입력해주세요.")
                            return
                        elif item.text() == 'y' or item.text() == 'n':
                            data.append(item.text().upper())
                        else: 
                            data.append(item.text())
                    else:
                            data.append(item.text())
            self.saveToDatabase(data, row)

    # 231211 테이블에 입력된 정보 DB에 INSERT by 정현아
    def saveToDatabase(self, data,row):
        try:
            query = "SELECT * FROM E_C WHERE EMP_NUM = %s AND NAME_EDU = %s AND EDU_INSTI = %s"
            self.cur.execute(query, (int(data[0]), data[1], data[2]))
            result = self.cur.fetchone()
            if result :
                QMessageBox.warning(self, "입력실패", f"{row+1}행에 이미 등록된 정보가 있습니다.")
                return
            query = "INSERT INTO E_C  VALUES (%s, %s, %s, %s)"
            self.cur.execute(query, tuple(data))
            self.conn.commit()
            QMessageBox.information(self, "입력 성공", "저장되었습니다.")
            
        except Exception as e:
            QMessageBox.warning(self, "입력실패", f"{e}")
            print(e)
            return
        self.initTable()
    
    # 231211 INSERT 후 테이블 초기화 by 정현아
    def initTable(self):
        for row in range(10):
            for col in range(self.addT.columnCount()):
                item = QTableWidgetItem("")
                self.addT.setItem(row, col, item)        

stylesheet = """
    QHeaderView::section{
        Background-color:#c6c6c6;
    }
"""
                    
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = DialogClass( ) 
    myWindow.show( ) 
    app.exec_( ) 