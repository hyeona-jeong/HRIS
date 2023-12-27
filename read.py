import os
import sys
import pymysql
import re

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from edit import Edit

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('read.ui')
form_class = uic.loadUiType(form)[0]

class Read(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self, idx):
        super( ).__init__( )
        self.setupUi(self)
        self.result = None
        
        self.conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        self.cur = self.conn.cursor()
        self.downlaod_btn_list = []
        
        self.load_post(idx)
            
        self.editBtn.clicked.connect(lambda: self.edit_post(self.conn, self.cur, idx))
        self.delBtn.clicked.connect(lambda: self.delete_post(idx))
        self.cnlBtn.clicked.connect(self.close)
        
    # 231222 DB 데이터 불러오기오고 라벨에 데이터 세팅 by 정현아
    def load_post(self, idx):
        # 이전에 저장된 값을 불러오지 않게 QWebEngineView 제거
        if hasattr(self, 'contents_webview'):
            self.verticalLayout.removeWidget(self.contents_webview)
            self.contents_webview.deleteLater()  # 메모리에서 해제

        # 새로운 QWebEngineView 생성 및 레이아웃에 추가
        self.contents_webview = QWebEngineView()
        self.verticalLayout.addWidget(self.contents_webview)
        
        query = "SELECT WRITER, TITLE, CONTENTS, EDIT_DATE, ATCH_IMG_PATH, ATCH_FILE_PATH, ATCH_FILE_NAME, SUBMIT_DATE FROM FORUM WHERE IDX = '%s'"
        self.cur.execute(query,(idx))
        self.result = self.cur.fetchone()
        
        # 231222 각 라벨에 데이터 값 세팅 by 정현아
        if self.result:
            post_wirter = self.result[0] 
            title = self.result[1]
            submit_date = self.result[7].strftime("%Y-%m-%d %H:%M")
            edit_date = self.result[3].strftime("%Y-%m-%d %H:%M")
            atch_imgs = self.result[4]
            set_timestamp = submit_date + r" (최종 수정시간 : " + edit_date + r")"
            
            self.title_lbl.setText(title)
            self.last_timestamp.setText(set_timestamp)
            self.writer_lbl.setText(post_wirter)
            contents = self.result[2]
            if atch_imgs:
                contents = self.load_img()
            self.contents_webview.setHtml(contents)
            
            # 231227 첨부파일 이름대로 푸쉬버튼 생성
            self.file_name_list = self.result[6].split(",")
            del self.file_name_list[-1]
            i = 0
            for atch_file_name in self.file_name_list:
                self.downlaod_btn_list.append(QPushButton(atch_file_name))
                self.downlaod_btn_list[i].setStyleSheet("border: none;")
                self.fileLay.insertWidget(i+1,self.downlaod_btn_list[i])
                self.downlaod_btn_list[i].installEventFilter(self)
                self.downlaod_btn_list[i].clicked[str].connect(self.download_file)
                i+=1
                
    def download_file(self,file_name):
        index = self.file_name_list.index(file_name)
        pass
    
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
    
    def delete_post(self, idx):
        reply = QMessageBox.question(self, '삭제 확인', '삭제된 정보는 복구할 수 없습니다.\n삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:        
                query = "DELETE FROM FORUM WHERE IDX = %s"
                self.cur.execute(query, idx)
                self.conn.commit()
                self.conn.close()
                self.close()
            except Exception as e:
                QMessageBox.warning(self, "게시글 삭제 실패", "Error: " + str(e))
                return       
            
    def edit_post(self, conn, cur, idx):
        self.w = Edit(conn, cur, idx)
        self.w.show()
        self.hide()
        self.w.closed.connect(lambda: (self.show(), self.load_post(idx)))

    # 231127 첨부파일 위에 위치시 커서 이미지 변경 by정현아 
    def eventFilter(self, object, event):
        if event.type() == QEvent.HoverEnter:
            QApplication.setOverrideCursor(Qt.PointingHandCursor)
            return True
        elif event.type() == QEvent.HoverLeave:
            QApplication.restoreOverrideCursor()
        return False
    
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)
        
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Read() 
    myWindow.show() 
    app.exec_() 