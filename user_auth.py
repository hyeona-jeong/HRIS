import os
import sys
import openpyxl
import pymysql
import math

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from add_edu import DialogClass

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('user_auth.ui')
form_class = uic.loadUiType(form)[0]

class EduList(QMainWindow, form_class):
    closed = pyqtSignal()
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.eduList.setStyleSheet(stylesheet)
        
        # 변경된 셀값 저장
        self.biz = '전체'
        self.name = ''
        self.gBtn = []
        self.delRowList = []
        self.chgRowList = []
        self.chgAuthList = []
        self.current_page = 1
        self.prev_page = None
        self.ignore_paging_btn = False
        self.header = ['','사번','사업부','그룹','이름','ID','권한']
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.bizCombo.activated[str].connect(self.searchBiz)
        self.namelineEdit.returnPressed.connect(self.searchEmp)
        self.empSearchBtn.clicked.connect(self.searchEmp)
        
        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)    
        
        self.table.itemChanged.connect(self.delChk)
        self.delBtn.clicked.connect(self.delChkList)
        self.saveBtn.clicked.connect(self.saveAuth)

        self.conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        self.cur = self.conn.cursor()
        
        self.main_query = """
        SELECT LOGIN_DATA.EMP_NUM, DEPT_BIZ, DEPT_GROUP, NAME_KOR, ID, AUTHORITY 
        FROM MAIN_TABLE, LOGIN_DATA 
        WHERE LOGIN_DATA.EMP_NUM = MAIN_TABLE.EMP_NUM
        """
        # 231128 table 세팅 by 정현아
        self.table.setRowCount(0)
        self.setTables(self.main_query)
        self.gBtn[0].setChecked(True)
        self.gBtn[0].setStyleSheet(
                    "QToolButton { border: None; color : black; font-weight: bold; }"
                )
        self.table.sortByColumn(7,Qt.AscendingOrder)
        
    # 231128 페이징 버튼 생성 by 정현아
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
        # 페이지 수가 5미만일 경우 페이지 수만큼 버튼생성, 5이상일 경우 5개 생성
        if page <5:
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
        # 231209 버튼을 배타적으로 설정하여 한가지만 선택가능하도록 함 by 정현아
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
                if not(btn.text() == '1' or btn.text() == '2' or btn.text() == '3' or btn.text() == str(page-1) or btn.text() == str(page) or btn.text() == "<<" or btn.text() == ">>"):
                    # 그리드 레이아웃에서 제일 앞에 있는 버튼 제거 후 다시 제일 뒤에 배치
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
                # 231209 3>2>1 내림차순으로 페이지 이동 by 정현아
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

    # 231202 테이블 세팅 함수 쿼리값 변경시 테이블위젯에 세팅된 테이블 값도 변경 by 정현아
    def setTables(self, query):
        # 테이블 정렬 상태 확인 후 쿼리를 정렬하는 쿼리로 변경함
        current_sorting_column = self.table.horizontalHeader().sortIndicatorSection()
        current_sorting_order = self.table.horizontalHeader().sortIndicatorOrder()
        if current_sorting_column == 7:
            current_sorting_column = ''
        order_direction = "ASC" if current_sorting_order == 0 else "DESC"
        if current_sorting_column == '' :
            sort_query = query
        else:
            sort_query = f"{query} ORDER BY {current_sorting_column} {order_direction};"
        self.table.blockSignals(True)
        # 테이블 내의 아이템을 모두 삭제
        self.table.clearContents()
        page_row = 15
        self.table.setRowCount(page_row)
        self.cur.execute(sort_query)
        result = self.cur.fetchall()
        # 231209 버튼 페이지 세팅, setCheckedBtn에서 호출시 페이징 버튼 생성 함수는 호출하지 않음 by 정현아
        if not self.ignore_paging_btn:
            self.setPagingBtn(len(result), query)
            self.current_page = 1
            self.gBtn[0].setChecked(True)
            self.gBtn[0].setStyleSheet(
                        "QToolButton { border: None; color : black; font-weight: bold; }"
                    )
        self.ignore_paging_btn = False
        self.table.setSortingEnabled(False)
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
            # 테이블 아이템에 쿼리 결과값 세팅 by 정현아
            for col, data in enumerate(row_data):
                if col != 5:
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    self.table.setItem(row % 15, col + 1, item)
                else: 
                    combo_box = QComboBox(self)
                    combo_box.addItem("Master")
                    combo_box.addItem("Regular")
                    combo_box.setCurrentText(str(data))
                    self.table.setCellWidget(row % 15, col+1, combo_box)
                    combo_box.currentIndexChanged.connect(lambda index, row=row % 15: self.changeAuth(index, row))
                    print(row%15, data)
                    
        # 231128 table item 텍스트 중앙 정렬 및 6번 컬럼 제외한 컬럼 편집불가 처리
        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                if self.table.item(r,c) is not None:
                    self.table.item(r,c).setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                    if c == 1 or c == 2 or c == 3 or c == 4 or c == 5:
                        self.table.item(r,c).setFlags(self.table.item(r,c).flags() & ~ (Qt.ItemIsEditable))
        self.table.setSortingEnabled(True)
        self.table.blockSignals(False)
        self.table.horizontalHeader().setSortIndicatorShown(False)

    # 231129 사업부검색 함수 
    def searchBiz(self,biz):
        self.table.blockSignals(True)
        self.biz = biz 
        if self.name == '' :
            if self.biz == '전체':
                self.setTables(self.main_query)
            else:
                query = """
                SELECT LOGIN_DATA.EMP_NUM, DEPT_BIZ, DEPT_GROUP, NAME_KOR, ID, AUTHORITY 
                FROM MAIN_TABLE, LOGIN_DATA 
                WHERE LOGIN_DATA.EMP_NUM = MAIN_TABLE.EMP_NUM AND DEPT_BIZ = \'""" + biz +'\''
                self.setTables(query)
        else : 
            self.searchEmp()
        self.table.blockSignals(False)
        
    # 231129 사원검색 함수
    def searchEmp(self):
        self.table.blockSignals(True)
        self.name = self.namelineEdit.text()
        if self.name != '' : 
            if self.biz == '전체':
                query = f"""
                SELECT LOGIN_DATA.EMP_NUM, DEPT_BIZ, DEPT_GROUP, NAME_KOR, ID, AUTHORITY 
                FROM MAIN_TABLE, LOGIN_DATA 
                WHERE LOGIN_DATA.EMP_NUM = MAIN_TABLE.EMP_NUM AND NAME_KOR LIKE '%{self.name}%'
                """

            elif self.biz != '전체':
                query = f"""
                SELECT LOGIN_DATA.EMP_NUM, DEPT_BIZ, DEPT_GROUP, NAME_KOR, ID, AUTHORITY 
                FROM MAIN_TABLE, LOGIN_DATA 
                WHERE LOGIN_DATA.EMP_NUM = MAIN_TABLE.EMP_NUM AND DEPT_BIZ = '{self.biz}' AND NAME_KOR LIKE '%{self.name}%'
                """
            self.setTables(query)
        else:
            self.searchBiz(self.biz)
        self.table.blockSignals(False)
        
    # 0번 컬럼과 7번을 제외하고 정렬시 헤더에 표시
    def onHeaderClicked(self, index):
        if not (index == 0 or index == 6) :
            current_sorting_order = self.table.horizontalHeader().sortIndicatorOrder()
            if index != 0 and current_sorting_order==0:
                self.table.setHorizontalHeaderItem(index, QTableWidgetItem(self.header[index]+'▲'))
            elif index != 0 and current_sorting_order==1:
                self.table.setHorizontalHeaderItem(index, QTableWidgetItem(self.header[index]+'▼'))
            for i in range(len(self.header)):
                if i != index :
                    self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.header[i]))

    def delChk(self, state, row):
        print(row)
        if state == Qt.Checked:
            self.delRowList.append(row)
        elif state == Qt.Unchecked:
            self.delRowList.remove(row)

    # 231214 정보 삭제
    def delChkList(self):
        self.table.blockSignals(True)
        delData = []
        if not self.delRowList :
            QMessageBox.warning(self, "사원삭제실패", "선택된 사원이 없습니다.")
            return
        else:
            # 231214 리스트에 선택된 로우의 사번, ID 정보를 리스트에 저장
            for i in self.delRowList :
                colData = []
                colData.append(int(self.table.item(i,1).text()))
                colData.append(self.table.item(i,5).text())
                delData.append(colData)

        query = 'DELETE FROM LOGIN_DATA WHERE EMP_NUM = %s AND ID = %s;'
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.executemany(query,(tuple(delData)))
                self.conn.commit()
                QMessageBox.information(self,"사원ID삭제성공","삭제되었습니다.") 
                self.setTables(self.main_query)
                self.delRowList = list()
            except Exception as e:
                QMessageBox.warning(self, "사원ID삭제실패", "Error: " + str(e))
                return       
        self.table.blockSignals(False)

    # 권한이 변경된 데이터 저장
    def changeAuth(self, Auth, r):
        if Auth == 0:
            Auth = "Master"
        else: Auth = "Regular"
        self.chgRowList.append(r)
        self.chgAuthList.append(Auth)
        if self.chgRowList.count(r) > 1:
            self.chgRowList.remove(r)
            self.chgAuthList.remove(Auth)

    # 권한이 변경된 데이터 DB에 저장
    def saveAuth(self):
        chgData = []
        if not self.chgAuthList:
            QMessageBox.warning(self, "사원권한변경실패", "권한이 변경된 사원이 없습니다.")
            return
        else:
            j = 0
            # 231214 리스트에 선택된 로우의 사번정보를 리스트에 저장
            for i in self.chgRowList:
                colData = []
                colData.append(self.chgAuthList[j])
                colData.append(int(self.table.item(i,1).text()))
                chgData.append(colData)  
                j+=1

        query = "UPDATE LOGIN_DATA SET AUTHORITY = %s WHERE EMP_NUM = %s"
        reply = QMessageBox.question(self, '변경 확인', '변경하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.executemany(query,(tuple(chgData)))
                self.conn.commit()
                QMessageBox.information(self,"사원권한변경성공","변경되었습니다.") 
                self.setTables(self.main_query)
                self.chgRowList = list()
                self.chgAuthList = list()
            except Exception as e:
                QMessageBox.warning(self, "사원권한변경실패", "Error: " + str(e))
                return       
        self.table.blockSignals(False)
            
            
            
    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)
        

stylesheet = """
    QTableWidget {
        border-radius: 10px;
        background-color: #eeeeee;
        margin-top:20px;   
        margin-bottom:20px;       
        padding-left:20px;          
        padding-right:20px;
    }
    QTableWidget::item {
        background-color: #ffffff;
        margin-top: 5px;    
        margin-bottom:5px;      
        border-radius: 9px;
    }
    QTableWidget::item:selected {
        color: black;
    }
    QHeaderView::section{
        Background-color:#c6c6c6;
        border-radius:5px;
        margin-top:25px; 
        margin-bottom:5px;
    }
    QToolButton{
        border: None;
        color: #868686; 
    }
"""
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = EduList() 
    myWindow.show() 
    app.exec_() 