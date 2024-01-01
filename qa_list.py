import os
import sys
import pymysql
import math
import time

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qa_write import Write
from qa_read import Read

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('forum_list.ui')
form_class = uic.loadUiType(form)[0]

class Q_A(QMainWindow, form_class):
    closed = pyqtSignal()
    qaToWrite = pyqtSignal()
    qaToRead = pyqtSignal()

    def __init__(self, emp_num, auth):
        super( ).__init__( )
        self.setupUi(self)
        self.setStyleSheet(stylesheet)
        self.label_2.setText(r" Q&A")
        self.label_2.setStyleSheet("background-color: #ff5500; color: white;  font-size:18pt; font-weight:600;")

        # 231202 체크박스 체크된 ROW저장 리스트, 사업부검색 콤보박스, 이름검색 라인에딧초기화 by 정현아
        self.delRowList = list()
        self.search_field = ''
        self.search_word = ''
        self.w = None
        self.user = emp_num
        self.auth = auth
        self.emp_num = []
        self.result = None
        self.gBtn = []
        self.current_page = 0
        self.prev_page = 0
        self.align_index = [0,1,0,0,0,0,0,0]
        self.current_index = 1
        self.prev_index = None
        self.ignore_paging_btn = False

        self.table.setRowCount(0)
        self.header = ['','번호','카테고리','제목','작성자','작성일','조회수']
        self.table.setColumnCount(len(self.header))
        self.table.setHorizontalHeaderLabels(self.header)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.conn = pymysql.connect(
            host='localhost',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
        )

        self.cur = self.conn.cursor()
        # 231224 테이블 세팅 by 정현아
        self.main_query = "SELECT IDX, CATEGORY, TITLE, WRITER, SUBMIT_DATE, VIEW_CNT, EMP_NUM FROM Q_A "
        if self.auth == "Regular":
            self.main_query += f"WHERE WRITER = (SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = {self.user}) "
        self.setTables(self.main_query)
        self.gBtn[0].setChecked(True)
        self.gBtn[0].setStyleSheet(
                    "QToolButton { border: None; color : black; font-weight: bold; }"
                )

        # 231202 사원전체 수 라벨에 세팅 by 정현아
        countQuery = "SELECT COUNT(*) FROM Q_A "
        if self.auth == "Regular":
            countQuery += f"WHERE WRITER = (SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = {self.user}) "
        self.cur.execute(countQuery)
        count = self.cur.fetchone()[0]
        self.countLabel.setText("총 ("+ str(count) + ")건")
        
        # 제목은 stretch로 설정 그 외 컬럼은 컨텐츠 사이즈에 맞게 설정 by 정현아
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)   
   
        # 콤보박스 및 버튼 클릭 이벤트 by 정현아
        self.search_cb.activated[str].connect(self.setCombo)
        self.search_le.returnPressed.connect(self.searchPost)
        self.empSearchBtn.clicked.connect(self.searchPost)

        self.table.itemChanged.connect(self.delChk)
        self.listDelBtn.clicked.connect(self.delChkList)
        self.listRegBtn.clicked.connect(lambda: self.writePost(emp_num))
        self.table.cellDoubleClicked.connect(self.readPost)
        self.table.horizontalHeader().sectionClicked.connect(self.chgHeader)

    # 페이지 버튼 생성 함수 by 정현아
    def setPagingBtn(self, row, query):
        j = 1
        # 기존 버튼 비우기
        self.gBtn.clear()  
        while self.gbox.count():
            item = self.gbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()        
        self.btnGroup = QButtonGroup(self)
        # 페이지 수 세팅
        page = math.ceil(row/15)
        if page == 0 :
            page = 1
        # 페이지 수가 5이하일 경우 페이지 수만큼 버튼생성, 5이상일 경우 5개 생성
        if page <=5:
            for i in range(page):
                self.gBtn.append(QToolButton())
        else:
            for i in range(5):
                self.gBtn.append(QToolButton())
        for btn in self.gBtn:
            btn.setCheckable(True)
            btn.setText(str(j))
            self.btnGroup.addButton(btn)
            self.gbox.addWidget(btn,0,j)
            j+=1
        prev_btn = QToolButton(self)
        prev_btn.setText("<<")
        end_btn = QToolButton(self)
        end_btn.setText(">>")
        # 231209 제일 앞으로 버튼과 제일 뒤로 버튼 생성
        self.btnGroup.addButton(prev_btn)
        self.btnGroup.addButton(end_btn)
        self.gbox.addWidget(prev_btn,0,0)
        self.gbox.addWidget(end_btn,0,j+2)
        self.btnGroup.setExclusive(True)
        # 231208 버튼의 인덱스 값과 query 값을 전달하여 페이지 세팅 by 정현아
        self.btnGroup.buttonClicked[int].connect(lambda button_id: self.setCheckedBtn(button_id, query, page))
            
    # 231207 버튼 클릭시 이벤트 by 정현아
    def setCheckedBtn(self, button_id, query, page):
        j = 1
        btn = self.btnGroup.button(button_id)
        btn.setChecked(True)

        for button in self.btnGroup.buttons():
            if button is btn and btn.isChecked():
                button.setStyleSheet(
                    "QToolButton { border: None; color : black; font-weight: bold; }"
                )
            else:
                button.setStyleSheet(
                    "QToolButton { border: None; color: #5a5a5a; }"
                )
        # 이전 페이지 저장
        if self.prev_page != self.current_page:
            self.prev_page = self.current_page 

        # 현재 페이지 세팅
        if btn.text().isdigit():
            self.current_page = int(btn.text())
              
        # 231210 페이지 수가 5보다 클 때 by 정현아
        if len(self.gBtn) >= 5:
            # 231209 1>2>3 오름차순으로 페이지 이동 by 정현아
            if self.current_page > self.prev_page:
                # 그리드 레이아웃에서 제일 앞에 있는 버튼 제거 후 다시 제일 뒤에 배치
                if not(btn.text() == '1' or btn.text() == '2' or btn.text() == '3' or btn.text() == str(page-1) or btn.text() == str(page) or btn.text() == "<<" or btn.text() == ">>"):
                    self.btnGroup.removeButton(self.gBtn[0])
                    item = self.gBtn.pop(0)
                    item.setText(str(int(btn.text())+2))
                    self.gBtn.append(item)
                    self.btnGroup.addButton(self.gBtn[4])
                    for button in self.gBtn:
                        self.gbox.addWidget(button,0,j)
                        j+=1
                elif btn.text() == str(page-1) and self.current_page - self.prev_page > 1 :
                    self.btnGroup.removeButton(self.gBtn[0])
                    item = self.gBtn.pop(0)
                    item.setText(str(int(btn.text())+1))
                    self.gBtn.append(item)
                    self.btnGroup.addButton(self.gBtn[4])
                    for button in self.gBtn:
                        self.gbox.addWidget(button,0,j)
                        j+=1
            # 231209 3>2>1 내림차순으로 페이지 이동 by 정현아
            else:
                # 그리드 레이아웃에서 제일 뒤에 있는 버튼 제거 후 다시 제일 앞에 배치
                if not(btn.text() == '1' or btn.text() == '2' or btn.text() == str(page-2) or btn.text() == str(page-1) or btn.text() == str(page) or btn.text() == "<<" or btn.text() == ">>"):
                    self.btnGroup.removeButton(self.gBtn[4])
                    item = self.gBtn.pop(4)
                    item.setText(str(int(btn.text())-2))
                    self.gBtn.insert(0,item)
                    self.btnGroup.addButton(self.gBtn[0])
                    for button in self.gBtn:
                        self.gbox.addWidget(button,0,j)
                        j+=1
                elif btn.text() == '2' and self.prev_page - self.current_page > 1 :
                    self.btnGroup.removeButton(self.gBtn[4])
                    item = self.gBtn.pop(4)
                    item.setText(str(int(btn.text())-1))
                    self.gBtn.insert(0,item)
                    self.btnGroup.addButton(self.gBtn[0])
                    for button in self.gBtn:
                        self.gbox.addWidget(button,0,j)
                        j+=1
                # 제일 앞으로 버튼 클릭시 1번 버튼 bold처리 및 버튼 숫자 1~5 세팅
                elif btn.text() =='<<':
                    self.current_page = 1
                    for i in range(5):
                        self.gBtn[i].setText(str(i + 1))
                    self.gBtn[0].setStyleSheet(
                            "QToolButton { border: None; color : black; font-weight: bold; }"
                        )
                elif btn.text() =='>>':
                    self.current_page = page
                    for i in range(5):
                        self.gBtn[i].setText(str(page -4 + i))
                    self.gBtn[4].setStyleSheet(
                            "QToolButton { border: None; color : black; font-weight: bold; }"
                        )   
        # 231210 페이지 수가 5보다 작을때 때 by 정현아
        else:
            if btn.text() =='<<':
                    self.current_page = 1
                    self.gBtn[0].setStyleSheet(
                            "QToolButton { border: None; color : black; font-weight: bold; }"
                        )
            elif btn.text() =='>>':
                self.current_page = page
                self.gBtn[page-1].setStyleSheet(
                        "QToolButton { border: None; color : black; font-weight: bold; }"
                    )   
                   
        self.ignore_paging_btn = True
        self.setTables(query)
        
    # 로딩시 커서 변경
    def setLoadingCursor(self, loading):
        if loading:
            QApplication.setOverrideCursor(Qt.WaitCursor)
        else:
            QApplication.restoreOverrideCursor()

    # 231202 테이블 세팅 함수 쿼리값 변경시 테이블위젯에 세팅된 테이블 값도 변경 by 정현아
    def setTables(self, query):
        self.emp_num = []
        # 로딩 중에 WaitCursor로 변경
        self.setLoadingCursor(True)
        # 테이블 정렬 상태 확인 후 쿼리를 정렬하는 쿼리로 변경함
        current_sorting_column = self.current_index
        current_sorting_order = self.align_index[self.current_index] % 2
        order_direction = "ASC" if current_sorting_order == 0 else "DESC"
        sort_query = f"{query} ORDER BY {current_sorting_column} {order_direction}"
        self.table.blockSignals(True)
        # 테이블 내의 아이템을 모두 삭제
        self.table.clearContents()
        # 페이지 내의 컬럼수 세팅
        page_row = 15
        self.table.setRowCount(page_row)
        self.cur.execute(sort_query)
        result = self.cur.fetchall()
        # 231209 버튼 페이지 세팅, setCheckedBtn에서 호출시 페이징 버튼 생성 함수는 호출하지 않음 by 정현아
        if not self.ignore_paging_btn:
            self.setPagingBtn(len(result), query)
            # 테이블 아이템 다시 세팅시 페이지 수 1로 설정
            self.current_page = 1
            self.gBtn[0].setChecked(True)
            self.gBtn[0].setStyleSheet(
                        "QToolButton { border: None; color : black; font-weight: bold; }"
                    )
        self.ignore_paging_btn = False
        # 231229 QA답변여부 체크
        check_query = "SELECT * FROM QA_COMMENT WHERE FO_IDX = %s"
        
        # 테이블 내에 아이템 세팅 페이지당 row수 15개로 제한
        for row, row_data in enumerate(result):
            if row < 15 * (self.current_page-1) :
                continue
            if row == 15 * self.current_page :
                break
            # 첫 열 체크박스 세팅 체크박스 정렬을 위해 위젯 생성 후 정렬
            chk_widget = QWidget()
            chk_layout = QHBoxLayout(chk_widget)
            chk_layout.setAlignment(Qt.AlignCenter)

            chk_bx = QCheckBox()
            chk_layout.addWidget(chk_bx)
            chk_layout.setContentsMargins(0, 0, 0, 0)
            chk_widget.setLayout(chk_layout)

            self.table.setCellWidget(row % 15, 0, chk_widget)
            chk_bx.stateChanged.connect(lambda state, row=row % 15: self.delChk(state, row))
            for col, data in enumerate(row_data):
                if col == 0:
                    self.cur.execute(check_query, data)
                    comment_yn = self.cur.fetchall
                if col == 6:
                    self.emp_num.append(data)
                elif col == 2:
                    title = "🔒" + str(data)
                    if comment_yn:
                        title += "☑️답변완료"
                    item = QTableWidgetItem(title)
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    self.table.setItem(row % 15, col + 1, item)
                else:
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    self.table.setItem(row % 15, col + 1, item)
        self.table.blockSignals(False)
        # 로딩이 끝나면 기본 커서로 변경
        self.setLoadingCursor(False) 

    # 231209 정렬할 때마다 헤더 옆에 화살표 특수문자를 붙여서 보여주고 정렬 방향 선택 by 정현아
    def chgHeader(self,index):
        if index == 0:
            return
        if self.prev_index != self.current_index:
           self.prev_index = self.current_index
        self.current_index = index
        if self.current_index == self.prev_index:
            self.align_index[index]+=1        
        if index != 0 and self.align_index[index] %2 == 0:
            self.table.setHorizontalHeaderItem(index, QTableWidgetItem(self.header[index]+'▲'))
            self.searchPost()
        elif index != 0 and self.align_index[index] %2 != 0:
            self.table.setHorizontalHeaderItem(index, QTableWidgetItem(self.header[index]+'▼'))
            self.searchPost()
        for i in range(len(self.header)):
            if i == index:
                continue
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.header[i]))
            
    # 231202 체크된 로우 확인 및 저장 by 정현아
    def delChk(self, state, row):
        if state == Qt.Checked:
            self.delRowList.append(row)
        elif state == Qt.Unchecked:
            self.delRowList.remove(row)

    # 231224 게시글 삭제
    def delChkList(self):
        self.table.blockSignals(True)
        delData = []
        if not self.delRowList :
            QMessageBox.warning(self, "게시글삭제실패", "선택된 게시글이 없습니다.")
            return
        else:
            # 231202 리스트에 선택된 로우의 IDX 정보를 리스트에 저장
            for i in self.delRowList :
                idx = int(self.table.item(i,1).text())
                delData.append(idx)

        query = 'DELETE FROM Q_A WHERE IDX = %s ;'
        reply = QMessageBox.question(self, '삭제 확인', '삭제된 정보는 복구할 수 없습니다.\n삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.executemany(query,(tuple(delData)))
                self.conn.commit()
                QMessageBox.information(self,"게시글 삭제 성공","삭제 되었습니다.") 
                self.setTables(self.main_query)
                self.delRowList = list()
                for idx in delData:
                    if idx not in self.emp_num:
                        break
                    self.emp_num.remove(idx)
            except Exception as e:
                QMessageBox.warning(self, "게시글 삭제 실패", "Error: " + str(e))
                return       
        self.table.blockSignals(False)

    # 231224 선택한 콤보박스로 검색할 범위 세팅 by 정현아
    def setCombo(self, keyword):
        self.search_field = {'전체': '', '제목': 'title', '내용': 'contents', '작성자': 'writer', '카테고리': 'category'}.get(keyword)

    # 231224 검색어가 비어있는지 확인 후 비어 있지 않으면 선택된 검색 범위에 맞게 해당 검색어로 검색 by 정현아
    def searchPost(self):
        self.table.blockSignals(True)
        self.search_word = self.search_le.text()
        if self.search_word != '':
            if self.search_field == '':
                query = f"""SELECT 
                IDX, CATEGORY, TITLE, WRITER, SUBMIT_DATE, VIEW_CNT, EMP_NUM 
                FROM Q_A 
                WHERE (TITLE LIKE '%{self.search_word}%' OR CONTENTS LIKE '%{self.search_word}%' OR WRITER LIKE '%{self.search_word}%' OR CATEGORY LIKE '%{self.search_word}%')"""
                if self.auth == "Regular":
                    query += f" AND WRITER = (SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = {self.user}) "
                self.setTables(query)
                countQuery = f"SELECT COUNT(*) FROM Q_A WHERE (TITLE LIKE '%{self.search_word}%' OR CONTENTS LIKE '%{self.search_word}%' OR WRITER LIKE '%{self.search_word}%' OR CATEGORY LIKE '%{self.search_word}%')"
                if self.auth == "Regular":
                    countQuery += f" AND WRITER = (SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = {self.user}) "
                self.cur.execute(countQuery)
                count = self.cur.fetchone()[0]
                self.countLabel.setText("총 ("+ str(count) + ")건")
            else :
                query = f"""SELECT 
                IDX, CATEGORY, TITLE, WRITER, SUBMIT_DATE, VIEW_CNT, EMP_NUM 
                FROM Q_A 
                WHERE {self.search_field} LIKE '%{self.search_word}%'"""
                if self.auth == "Regular":
                    query += f" AND WRITER = (SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = {self.user}) "
                self.setTables(query)
                countQuery = f"SELECT COUNT(*) FROM Q_A WHERE {self.search_field} LIKE '%{self.search_word}%'"
                if self.auth == "Regular":
                    countQuery += f" AND WRITER = (SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = {self.user}) "
                self.cur.execute(countQuery)
                count = self.cur.fetchone()[0]
                self.countLabel.setText("총 ("+ str(count) + ")건")
        else:
            self.setTables(self.main_query)
            self.gBtn[0].setChecked(True)
            self.gBtn[0].setStyleSheet(
                        "QToolButton { border: None; color : black; font-weight: bold; }"
                    )
            countQuery = "SELECT COUNT(*) FROM Q_A "
            if self.auth == "Regular":
                countQuery += f"WHERE WRITER = (SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = {self.user}) "
            self.cur.execute(countQuery)
            count = self.cur.fetchone()[0]
            self.countLabel.setText("총 ("+ str(count) + ")건")
            self.table.blockSignals(False)
    
    # 글쓰기 화면 불러오기 by 정현아
    def writePost(self, emp_num):
        self.w = Write(emp_num,self.conn,self.cur)
        self.qaToWrite.emit()
        self.w.show()
        self.hide()
        self.w.closed.connect(lambda: (self.show(), self.show_list()))
        
    # 231224 게시글 읽기
    def readPost(self, row, col):
        idx = int(self.table.item(row,1).text())
        query = "SELECT VIEW_CNT FROM Q_A WHERE IDX = %s"
        self.cur.execute(query, idx)
        result = self.cur.fetchone()[0]
        if not result:
            QMessageBox.warning(self, "게시글 없음", "삭제된 게시글 입니다.")
            return
        result += 1
        query = "UPDATE Q_A SET VIEW_CNT =%s WHERE IDX = %s"
        self.cur.execute(query, (result, idx))
        self.conn.commit()
        
        self.w1 = Read(idx, self.user)
        if not (self.user == self.emp_num[row] or self.auth == "Master"):
            QMessageBox.warning(self,"권한 부적합","QA 내용은 작성자와 관리자만 확인가능합니다.")
            return
        
        self.qaToRead.emit()
        self.w1.show()
        self.hide()
        self.w1.closed.connect(lambda: (self.show(), self.show_list()))
        
    def show_list(self):
        query = "SELECT * FROM Q_A"
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.setTables(self.main_query)
        self.gBtn[0].setChecked(True)
        self.gBtn[0].setStyleSheet(
                    "QToolButton { border: None; color : black; font-weight: bold; }"
                )
        countQuery = "SELECT COUNT(*) FROM Q_A "
        if self.auth == "Regular":
            countQuery += f"WHERE WRITER = (SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = {self.user}) "
        self.cur.execute(countQuery)
        count = self.cur.fetchone()[0]
        self.countLabel.setText("총 ("+ str(count) + ")건")
        self.show()

    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)
            
stylesheet = """
    QTableWidget {
        border-radius: 10px;
        background-color: #eeeeee;
        margin-top:10px;   
        margin-bottom:10px;       
        padding-left:10px;          
        padding-right:10px;
    }
    QTableWidget::item {
        background-color: #ffffff;
        margin-top: 5px;    
        margin-bottom:5px;      
        color: #404040;
    }
    QTableWidget::item:selected {
        color: black;
    }
    QHeaderView::section{
        Background-color:#c6c6c6;
        border-radius:2px;
    }
    QToolButton{
        border: None;
        color: #868686; 
    }
"""
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Q_A() 
    myWindow.show() 
    app.exec_() 