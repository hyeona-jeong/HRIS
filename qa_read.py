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
        self.co_idx_list = []
        self.idx = idx
        
        self.conn = pymysql.connect(
                host='192.168.2.20',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        self.cur = self.conn.cursor()
        self.downlaod_btn_list = []
        
        query = "SELECT AUTHORITY, NAME_KOR FROM LOGIN_DATA, MAIN_TABLE WHERE LOGIN_DATA.EMP_NUM = MAIN_TABLE.EMP_NUM AND LOGIN_DATA.EMP_NUM = %s"
        self.cur.execute(query, emp_num)
        result = self.cur.fetchone()
        self.auth = result[0]
        self.username = result[1]
        
        self.load_post()
        self.load_comment()
        self.co_subitBtn.clicked.connect(lambda: self.submit_comment(emp_num))
        self.editBtn.clicked.connect(self.edit_post)
        self.delBtn.clicked.connect(self.delete_post)
        self.cnlBtn.clicked.connect(self.close)
                
    # 231222 DB 데이터 불러오기오고 라벨에 데이터 세팅 by 정현아
    def load_post(self):
        # 이전에 저장된 값을 불러오지 않게 QWebEngineView 제거
        if hasattr(self, 'contents_webview'):
            self.verticalLayout_2.removeWidget(self.contents_webview)
            self.contents_webview.deleteLater()  # 메모리에서 해제

        # 새로운 QWebEngineView 생성 및 레이아웃에 추가
        self.contents_webview = QWebEngineView()
        self.verticalLayout_2.addWidget(self.contents_webview)
        
        query = "SELECT WRITER, TITLE, CONTENTS, EDIT_DATE, ATCH_IMG_PATH, ATCH_FILE_PATH, ATCH_FILE_NAME, SUBMIT_DATE FROM Q_A WHERE IDX = '%s'"
        self.cur.execute(query,(self.idx))
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
    
    # 231229 등록된 리플을 불러오는 메서드 by 정현아
    def load_comment(self):
        query = "SELECT IDX, WRITER, CONTENTS FROM QA_COMMENT WHERE FO_IDX = %s"
        self.cur.execute(query, self.idx)
        result = self.cur.fetchall()
        for row,row_data in enumerate(result):
            # 댓글 생성위치설정
            co_num = self.verticalLayout_9.count()-1
            # 댓글란을 가로로 배치하기 위해 레이아웃 생성
            self.coBox = QHBoxLayout()
            self.verticalLayout_9.insertLayout(co_num,self.coBox)
            
            for col, data in enumerate(row_data):    
                # 댓글 인덱스 값 저장    
                if col == 0:
                    self.co_idx_list.append(data)
                
                # 이름 레이블 생성 및 배치
                elif col == 1:
                    name_lbl = QLabel(data)
                    name_lbl.setFixedWidth(50)
                    name_lbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    self.coBox.insertWidget(0,name_lbl)
                    
                # 댓글 레이블 생성 및 배치
                elif col == 2:
                    con_lbl = QLabel(data)
                    con_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self.coBox.insertWidget(1,con_lbl)
                
            co_edit_btn = QPushButton("수정")
            co_edit_btn.setFixedSize(34,28)
            co_edit_btn.clicked.connect(lambda state, idx=self.co_idx_list[-1]: self.edit_comment(idx))
            self.coBox.insertWidget(2,co_edit_btn)
            
            co_del_btn = QPushButton("삭제")
            co_del_btn.setFixedSize(34,28)
            co_del_btn.clicked.connect(lambda state, idx=self.co_idx_list[-1]: self.delete_comment(idx))
            self.coBox.insertWidget(3,co_del_btn)
            
            if not (self.auth == "Master" or row_data[1] == self.username):
                co_edit_btn.setVisible(False)
                co_del_btn.setVisible(False)
                
    # 231229 댓글 수정 메서드 by 정현아
    def edit_comment(self, idx):
        query = "SELECT CONTENTS FROM QA_COMMENT WHERE IDX = %s"
        self.cur.execute(query, idx)
        contents = self.cur.fetchone()
        
        index = self.co_idx_list.index(idx)
        co_cnt = len(self.co_idx_list)
        co_num = self.verticalLayout_9.count() - co_cnt + index - 1
        comment_layout = self.verticalLayout_9.itemAt(co_num)
        # 레이아웃에 있는 댓글 레이블 메모리에서 해제 
        for i in range(1,4):
            item = comment_layout.takeAt(1)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()   
        co_te = QTextEdit()
        co_te.setHtml(contents[0])
        comment_layout.addWidget(co_te)
        submit_Btn = QPushButton("등록")
        submit_Btn.setFixedSize(75,70)
        comment_layout.addWidget(submit_Btn)
        submit_Btn.clicked.connect(lambda : self.save_edit_comment(object=co_te,idx=idx))
            
    # 231229 댓글 수정 후 DB에 저장 및 입력창 > 레이블, 저장 버튼 > 삭제, 수정버튼 변경 by 정현아
    def save_edit_comment(self, object, idx):
        contents = object.toHtml()
        
        index = self.co_idx_list.index(idx)
        co_cnt = len(self.co_idx_list)
        co_num = self.verticalLayout_9.count() - co_cnt + index - 1
        del_comment = self.verticalLayout_9.itemAt(co_num)
        
        query = "UPDATE QA_COMMENT SET CONTENTS = %s WHERE IDX = %s"
        self.cur.execute(query, (contents, idx))
        self.conn.commit()
        
        # 레이아웃에 있는 모든 위젯들을 메모리에서 해제
        while del_comment.count():
            item = del_comment.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()   
        # 본문에 있는 HBOX레이아웃을 VBOX레이아웃에서 제거
        self.verticalLayout_9.removeItem(del_comment)
        
        query = "SELECT IDX, WRITER, CONTENTS, SUBMIT_DATE, EDIT_DATE FROM QA_COMMENT WHERE IDX = %s"
        self.cur.execute(query, idx)
        result = self.cur.fetchone()
        self.insert_comment(result)
                  
    # 231229 댓글 삭제 메서드 by 정현아
    def delete_comment(self, idx):
        index = self.co_idx_list.index(idx)
        co_cnt = len(self.co_idx_list)
        co_num = self.verticalLayout_9.count() - co_cnt + index - 1
        query = "DELETE FROM QA_COMMENT WHERE IDX = %s"
        self.cur.execute(query,idx)
        self.conn.commit()
        del_comment = self.verticalLayout_9.itemAt(co_num)
        # 레이아웃에 있는 모든 위젯들을 메모리에서 해제
        while del_comment.count():
            item = del_comment.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()   
        # 본문에 있는 HBOX레이아웃을 VBOX레이아웃에서 제거
        self.verticalLayout_9.removeItem(del_comment)
    
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
    
    def delete_post(self):
        reply = QMessageBox.question(self, '삭제 확인', '삭제된 정보는 복구할 수 없습니다.\n삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:        
                query = "DELETE FROM Q_A WHERE IDX = %s"
                self.cur.execute(query, self.idx)
                self.conn.commit()
                self.conn.close()
                self.close()
            except Exception as e:
                QMessageBox.warning(self, "게시글 삭제 실패", "Error: " + str(e))
                return       
            
    # 231229 댓글 등록 메서드 by 정현아
    def submit_comment(self, emp_num):
        # 입력내용이 없을 시 입력 불가
        content = self.co_te.toPlainText()
        if content == "" :
            QMessageBox.warning(self,"댓글 등록 실패","댓글을 입력해주세요.")
            return
        contents = self.co_te.toHtml()
        fo_idx = self.idx
        query = "SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = %s"
        self.cur.execute(query, emp_num)
        co_writer = self.cur.fetchone()[0]
        
        query = "INSERT INTO QA_COMMENT (FO_IDX, WRITER, CONTENTS) VALUES (%s, %s, %s)"
        self.cur.execute(query,(fo_idx,co_writer,contents))
        self.conn.commit()
        
        # 막 입력된 정보를 가져와야 하므로 제일 마지막으로 저장된 정보 하나만 가져옴
        query = "SELECT IDX, WRITER, CONTENTS, SUBMIT_DATE, EDIT_DATE FROM QA_COMMENT WHERE FO_IDX = %s ORDER BY IDX DESC LIMIT 1"
        self.cur.execute(query, self.idx)
        result = self.cur.fetchone()
        # 댓글 idx 리스트에 추가
        self.co_idx_list.append(result[0])
        self.insert_comment(result)
    
    # 231229 입력 댓글 생성 by 정현아
    def insert_comment(self, data):
        # 댓글 생성위치설정
        co_num = self.verticalLayout_9.count()-1
        # 댓글란을 가로로 배치하기 위해 레이아웃 생성
        self.coBox = QHBoxLayout()
        self.verticalLayout_9.insertLayout(co_num,self.coBox)
        
        # 이름 레이블 생성 및 배치
        name_lbl = QLabel(data[1])
        name_lbl.setFixedWidth(50)
        name_lbl.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.coBox.insertWidget(0,name_lbl)
       
        # 댓글 레이블 생성 및 배치
        con_lbl = QLabel(data[2])
        con_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.coBox.insertWidget(1,con_lbl)
        
        co_edit_btn = QPushButton("수정")
        co_edit_btn.setFixedSize(34,28)
        self.coBox.insertWidget(2,co_edit_btn)
        
        co_del_btn = QPushButton("삭제")
        co_del_btn.setFixedSize(34,28)
        self.coBox.insertWidget(3,co_del_btn)
        # 댓글 입력란 초기화 
        self.co_te.setPlainText("")
        
        co_edit_btn.clicked.connect(lambda state, idx=self.co_idx_list[-1]: self.edit_comment(idx))
        co_del_btn.clicked.connect(lambda state, idx=self.co_idx_list[-1]: self.delete_comment(idx))
        
        if not (self.auth == "Maser" or data[1] == self.username):
            co_edit_btn.setVisible(False)
            co_del_btn.setVisible(False)
        
        
    def edit_post(self):
        self.w = Edit(self.conn, self.cur, self.idx)
        self.w.show()
        self.hide()
        self.w.closed.connect(lambda: (self.show(), self.load_post()))

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