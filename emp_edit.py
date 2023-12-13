import os
import sys
import re
import pymysql
import requests

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('emp_edit.ui')
form_class = uic.loadUiType(form)[0]

class Edit(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        #그룹박스내에 생성창 리스트
        
        # 231206 우편번호는 찾기를 통해서만 입력가능 by 정현아
        self.addressnum_lineEdit.setReadOnly(True) 
        self.searchAddress.clicked.connect(self.searchPost)
    
    # 231206 우편번호 찾기 팝업창 생성 by 정현아
    def searchPost(self):
        self.w = QDialog(self)
        searchPost = uic.loadUi(resource_path('search_post.ui'), self.w)
        self.w.address_lineEdit.returnPressed.connect(self.findAddress)
        self.w.searchBtn.clicked.connect(self.findAddress)
        self.w.table.cellDoubleClicked.connect(self.selectPost)
        
        self.w.saveBtn.clicked.connect(self.acceptDialogResult)
        self.w.cnlBtn.clicked.connect(self.w.close)
        
        if self.w.exec_() == QDialog.Accepted:
            pass
        
    # 231206 우편번호 찾기 후 찾은 내용 라인에디터에 세팅 by 정현아
    def acceptDialogResult(self):
        self.w.setResult(QDialog.Accepted)
        self.addressnum_lineEdit.setText(self.post_num)
        self.address_lineEdit.setText(self.post_address)    
        self.w.close()
        
    # 231206 오픈 API를 통해 우편번호 찾기 by 정현아
    def findAddress(self):
        post_num = []
        post_address = []
        self.w.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
        self.w.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)

        address = self.w.address_lineEdit.text()
        # 도로명 주소로 검색하고 도로명 주소 결과가 없으면 지번 주소로 다시 검색 by 정현아
        url = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd'
        params = {
            'serviceKey': '7kEsxVN9P4SCOTTBAmWPvKJQDrhW4i08XbJe98mkPpthjKeB6bQjiDMSEJuNHVroSg3sx8OUYLaeSIe1J1tSsw==',
            'searchSe': 'road',
            'srchwrd': '',
            'countPerPage': '50',
            'currentPage': '1'
        }
        params['srchwrd'] = address

        response = requests.get(url, params=params).text.encode('utf-8')
        xmlobj = BeautifulSoup(response, 'lxml-xml')

        post = xmlobj.find_all('zipNo')
        post2 = xmlobj.find_all('lnmAdres')
        row = len(post)

        if(row != 0):
            self.w.table.setRowCount(row)
            for p in post:
                post_num.append(p.getText())
            for p in post2 :
                post_address.append(p.getText())
            for r in range(row):
                self.w.table.setItem(r, 0, QTableWidgetItem(str(post_num[r])))
                self.w.table.setItem(r, 1, QTableWidgetItem(str(post_address[r])))
        else:
            params['searchSe'] = 'dong'
            response = requests.get(url, params=params).text.encode('utf-8')
            xmlobj = BeautifulSoup(response, 'lxml-xml')

            post = xmlobj.find_all('zipNo')
            post2 = xmlobj.find_all('lnmAdres')
            row = len(post)

            if(row != 0):
                self.w.table.setRowCount(row)
                for p in post:
                    post_num.append(p.getText())
                for p in post2 :
                    post_address.append(p.getText())
                for r in range(row):
                    self.w.table.setItem(r, 0, QTableWidgetItem(str(post_num[r])))
                    self.w.table.setItem(r, 1, QTableWidgetItem(str(post_address[r])))   
                    
    # 231206 목록에서 찾은 우편번호 및 주소 라인에디트에 세팅 by 정현아
    def selectPost(self, row, col):
        self.post_num = self.w.table.item(row, 0).text() 
        self.post_address = self.w.table.item(row, 1).text()
        self.w.address_lineEdit.setText(self.post_num + " " + self.post_address)

    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Edit() 
    myWindow.show() 
    app.exec_() 