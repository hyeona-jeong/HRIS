import os
import sys
import pymysql
import re

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('read.ui')
form_class = uic.loadUiType(form)[0]

class Read(QMainWindow, form_class):

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.result = None
        
        self.load_post()
        # 231222 각 라벨에 데이터 값 세팅 by 정현아
        if self.result:
            post_wirter = self.result[0] 
            title = self.result[1]
            edit_date = self.result[3].strftime("%Y-%m-%d %H:%M")
            atch_imgs = self.result[4]
            
            # 내용에 QWebEngineView 추가
            self.contents_webview = QWebEngineView()
            self.verticalLayout.addWidget(self.contents_webview)
            
            self.title_lbl.setText(title)
            self.last_timestamp.setText(edit_date)
            self.writer_lbl.setText(post_wirter)
            contents = self.result[2]
            if atch_imgs:
                contents = self.load_img()
            self.contents_webview.setHtml(contents)
        
    # DB 데이터 불러오기 by 정현아
    def load_post(self, idx = 6):
        self.conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        self.cur = self.conn.cursor()
        query = "SELECT WRITER, TITLE, CONTENTS, EDIT_DATE, ATCH_IMG_PATH, ATCH_FILE_PATH, ATCH_FILE_NAME FROM FORUM WHERE IDX = '%s'"
        self.cur.execute(query,(idx))
        self.result = self.cur.fetchone()
    
    # 231222 이미지 태그 경로를 로컬에서 구글드라이브 경로로 변경 by 정현아
    def load_img(self):
        contents = self.result[2]
        # <img로 시작하고 src 속성이 "https://drive.google.com/uc?id="로 시작하지 않는 경우 이미지 태그 웹이미지 태그로 변경 by 정현아
        local_img_tag = re.compile(r'<img\s[^>]*src=["\'](?!https://drive\.google\.com/uc\?id=)[^"\']*["\'][^>]*>')
        web_img_tags = self.result[4].split(',')
        all_contents = contents

        for new_tag in web_img_tags:
            if new_tag == '':
                break

            new_tag = f'<img src="{new_tag}"/>'
            all_contents = re.sub(local_img_tag, new_tag, all_contents, count=1)
        return all_contents
        
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Read() 
    myWindow.show() 
    app.exec_() 