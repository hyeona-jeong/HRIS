import os
import sys
import openpyxl
import pymysql
import math
import datetime
import re
import shutil

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from add_edu import DialogClass

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('pm_list.ui')
form_class = uic.loadUiType(form)[0]

class PMList(QMainWindow, form_class):
    closed = pyqtSignal()
    def __init__(self,user_info):
        super( ).__init__( )
        self.setupUi(self)
        self.pmList.setStyleSheet(stylesheet)
        # list(ID, EMP_NUM, NAME_KOR, AUTHORITY)
        self.user_info = user_info
        
        # 변경된 셀값 저장
        self.chLists = []
        self.biz = '전체'
        self.name = ''
        self.text = ''
        self.flag = 0
        self.gBtn = []
        self.delRowList = []
        self.current_page = 1
        self.prev_page = None
        self.align_index = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.current_index = 1
        self.file_chk = False
        self.prev_index = None
        self.ignore_paging_btn = False
        self.table.setColumnHidden(25,True)
        self.header = ['','과제코드','과제명','담당자','부서','과제생성일','책임자','부서','고객사','계약금액','공수','정규(명)','파트너(명)','제안일','시작일','완료일','기간','상태','개요','특이사항','첨부파일','확정유무','등록자 ID','등록자 사번','등록자 이름','첨부파일경로']
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  

        self.bizCombo.activated[str].connect(self.searchBiz)
        self.namelineEdit.returnPressed.connect(self.searchEmp)
        self.empSearchBtn.clicked.connect(self.searchEmp)
        
        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)    
        
        self.xlBtn.clicked.connect(self.createExcel)
        self.listRegBtn.clicked.connect(self.registPM)
        self.table.itemChanged.connect(self.delChk)
        self.listDelBtn.clicked.connect(self.delChkList)
        self.table.cellDoubleClicked.connect(self.showPMInfo)

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
        SELECT PM_CODE, PM_NAME, PM_NORI_MANAGER, PM_NORI_BU, PM_CREATE_DATE, PM_MANAGER, 
        PM_BU, PM_BUSINESS, FORMAT(PM_PRICE, 0) AS PM_PRICE, PM_WORKLOAD, PM_FULL, PM_PART, PM_SUGGEST_DATE, 
        PM_START_DATE, PM_END_DATE, PM_WORK_DATE, PM_STATUS, PM_OUTLINE, PM_BEGO, PM_FILE, PM_CONFIRMED, PM_SAVE_ID, PM_SAVE_SA, PM_SAVE_NAME, PM_FILE_PATH
        FROM PM_DATA
        """
        
        #권한에 따라 제한
        if self.user_info[3] != 'Master':
            self.table.setColumnHidden(0,True)
            self.listDelBtn.setVisible(False)
            
        # 231128 table 세팅 by 정현아
        self.table.setRowCount(0)
        self.setTables(self.main_query)
        self.gBtn[0].setChecked(True)
        self.gBtn[0].setStyleSheet(
                    "QToolButton { border: None; color : black; font-weight: bold; }"
                )
        
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

    # 로딩시 커서 변경
    def setLoadingCursor(self, loading):
        if loading:
            QApplication.setOverrideCursor(Qt.WaitCursor)
        else:
            QApplication.restoreOverrideCursor()

    # 231202 테이블 세팅 함수 쿼리값 변경시 테이블위젯에 세팅된 테이블 값도 변경 by 정현아
    def setTables(self, query):
        # 로딩 중에 WaitCursor로 변경
        self.setLoadingCursor(True)
        # 테이블 정렬 상태 확인 후 쿼리를 정렬하는 쿼리로 변경함
        current_sorting_column = self.current_index
        current_sorting_order = self.align_index[self.current_index]%2
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
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                self.table.setItem(row % 15, col + 1, item)
        self.table.blockSignals(False)
        # 로딩이 끝나면 기본 커서로 변경
        self.setLoadingCursor(False) 


    # 231129 사업부검색 함수 
    def searchBiz(self,biz):
        self.table.blockSignals(True)
        self.biz = biz 
        if self.name == '' :
            if self.biz == '전체':
                self.setTables(self.main_query)
            else:
                query = f"""
                SELECT PM_CODE, PM_NAME, PM_NORI_MANAGER, PM_NORI_BU, PM_CREATE_DATE, PM_MANAGER, 
                PM_BU, PM_BUSINESS, FORMAT(PM_PRICE, 0) AS PM_PRICE, PM_WORKLOAD, PM_FULL, PM_PART, PM_SUGGEST_DATE, 
                PM_START_DATE, PM_END_DATE, PM_WORK_DATE, PM_STATUS, PM_OUTLINE, PM_BEGO, PM_FILE, PM_CONFIRMED, PM_SAVE_ID, PM_SAVE_SA, PM_SAVE_NAME, PM_FILE_PATH
                FROM PM_DATA
                WHERE PM_NORI_BU = '{self.biz}' """
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
                SELECT PM_CODE, PM_NAME, PM_NORI_MANAGER, PM_NORI_BU, PM_CREATE_DATE, PM_MANAGER, 
                PM_BU, PM_BUSINESS, FORMAT(PM_PRICE, 0) AS PM_PRICE, PM_WORKLOAD, PM_FULL, PM_PART, PM_SUGGEST_DATE, 
                PM_START_DATE, PM_END_DATE, PM_WORK_DATE, PM_STATUS, PM_OUTLINE, PM_BEGO, PM_FILE, PM_CONFIRMED, PM_SAVE_ID, PM_SAVE_SA, PM_SAVE_NAME, PM_FILE_PATH
                FROM PM_DATA
                WHERE PM_NORI_MANAGER LIKE '%{self.name}%'
                """

            elif self.biz != '전체':
                query = f"""
                SELECT PM_CODE, PM_NAME, PM_NORI_MANAGER, PM_NORI_BU, PM_CREATE_DATE, PM_MANAGER, 
                PM_BU, PM_BUSINESS, FORMAT(PM_PRICE, 0) AS PM_PRICE, PM_WORKLOAD, PM_FULL, PM_PART, PM_SUGGEST_DATE, 
                PM_START_DATE, PM_END_DATE, PM_WORK_DATE, PM_STATUS, PM_OUTLINE, PM_BEGO, PM_FILE, PM_CONFIRMED, PM_SAVE_ID, PM_SAVE_SA, PM_SAVE_NAME, PM_FILE_PATH
                FROM PM_DATA
                WHERE PM_NORI_BU = '{self.biz}' AND PM_NORI_MANAGER LIKE '%{self.name}%'
                """
            self.setTables(query)
        else:
            self.searchBiz(self.biz)
        self.table.blockSignals(False)

    # 231209 정렬할 때마다 헤더 옆에 화살표 특수문자를 붙여서 보여줌 by 정현아
    def onHeaderClicked(self,index):
        if index == 0:
            return
        if self.prev_index != self.current_index:
           self.prev_index = self.current_index
        self.current_index = index
        if self.current_index == self.prev_index:
            self.align_index[index]+=1        
        if index != 0 and self.align_index[index] %2 == 0:
            self.table.setHorizontalHeaderItem(index, QTableWidgetItem(self.header[index]+'▲'))
            self.searchEmp()
        elif index != 0 and self.align_index[index] %2 != 0:
            self.table.setHorizontalHeaderItem(index, QTableWidgetItem(self.header[index]+'▼'))
            self.searchEmp()
        for i in range(len(self.header)):
            if i == index:
                continue
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.header[i]))
        

    def delChk(self, state, row):
        if state == Qt.Checked:
            self.delRowList.append(row)
        elif state == Qt.Unchecked:
            self.delRowList.remove(row)

    # 231202 사원정보 삭제
    def delChkList(self):
        delData = []
        if not self.delRowList :
            QMessageBox.warning(self, "삭제 실패", "선택된 과제가 없습니다.")
            return
        else:
            # 231202 리스트에 선택된 로우의 과제코드를 저장
            for i in self.delRowList :
                colData = []
                if self.table.item(i,21).text() == 'Y':
                    QMessageBox.information(self,"삭제실패", "확정된 과제는 삭제할 수 없습니다.\n" + f"(과제번호: {self.table.item(i,1).text()})")
                    return 
                colData.append(self.table.item(i,1).text())
                delData.append(colData)

        query = 'DELETE FROM PM_DATA WHERE PM_CODE = %s '
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.executemany(query,(tuple(delData)))
                self.conn.commit()
                QMessageBox.information(self,"삭제성공","삭제 되었습니다.") 
                self.setTables(self.main_query)
                self.delRowList = list()
            except Exception as e:
                QMessageBox.warning(self, "삭제실패", "Error: " + str(e))
                return       
                
    def createExcel(self):
        wb = openpyxl.Workbook()
        try:
            if self.biz == '전체':
                if not self.name:
                    query = self.main_query
                else:
                    query = f"""
                    SELECT PM_CODE, PM_NAME, PM_NORI_MANAGER, PM_NORI_BU, PM_CREATE_DATE, PM_MANAGER, 
                    PM_BU, PM_BUSINESS, FORMAT(PM_PRICE, 0) AS PM_PRICE, PM_WORKLOAD, PM_FULL, PM_PART, PM_SUGGEST_DATE, 
                    PM_START_DATE, PM_END_DATE, PM_WORK_DATE, PM_STATUS, PM_OUTLINE, PM_BEGO, PM_FILE, PM_CONFIRMED, PM_SAVE_ID, PM_SAVE_SA, PM_SAVE_NAME, PM_FILE_PATH
                    FROM PM_DATA
                    WHERE PM_NORI_MANAGER LIKE '%{self.name}%'
                    """
            else :
                if not self. name:
                    query = f"""
                    SELECT PM_CODE, PM_NAME, PM_NORI_MANAGER, PM_NORI_BU, PM_CREATE_DATE, PM_MANAGER, 
                    PM_BU, PM_BUSINESS, FORMAT(PM_PRICE, 0) AS PM_PRICE, PM_WORKLOAD, PM_FULL, PM_PART, PM_SUGGEST_DATE, 
                    PM_START_DATE, PM_END_DATE, PM_WORK_DATE, PM_STATUS, PM_OUTLINE, PM_BEGO, PM_FILE,PM_CONFIRMED, PM_SAVE_ID, PM_SAVE_SA, PM_SAVE_NAME, PM_FILE_PATH
                    FROM PM_DATA
                    WHERE PM_NORI_BU = '{self.biz}' """
                else:
                    query = f"""
                    SELECT PM_CODE, PM_NAME, PM_NORI_MANAGER, PM_NORI_BU, PM_CREATE_DATE, PM_MANAGER, 
                    PM_BU, PM_BUSINESS, FORMAT(PM_PRICE, 0) AS PM_PRICE, PM_WORKLOAD, PM_FULL, PM_PART, PM_SUGGEST_DATE, 
                    PM_START_DATE, PM_END_DATE, PM_WORK_DATE, PM_STATUS, PM_OUTLINE, PM_BEGO, PM_FILE, PM_CONFIRMED, PM_SAVE_ID, PM_SAVE_SA, PM_SAVE_NAME, PM_FILE_PATH
                    FROM PM_DATA
                    WHERE PM_NORI_BU = '{self.biz}' AND PM_NORI_MANAGER LIKE '%{self.name}%'
                    """
                    
            self.cur.execute(query)
            result = self.cur.fetchall()
        except Exception as e:
            QMessageBox.warning(self, "엑셀파일추출 실패", "Error: " + str(e))
            return   
        w1 = wb["Sheet"]
        
        for i in range(len(result)):
            for j in range(len(result[i])):
                w1.cell(i+1,j+1).value = result[i][j]
                
        #파일명_날짜로 파일명 자동 적용
        save_filename = '\\과제관리_' + datetime.datetime.now().strftime("%Y-%m-%d")
        
        #본인 계정 경로 추적 및 바탕화면
        save_user_name = os.path.expanduser('~') + '\\Desktop' + save_filename
                                                                   
        fname = QFileDialog.getSaveFileName(self, 'Save file', save_user_name,'Excel file(*xlsx *xls)')


        if fname[0]:
            wb.save(fname[0] + r".xlsx")
            QMessageBox.information(self, "엑셀파일추출 성공", "엑셀파일이 추출되었습니다.")
        else: 
            return
        
    # PM등록 팝업창 생성
    def registPM(self):
        self.w = QDialog(self)
        uic.loadUi(resource_path('pm_regist.ui'), self.w)
        
        self.w.delBtn.setVisible(False)
        
        # 과제코드, 등록자, 등록자 사번 과제생성일, 계약공수 항목을 수정불가처리 및 첨부파일은 ReadOnly로 설정
        self.w.pm_code.setEnabled(False)
        self.w.pm_save_name.setEnabled(False)
        self.w.pm_save_sa.setEnabled(False)
        self.w.pm_save_name.setText(self.user_info[2])
        self.w.pm_save_sa.setText(str(self.user_info[1]))
        #과제생성일은 현재 날짜로 값 설정
        self.w.pm_create_date.setDate(QDate.currentDate())
        self.w.pm_create_date.setEnabled(False)
        self.w.pm_workload.setEnabled(False)
        # 상태를 대기로 설정
        self.w.pm_status.setCurrentText('대기')
        # 확정유무를 N으로 설정
        self.w.pm_confirmed.setCurrentText('N')
        
        # 계약금액, 정규, 파트너 항목에 숫자만 입력가능하도록 입력제한
        self.w.pm_price.setValidator(QIntValidator(self))
        self.w.pm_full.setValidator(QIntValidator(self))
        self.w.pm_part.setValidator(QIntValidator(self))
        
        self.w.pm_file.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.w.pm_file.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        
        self.w.pm_price.textChanged.connect(self.changeIntFormat)
        self.w.attchFileBtn.clicked.connect(self.attachFile)
        self.w.cnlBtn.clicked.connect(self.w.accept)
        self.w.saveBtn.clicked.connect(lambda: self.savePM('regist'))
        self.w.pm_file.cellClicked.connect(self.selectFile)
        self.w.exec_()
        
    # 계약금액입력 콤마추가하여 포맷 변환
    def changeIntFormat(self):
        pm_price = self.w.pm_price.text()
        
        #숫자가 아닌 문자가 들어오면 제거
        chkInt = re.compile('[^0-9]')
        pm_price = chkInt.sub('',pm_price)
        
        #1000자리 숫자마다 콤마 추가
        int_pm_price = int(pm_price.replace(',',''))
        pm_price_comma = format(int_pm_price,',')
        self.w.pm_price.setText(pm_price_comma)
        
      # 파일 copy
    def save_file_at_dir(self, dst_dir_path, sot_dir_path, sot_filename):
        # 디렉토리 생성 (존재하지 않는 경우)
        os.makedirs(dst_dir_path, exist_ok=True)
        
        for source_path, file_name in zip(sot_dir_path, sot_filename):
            source_file_path = os.path.join(source_path, file_name)
            target_file_path = os.path.join(dst_dir_path, file_name)
            
            if source_file_path != target_file_path:                    
                shutil.copy(source_file_path, target_file_path)
        
    # PM정보저장
    def savePM(self,type):
        pm_full = 0 if self.w.pm_full.text() == '' else int(self.w.pm_full.text())
        pm_part = 0 if self.w.pm_part.text() == '' else int(self.w.pm_part.text())
        
        pm_workload = pm_full + pm_part
        pm_price = self.w.pm_price.text()
        
        # 첨부파일 리스트를 문자열로 변환
        file_name = ''
        file_path = ''
        cnt = self.w.pm_file.rowCount()
        for i in range(cnt):
            file_name += self.w.pm_file.item(i,0).text()
            file_path += self.w.pm_file.item(i,2).text()
            if i != cnt-1:
                file_name += ','
                file_path += ','
        
        dir_file_name = file_name.split(',')
        dir_file_path = file_path.split(',')

        #if self.file_chk == True:
            
            #소스 파일
            #dir_paths = (os.path.dirname(self.file_path))
            #dir_files = (os.path.basename(self.file_path))
            
            #dir_paths = [os.path.dirname(self.file_path)]
            #dir_files = [os.path.basename(self.file_path)]
            
            #source_file_path = (",".join(dir_paths))
            #source_file_name = (",".join(dir_files))
        
            #저장 경로
            #dst_file_path = 'C:/HRIS/upload_data/pm_list' + '/' + QDateTime.currentDateTime().toString('yyyyMMddHHmm')
            #dst_file_name = dir_files
            
            #print(dir_paths)
            #print(dir_files)
                                    
        pmAttr ={
            '과제코드': QDateTime.currentDateTime().toString('yyyyMMddHHmm'),  
            '과제명': self.w.pm_name.text(),             
            '담당자': self.w.pm_nori_manager.text(), 
            '부서(담당자)': self.w.pm_nori_bu.currentText(),
            '과제생성일': self.w.pm_create_date.date().toString("yyyy-MM-dd"),
            '책임자':self.w.pm_manager.text(), 
            '부서(책임자)':self.w.pm_bu.text(),  
            '고객사': self.w.pm_business.text(),             
            '계약금액': 0 if pm_price == '' else int(pm_price.replace(',','')),  
            '계약공수': pm_workload,   
            '정규':0 if pm_full == '' else int(pm_full),  
            '파트너':0 if pm_part == '' else int(pm_part),  
            '제안일':self.w.pm_suggest_date.date().toString("yyyy-MM-dd"),    
            '시작일':self.w.pm_start_date.date().toString("yyyy-MM-dd"),
            '완료일':self.w.pm_end_date.date().toString("yyyy-MM-dd"), 
            '기간':self.w.pm_work_date.value(),  
            '상태':self.w.pm_status.currentText(),  
            '개요':self.w.pm_outline.toPlainText() ,             
            '특이사항':self.w.pm_bego.toPlainText() , 
            '첨부파일':file_name, 
            '확정유무':self.w.pm_confirmed.currentText(),
            '등록자 ID':self.user_info[0],
            '등록자 사번':int(self.user_info[1]),
            '등록자 이름':self.user_info[2],
            '첨부파일경로': '' 
                    }
        if pmAttr['첨부파일']  == '':
            pmAttr['첨부파일경로'] = ''
        else :
            pmAttr['첨부파일경로'] = 'C:/HRIS/upload_data/pm_list' + '/' + QDateTime.currentDateTime().toString('yyyyMMddHHmm')
            
        if type == 'regist':
            
            query = """
            INSERT INTO PM_DATA (
                pm_code,
                pm_name,
                pm_nori_manager,
                pm_nori_bu,
                pm_create_date,
                pm_manager,
                pm_bu,
                pm_business,
                pm_price,
                pm_workload,
                pm_full,
                pm_part,
                pm_suggest_date,
                pm_start_date,
                pm_end_date,
                pm_work_date,
                pm_status,
                pm_outline,
                pm_bego,
                pm_file,
                pm_confirmed,
                pm_save_id,
                pm_save_sa,
                pm_save_name,
                pm_file_path
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s ,%s , %s 
            )
            """ 
        elif type == 'edit':
            pmAttr['과제코드'] = self.w.pm_code.text()
            pmAttr['과제생성일'] = self.w.pm_create_date.date().toString("yyyy-MM-dd")
            if pmAttr['첨부파일'] == '':
               pmAttr['첨부파일경로'] = ''
            else:
               pmAttr['첨부파일경로'] = 'C:/HRIS/upload_data/pm_list' + '/' + pmAttr['과제코드']
            
            query = f"""
            UPDATE PM_DATA SET
                pm_code = %s,
                pm_name = %s,
                pm_nori_manager = %s,
                pm_nori_bu = %s,
                pm_create_date = %s,
                pm_manager = %s,
                pm_bu = %s,
                pm_business = %s,
                pm_price = %s,
                pm_workload = %s,
                pm_full = %s,
                pm_part = %s,
                pm_suggest_date = %s,
                pm_start_date = %s,
                pm_end_date = %s,
                pm_work_date = %s,
                pm_status = %s,
                pm_outline = %s,
                pm_bego = %s,
                pm_file = %s,
                pm_confirmed = %s,
                pm_save_id = %s,
                pm_save_sa = %s,
                pm_save_name = %s,
                pm_file_path = %s
            WHERE pm_code = '{pmAttr['과제코드']}'
            """ 
        
        if self.file_chk == True:
        #파일 copy
            self.save_file_at_dir(pmAttr['첨부파일경로'], dir_file_path, dir_file_name)
        else:
            pass
        
        reply = QMessageBox.question(self, '저장 확인', '저장하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.execute(query, tuple(pmAttr.values()))
                self.conn.commit()
                QMessageBox.information(self, "과제 등록 성공", "저장되었습니다.")
                self.w.accept()
                
            except Exception as e:
                QMessageBox.warning(self, "과제 등록 실패", "Error: " + str(e))
                print(str(e))
                return     
            
            finally:
                self.setTables(self.main_query)
                self.gBtn[0].setChecked(True)
                self.gBtn[0].setStyleSheet(
                            "QToolButton { border: None; color : black; font-weight: bold; }"
                        )
                
                
    def showPMInfo(self, row, col):
        pmCode = self.table.item(row, 1).text()
        query = f"""
        SELECT pm_code,
            pm_name,
            pm_nori_manager,
            pm_nori_bu,
            pm_create_date,
            pm_manager,
            pm_bu,
            pm_business,
            FORMAT(PM_PRICE, 0) AS PM_PRICE,
            pm_workload,
            pm_full,
            pm_part,
            pm_suggest_date,
            pm_start_date,
            pm_end_date,
            pm_work_date,
            pm_status,
            pm_outline,
            pm_bego,
            pm_file,
            pm_confirmed,
            pm_save_id,
            pm_save_sa,
            pm_save_name,
            pm_file_path
            FROM PM_DATA
            WHERE PM_CODE = '{pmCode}'
        """
        self.cur.execute(query)
        result = self.cur.fetchone()
        self.w = QDialog(self)
        uic.loadUi(resource_path('pm_regist.ui'), self.w)
        
        self.setViewUI(result)
        self.w.saveBtn.setText('수정')
        self.w.cnlBtn.clicked.connect(self.w.accept)
        self.w.saveBtn.clicked.connect(self.editPM)
        self.w.delBtn.clicked.connect(self.delPM)
        self.w.exec_()
        
    def setViewUI(self, result):
        if not (self.user_info[3] == 'Master' or self.user_info[1] == int(self.w.pm_save_sa.text())):
            self.w.delBtn.setVisible(False)
            self.w.saveBtn.setVisible(False)
        
        self.w.pm_file.setColumnHidden(2,True)
        
        # self.w.attchFileBtn.setVisible(False)
        self.w.pm_save_name.setReadOnly(True)
        self.w.pm_save_sa.setReadOnly(True)
        self.w.pm_code.setReadOnly(True)
        self.w.pm_name.setReadOnly(True)
        self.w.pm_nori_manager.setReadOnly(True)
        self.w.pm_nori_bu.setEnabled(False)
        self.w.pm_create_date.setReadOnly(True)
        self.w.pm_manager.setReadOnly(True)
        self.w.pm_bu.setReadOnly(True)
        self.w.pm_business.setReadOnly(True)
        self.w.pm_price.setReadOnly(True)
        self.w.pm_workload.setReadOnly(True)
        self.w.pm_full.setReadOnly(True)
        self.w.pm_part.setReadOnly(True)
        self.w.pm_suggest_date.setReadOnly(True)
        self.w.pm_start_date.setReadOnly(True)
        self.w.pm_end_date.setReadOnly(True)
        self.w.pm_work_date.setReadOnly(True)
        self.w.pm_status.setEnabled(False)
        self.w.pm_outline.setReadOnly(True)
        self.w.pm_bego.setReadOnly(True)
        self.w.pm_confirmed.setEnabled(False)
        
        self.w.pm_file.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.w.pm_file.setColumnHidden(1,True)
        
        self.w.pm_code.setText(result[0])
        self.w.pm_name.setText(result[1])
        self.w.pm_nori_manager.setText(result[2])
        self.w.pm_nori_bu.setCurrentText(result[3])
        self.w.pm_create_date.setDate(result[4])        
        self.w.pm_manager.setText(result[5])
        self.w.pm_bu.setText(result[6])
        self.w.pm_business.setText(result[7])
        self.w.pm_price.setText(str(result[8]))
        self.w.pm_workload.setText(str(result[9]))
        self.w.pm_full.setText(str(result[10]))
        self.w.pm_part.setText(str(result[11]))
        self.w.pm_suggest_date.setDate(result[12])
        self.w.pm_start_date.setDate(result[13])
        self.w.pm_end_date.setDate(result[14])
        self.w.pm_work_date.setValue(result[15])
        self.w.pm_status.setCurrentText(result[16])
        self.w.pm_outline.setPlainText(result[17])
        self.w.pm_bego.setPlainText(result[18])
        self.w.pm_confirmed.setCurrentText(result[20])   
        self.w.pm_save_name.setText(result[23])
        self.w.pm_save_sa.setText(str(result[22]))
        
        pm_file = result[19].split(',')
        pm_file_path = result[24]
        row = 0
        if pm_file != '':
            for file in pm_file:
                self.w.pm_file.insertRow(row)
                self.w.pm_file.setItem(row,0,QTableWidgetItem(file))
                self.w.pm_file.setItem(row,2,QTableWidgetItem(pm_file_path))
                row += 1
        
    def editPM(self):     
        # self.w.attchFileBtn.setVisible(True)
        self.w.pm_name.setReadOnly(False)
        self.w.pm_nori_manager.setReadOnly(False)
        self.w.pm_nori_bu.setEnabled(True)
        self.w.pm_manager.setReadOnly(False)
        self.w.pm_bu.setReadOnly(False)
        self.w.pm_business.setReadOnly(False)
        self.w.pm_price.setReadOnly(False)
        self.w.pm_workload.setReadOnly(False)
        self.w.pm_full.setReadOnly(False)
        self.w.pm_part.setReadOnly(False)
        self.w.pm_suggest_date.setReadOnly(False)
        self.w.pm_start_date.setReadOnly(False)
        self.w.pm_end_date.setReadOnly(False)
        self.w.pm_work_date.setReadOnly(False)
        self.w.pm_status.setEnabled(True)
        self.w.pm_outline.setReadOnly(False)
        self.w.pm_bego.setReadOnly(False)
        self.w.pm_confirmed.setEnabled(True)
        
        # 2번째 열에 삭제 표시 추가
        row = 0
        for i in range(self.w.pm_file.rowCount()):
            self.w.pm_file.setItem(row,1,QTableWidgetItem('X'))
            self.w.pm_file.item(row, 1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            row += 1
        
        self.w.pm_file.setColumnHidden(1,False)
        self.w.pm_file.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.w.pm_file.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        
        self.w.saveBtn.setText('저장')
        self.w.saveBtn.clicked.connect(lambda: self.savePM('edit'))
        self.w.attchFileBtn.clicked.connect(self.attachFile)
        self.w.pm_file.cellClicked.connect(self.selectFile)
        
    def delPM(self):
        pm_code = self.w.pm_code.text()
        
        if self.w.pm_confirmed.currentText() == 'Y':
            QMessageBox.information(self,"삭제실패", "확정된 과제는 삭제할 수 없습니다.\n" + f"(과제번호: {pm_code})")
        else:
            reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                query = f"DELETE FROM PM_DATA WHERE PM_CODE = '{pm_code}'"
                try:
                    self.cur.execute(query)
                    self.conn.commit()
                    QMessageBox.information(self, "삭제 성공", "삭제되었습니다.")
                    self.w.close()
                except:
                    QMessageBox.warning(self, "과제 삭제 실패", "Error: " + str(e))
                    
                finally:
                    self.setTables(self.main_query)
                    self.gBtn[0].setChecked(True)
                    self.gBtn[0].setStyleSheet(
                                "QToolButton { border: None; color : black; font-weight: bold; }"
                            )
    #첨부파일 선택 이벤트
    def attachFile(self):
        if self.w.pm_file.rowCount() >= 5:
            QMessageBox.warning(self, "추가 실패","첨부파일은 최대 5개까지 추가하실 수 있습니다.")
            return
        
        fname,_ = QFileDialog.getOpenFileName(self, '첨부 파일 추가', 'C:/Program Files', '모든 파일(*.*)')
        file_name = os.path.basename(fname)
        file_path = os.path.dirname(fname)
                
        # 선택된 파일이 있을 시
        if fname:
            # 테이블에 row를 한 줄 추가하고 파일명과 버튼을 각 셀에 배치
            self.w.pm_file.insertRow(0)
            item_file = QTableWidgetItem(file_name)
            item_path = QTableWidgetItem(file_path)
            self.w.pm_file.setItem(0, 0, item_file)
            self.w.pm_file.setItem(0, 1, QTableWidgetItem('X'))
            self.w.pm_file.setItem(0, 2, item_path)
            self.w.pm_file.setColumnHidden(2, True)
            self.w.pm_file.item(0, 1).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.file_chk = True
            
            # # 삭제버튼을 중앙에 위치시키기 위해 위젯을 생성하여 중앙 정렬
            # btnWidget = QWidget()
            # btnLayout = QHBoxLayout(btnWidget)
            # btnLayout.setAlignment(Qt.AlignCenter)
            
            # # 삭제버튼 크기 조정
            # delBtn = QPushButton('X')
            # delBtn.setMinimumSize(28,28)
            # delBtn.setMaximumSize(28,28)
            # delBtn.setStyleSheet("border: none;")
            
            # btnLayout.addWidget(delBtn)
            # btnLayout.setContentsMargins(0, 0, 0, 0)
            # btnWidget.setLayout(btnLayout)
            
            # self.w.pm_file.setCellWidget(self.file_cnt, 1, btnWidget)
        # 선택된 파일이 없을 시 
        else:
            pass
    
    def selectFile(self, row, col):
        if col == 1:
            self.w.pm_file.removeRow(row)
        else:
            pass
        
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
    myWindow = PMList() 
    myWindow.show() 
    app.exec_() 