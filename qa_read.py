import os
import sys
import pymysql
import re
import gdown

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from qa_edit import Edit

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('qa_read.ui')
form_class = uic.loadUiType(form)[0]

class Read(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self, idx, emp_num):
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
        
        self.co_subitBtn.clicked.connect(lambda: self.submit_comment(self.conn, self.cur, idx, emp_num))
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
        self.verticalLayout_2.addWidget(self.contents_webview)
        
        query = "SELECT WRITER, TITLE, CONTENTS, EDIT_DATE, ATCH_IMG_PATH, ATCH_FILE_PATH, ATCH_FILE_NAME, SUBMIT_DATE FROM Q_A WHERE IDX = '%s'"
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
            if self.result[6]:
                self.file_name_list = self.result[6].split(",")
                del self.file_name_list[-1]
                i = 0
                for atch_file_name in self.file_name_list:
                    self.downlaod_btn_list.append(QPushButton(atch_file_name))
                    self.downlaod_btn_list[i].setStyleSheet("border: none;")
                    self.fileLay.insertWidget(i+1,self.downlaod_btn_list[i])
                    self.downlaod_btn_list[i].installEventFilter(self)
                    self.downlaod_btn_list[i].clicked.connect(lambda _, file_name=atch_file_name: self.download_file(file_name))
                    i+=1
    
    # 231228 파일 다운로드 by 정현아            
    def download_file(self,file_name):
        index = self.file_name_list.index(file_name)
        web_path = self.result[5].split(",")
        reply = QMessageBox.question(self, '저장 확인', '현재 폴더에 저장하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            gdown.download(web_path[index],self.file_name_list[index],quiet=False)
            QMessageBox.information(self,"저장 완료", "저장되었습니다.")
    
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
                query = "DELETE FROM Q_A WHERE IDX = %s"
                self.cur.execute(query, idx)
                self.conn.commit()
                self.conn.close()
                self.close()
            except Exception as e:
                QMessageBox.warning(self, "게시글 삭제 실패", "Error: " + str(e))
                return       
            
    # 231229 댓글 등록 메서드 by 정현아
    def submit_comment(self, conn, cur, idx, emp_num):
        content = self.co_te.toPlainText()
        if content == "" :
            QMessageBox.warning(self,"댓글 등록 실패","댓글을 입력해주세요.")
            return
        contents = self.co_te.toHtml()
        fo_idx = idx
        query = "SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = %s"
        cur.execute(query, emp_num)
        co_writer = cur.fetchone()[0]
        
        query = "INSERT INTO QA_COMMENT (FO_IDX, WRITER, CONTENTS) VALUES (%s, %s, %s)"
        cur.execute(query,(fo_idx,co_writer,contents))
        conn.commit()
        query = "SELECT IDX, WRITER, CONTENTS, SUBMIT_DATE, EDIT_DATE FROM QA_COMMENT WHERE FO_IDX = %s ORDER BY IDX DESC LIMIT 1"
        cur.execute(query, idx)
        result = cur.fetchone()
        self.insert_comment(result)
    
    def insert_comment(self, data):
        co_num = self.verticalLayout_9.count()-1
        coBox = QHBoxLayout()
        self.verticalLayout_9.insertLayout(co_num,coBox)
        name_lbl = QLabel(data[1])
        name_lbl.setMinimumWidth(50)
        coBox.insertWidget(0,name_lbl)
        con_lbl = QLabel(data[2])
        coBox.insertWidget(1,con_lbl)
        con_lbl.setAlignment(Qt.AlignLeft) 
        con_lbl.setWordWrap(True)
        edit_btn = QPushButton("수정")
        edit_btn.setFixedSize(34,28)
        coBox.insertWidget(2,edit_btn)
        co_del_btn = QPushButton("삭제")
        co_del_btn.setFixedSize(34,28)
        coBox.insertWidget(3,co_del_btn)
        self.co_te.setPlainText("")
        
        
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