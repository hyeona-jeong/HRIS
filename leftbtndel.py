import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ######UI 세팅########
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem('Apple'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Banana'))
        self.tableWidget.setItem(1, 0, QTableWidgetItem('Orange'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem('Grape'))

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.setWindowTitle('PyQt5 - QTableWidget')
        self.setGeometry(300, 100, 600, 400)
        self.show()
        ######################
        

        # 메뉴바 활성화
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        # 우클릭시 메뉴바 생성
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)

        # 만약 다른 클릭으로 메뉴바 생성하고 싶다면
        # self.tableWidget.viewport().installEventFilter(self)

    # installEventFilter사용시 작동(실시간을 요구하기때문에 과부하 많이 걸림)
    def eventFilter(self, source:QtCore.QObject, event:QtCore.QEvent):    
        
        # 마우스 더블클릭시
        if(
            event.type() == QtCore.QEvent.Type.MouseButtonDblClick and
            event.buttons() == QtCore.Qt.MouseButton.LeftButton and
            source is self.tableWidget.viewport()
        ):
            self.generateMenu(event.pos())
        
        
        return super(MyApp, self).eventFilter(source, event)
            

    def generateMenu(self, pos):
        # 빈공간에서
        if(self.tableWidget.itemAt(pos) is None):
            self.emptymMenu = QMenu(self)
            self.emptymMenu.addAction("추가", self.addRow)      
            self.emptymMenu.exec_(self.tableWidget.mapToGlobal(pos)) 
            
        # 아이템에서
        else:
            self.menu = QMenu(self)
            self.menu.addAction("삭제",lambda: self.deleteRow(pos))      
            
            self.menu.exec_(self.tableWidget.mapToGlobal(pos)) 

    def addRow(self):
        print("추가")
        # 마지막줄에 추가하기 위함
        rowPosition =self.tableWidget.rowCount()
        columnPosition =self.tableWidget.columnCount()
        
        self.tableWidget.insertRow(rowPosition)
        
        # 모든 열에 세팅
        for column in range(columnPosition):
            self.tableWidget.setItem(rowPosition,column,QTableWidgetItem(''))
        
        
    def deleteRow(self,pos):
        print("삭제",pos)
        self.tableWidget.removeRow(self.tableWidget.indexAt(pos).row())
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())