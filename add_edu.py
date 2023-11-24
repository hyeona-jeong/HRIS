import os
import sys

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
        
        # for r in range(self.addT.rowCount()):
        #     cell_widget = QComboBox()
        #     cell_widget.addItem('')
        #     cell_widget.addItem('Y')
        #     cell_widget.addItem('N')
    
        #     self.addT.setCellWidget(r, 3, cell_widget)
            
        self.addT.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.addT.customContextMenuRequested.connect(self.generateMenu)
        
    def eventFilter(self, source:QObject, event:QEvent):    
        
        # 마우스 더블클릭시
        if(
            event.type() == QEvent.Type.MouseButtonDblClick and
            event.buttons() == Qt.MouseButton.LeftButton and
            source is self.addT.viewport()
        ):
            self.generateMenu(event.pos())
        
        
        return super(dialogClass, self).eventFilter(source, event)
            

    def generateMenu(self, pos):
        # 빈공간에서
        if(self.addT.itemAt(pos) is None):
            pass
            
        # 아이템에서
        else:
            self.menu = QMenu(self)
            self.menu.addAction("삭제",lambda: self.deleteRow(pos))      
            
            self.menu.exec_(self.addT.mapToGlobal(pos)) 
            
    def deleteRow(self,pos):
        print("삭제",pos)
        self.addT.removeRow(self.addT.indexAt(pos).row())
         
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = dialogClass( ) 
    myWindow.show( ) 
    app.exec_( ) 