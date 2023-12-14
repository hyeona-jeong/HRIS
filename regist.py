import os
import sys
import pymysql
import re
import math

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from emp_regist import Regist
from emp_info import EmpInfo
from edit_tap import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('emp_list.ui')
form_class = uic.loadUiType(form)[0]

class Emplist(QMainWindow, form_class):
    closed = pyqtSignal()
    listToInfo = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.setStyleSheet(stylesheet)

        # 231202 체크박스 체크된 ROWW저장 리스트, 사업부검색 콤보박스, 이름검색 라인에딧초기화 by 정현아
        self.delRowList = list()
        self.biz = '전체'
        self.name = ''
        self.w = None
        self.emp_num =None
        self.result = None
        self.path = None
        self.fname = None
        self.pixmap = None
        self.gBtn = []
        self.current_page = 1
        self.prev_page = None
        self.align_index = [0,0,0,0,0,0,0,0]
        self.current_index = 8
        self.prev_index = None
        self.TSP = ['생산실행IT G','생산스케쥴IT G','생산품질IT G','TSP운영 1G','TSP운영 2G','TSP고객총괄','']
        self.FAB = ['빅데이터 G','인프라 G','스마트팩토리 G','']
        self.MIS = ['전기운영 G','PLM G','']
        self.TC = ['TC/TPSS개발파트','화성 TC2.5','SAS TC2.5','']
        self.SP = ['사업기획팀','기술전략팀','']
        self.BS = ['경영지원','']
        self.ignore_paging_btn = False

        self.table.setRowCount(0)
        self.header = ['','부서','이름','직무','직급','직책','휴대폰번호','메일']
        self.table.setColumnCount(len(self.header))
        self.table.setHorizontalHeaderLabels(self.header)

        chk_bx_header = QTableWidgetItem()
        chk_bx_header.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        chk_bx_header.setCheckState(Qt.Unchecked)
        self.table.setHorizontalHeaderItem(0, chk_bx_header)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.conn = pymysql.connect(
            host='localhost',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
        )

        # 231202 사원전체 테이블 세팅 by 정현아
        self.cur = self.conn.cursor()
        self.main_query = "SELECT CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_KOR, POSITION, EMP_RANK, WORK_POS, PHONE, MAIL FROM MAIN_TABLE"
        self.setTables(self.main_query)
        self.gBtn[0].setChecked(True)
        self.gBtn[0].setStyleSheet(
                    "QToolButton { border: None; color : black; font-weight: bold; }"
                )

        # 231202 사원전체 수 라벨에 세팅 by 정현아
        countQuery = "SELECT COUNT(*) FROM MAIN_TABLE;"
        self.cur.execute(countQuery)
        count = self.cur.fetchone()[0]
        self.countLabel.setText("총 "+ str(count) + "건")
        
        # 체크박스와 메일은 컬럼 내용에 맞게 사이즈 설정, 그외 컬럼은 stretch로 설정 by 정현아
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
   
        # 콤보박스 및 버튼 클릭 이벤트 by 정현아
        self.bizCombo.activated[str].connect(self.searchBiz)
        self.namelineEdit.returnPressed.connect(self.searchEmp)
        self.empSearchBtn.clicked.connect(self.searchEmp)

        self.table.itemChanged.connect(self.delChk)
        self.listDelBtn.clicked.connect(self.delChkList)
        self.listRegBtn.clicked.connect(self.showRegsit)
        self.table.cellDoubleClicked.connect(self.showEmpInfo)
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
        # 로딩 중에 WaitCursor로 변경
        self.setLoadingCursor(True)
        # 테이블 정렬 상태 확인 후 쿼리를 정렬하는 쿼리로 변경함
        current_sorting_column = self.current_index
        current_sorting_order = self.align_index[self.current_index]
        # 소팅컬럼 초기화할 때 미리 세팅해놓으면 8로 리턴되어 1로 다시 세팅
        if current_sorting_column == 8:
            current_sorting_column = 1
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
        self.table.horizontalHeader().setSortIndicatorShown(False)

    # 231209 정렬할 때마다 헤더 옆에 화살표 특수문자를 붙여서 보여줌 by 정현아
    def chgHeader(self,index):
        if self.prev_index != self.current_index:
           self.prev_index = self.current_index
        self.current_index = index
        if index != 0 and self.align_index[index] %2 == 0:
            self.table.setHorizontalHeaderItem(index, QTableWidgetItem(self.header[index]+'▲'))
        elif index != 0 and self.align_index[index] %2 != 0:
            self.table.setHorizontalHeaderItem(index, QTableWidgetItem(self.header[index]+'▼'))
        for i in range(len(self.header)):
            if i == index:
                continue
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.header[i]))
        if self.current_index == self.prev_index:
            self.align_index[index]+=1
            
    # 231202 체크된 로우 확인 및 저장 by 정현아
    def delChk(self, state, row):
        if state == Qt.Checked:
            self.delRowList.append(row)
        elif state == Qt.Unchecked:
            self.delRowList.remove(row)
        print(row)

    # 231202 사원정보 삭제
    def delChkList(self):
        self.table.blockSignals(True)
        delData = []
        if not self.delRowList :
            QMessageBox.warning(self, "사원삭제실패", "선택된 사원이 없습니다.")
            return
        else:
            # 231202 리스트에 선택된 로우의 이름과 핸드폰 정보를 리스트에 저장
            for i in self.delRowList :
                colData = []
                colData.append(self.table.item(i,2).text())
                colData.append(self.table.item(i,6).text())
                delData.append(colData)

        query = 'DELETE FROM MAIN_TABLE WHERE NAME_KOR = %s AND PHONE = %s;'
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.executemany(query,(tuple(delData)))
                self.conn.commit()
                QMessageBox.information(self,"사원삭제성공","삭제 되었습니다.") 
                self.setTables(self.main_query)
                self.delRowList = list()
            except Exception as e:
                QMessageBox.warning(self, "사원삭제실패", "Error: " + str(e))
                return       
        self.table.blockSignals(False)

    # 231129 사업부검색 함수 이름 검색란이 비어있는지 체크하고 비어있으면 사업부 콤보박스 체크하여 조건에 맞게 필터링 by 정현아
    def searchBiz(self,biz):
        self.table.blockSignals(True)
        self.biz = biz 
        if self.name == '' :
            if self.biz == '전체':
                self.setTables(self.main_query)
                countQuery = "SELECT COUNT(*) FROM MAIN_TABLE;"
                self.cur.execute(countQuery)
                count = self.cur.fetchone()[0]
                self.countLabel.setText("총 "+ str(count) + "건")
            else:
                query = """SELECT 
                CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_KOR, POSITION, EMP_RANK, WORK_POS, PHONE, MAIL 
                FROM MAIN_TABLE 
                WHERE DEPT_BIZ = '""" + biz +"'"
                self.setTables(query)
                countQuery = "SELECT COUNT(*) FROM MAIN_TABLE WHERE DEPT_BIZ = '" + biz +"';"
                self.cur.execute(countQuery)
                count = self.cur.fetchone()[0]
                self.countLabel.setText("총 "+ str(count) + "건")
        else : 
            self.searchEmp()
        self.table.blockSignals(False)

    # 231129 이름 함수 이름 검색란이 비어있는지 체크하고 비어있지 않으면 사업부 콤보박스 체크하여 조건에 맞게 필터링 by 정현아
    def searchEmp(self):
        self.table.blockSignals(True)
        self.name = self.namelineEdit.text()
        if self.name != '':
            if self.biz == '전체':
                query = """SELECT 
                CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_KOR, POSITION, EMP_RANK, WORK_POS, PHONE, MAIL 
                FROM MAIN_TABLE 
                WHERE NAME_KOR LIKE '%""" + self.name +"%'"
                self.setTables(query)
                countQuery = "SELECT COUNT(*) FROM MAIN_TABLE WHERE NAME_KOR LIKE '%""" + self.name +"%'"
                self.cur.execute(countQuery)
                count = self.cur.fetchone()[0]
                self.countLabel.setText("총 "+ str(count) + "건")
            else :
                query = """SELECT 
                CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_KOR, POSITION, EMP_RANK, WORK_POS, PHONE, MAIL 
                FROM MAIN_TABLE 
                WHERE NAME_KOR LIKE '%""" + self.name +"%' AND DEPT_BIZ = '" + self.biz + "'"
                self.setTables(query)
                countQuery = "SELECT COUNT(*) FROM MAIN_TABLE WHERE NAME_KOR LIKE '%""" + self.name +"%' AND DEPT_BIZ = '" + self.biz + "'"
                self.cur.execute(countQuery)
                count = self.cur.fetchone()[0]
                self.countLabel.setText("총 "+ str(count) + "건")
        else:
            self.searchBiz(self.biz)
        self.table.blockSignals(False)
        
    # 핸드폰 정보를 읽어와 사원 정보를 추출하여 개인정보 조회화면과 연결 by 정현아
    def showEmpInfo(self, row, col):
        phone = self.table.item(row, 6).text()
        query = "SELECT EMP_NUM FROM MAIN_TABLE WHERE PHONE = %s;"
        self.cur.execute(query, (phone,))
        self.emp_num = self.cur.fetchone()[0]
        if self.emp_num is not None:
            self.w = EmpInfo()
            self.listToInfo.emit()
            self.w.show()
            self.hide()
            self.showInfo(self.emp_num)
            self.w.showedEdit.connect(self.showEdit)
            self.w.cnlBtn.clicked.connect(self.back)
            
    # 개인정보조회 화면 출력 by 정현아
    def showInfo(self, emp):
        while self.w.tabWidget.count() > 1:
            self.w.tabWidget.removeTab(1)
        familyTab = FamilyTab(emp,'info')
        self.w.familyTab = familyTab
        self.w.tabWidget.addTab(self.w.familyTab.family, '가족관계')

        contactTab = ContactTab(emp,'info')
        self.w.contactTab = contactTab
        self.w.tabWidget.addTab(self.w.contactTab.contact, '비상연락처')

        schoolTab = SchoolTab(emp,'info')
        self.w.schoolTab = schoolTab
        self.w.tabWidget.addTab(self.w.schoolTab.school, '학력')

        certificationTab = CertificationTab(emp,'info')
        self.w.certificationTab = certificationTab
        self.w.tabWidget.addTab(self.w.certificationTab.certificate, '자격증')
        
        careerTab = CareerTab(emp,'info')
        self.w.careerTab = careerTab
        self.w.tabWidget.addTab(self.w.careerTab.career, '경력')

        technicalTab = TechnicalTab(emp,'info')
        self.w.technicalTab = technicalTab
        self.w.tabWidget.addTab(self.w.technicalTab.technical, '기술사항')

        rpTab = RPTab(emp,'info')
        self.w.rpTab = rpTab
        self.w.tabWidget.addTab(self.w.rpTab.rp, '상벌')

        rsTab = RSTab(emp,'info')
        self.w.rsTab = rsTab
        self.w.tabWidget.addTab(self.w.rsTab.rs, '호봉')
        
        self.w.layout = QVBoxLayout()
        self.w.layout.addWidget(self.w.tabWidget)

        query = """
        SELECT 
        NAME_KOR, EMP_NUM, EMP_RANK, POSITION, PHONE, MAIL, CONCAT(DEPT_BIZ, ' > ', DEPT_GROUP) AS DEPT, NAME_ENG, 
        ADDRESS, WORK_POS, SALARY, DATE_JOIN, IFNULL(HEIGHT,''), IFNULL(WEIGHT,''), MILITARY, MARRY, LAST_EDU,ADDRESS_NUM, PIC 
        FROM MAIN_TABLE 
        WHERE EMP_NUM = %s; 
        """
        self.cur.execute(query,(emp,))
        result = self.cur.fetchone()
        
        self.w.namekor.setText(result[0])
        self.w.empnum.setText(str(result[1]))
        self.w.emprank.setText(result[2])
        self.w.position.setText(result[3])
        self.w.phone.setText(result[4])
        self.w.mail.setText(result[5])
        self.w.dept.setText(result[6])
        self.w.nameeng.setText(result[7])
        self.w.address.setText(result[8])
        self.w.work_pos.setText(result[9])
        self.w.sal.setText(result[10])
        self.w.joindate.setText(str(result[11]))
        self.w.height.setText(str(result[12]))
        self.w.weight.setText(str(result[13]))
        self.w.militay.setText(result[14])
        self.w.marry.setText(result[15])
        self.w.lastedu.setText(result[16])
        self.w.addressnum.setText(str(result[17]))

        data = result[18]
        img = QPixmap()
        img.loadFromData(data, 'PNG')

        resize_pixmap = img.scaled(130,150)
        self.w.pic.setPixmap(resize_pixmap) 

    # 개인정보편집화면으로 이동
    def showEdit(self):
        familyTab = FamilyTab(self.emp_num,'edit')
        self.w.w.familyTab = familyTab
        self.w.w.tabWidget.addTab(self.w.w.familyTab.family, '가족관계')

        contactTab = ContactTab(self.emp_num,'edit')
        self.w.w.contactTab = contactTab
        self.w.w.tabWidget.addTab(self.w.w.contactTab.contact, '비상연락처')

        schoolTab = SchoolTab(self.emp_num,'edit')
        self.w.w.schoolTab = schoolTab
        self.w.w.tabWidget.addTab(self.w.w.schoolTab.school, '학력')

        certificationTab = CertificationTab(self.emp_num,'edit')
        self.w.w.certificationTab = certificationTab
        self.w.w.tabWidget.addTab(self.w.w.certificationTab.certificate, '자격증')
        
        careerTab = CareerTab(self.emp_num,'edit')
        self.w.w.careerTab = careerTab
        self.w.w.tabWidget.addTab(self.w.w.careerTab.career, '경력')

        technicalTab = TechnicalTab(self.emp_num,'edit')
        self.w.w.technicalTab = technicalTab
        self.w.w.tabWidget.addTab(self.w.w.technicalTab.technical, '기술사항')

        rpTab = RPTab(self.emp_num,'edit')
        self.w.w.rpTab = rpTab
        self.w.w.tabWidget.addTab(self.w.w.rpTab.rp, '상벌')

        rsTab = RSTab(self.emp_num,'edit')
        self.w.w.rsTab = rsTab
        self.w.w.tabWidget.addTab(self.w.w.rsTab.rs, '호봉')
        
        self.w.w.layout = QVBoxLayout()
        self.w.w.layout.addWidget(self.w.w.tabWidget)
        
        query = """
        SELECT 
        NAME_KOR, NAME_ENG, EMP_NUM, DATE_JOIN, EMP_RANK, SUBSTRING(REG_NUM,1,6), SUBSTRING(REG_NUM,7,7), MAIL, SUBSTRING(PHONE,1,3), SUBSTRING(PHONE,4,4), 
        SUBSTRING(PHONE,8,4), DEPT_BIZ, WORK_POS, POSITION, ADDRESS_NUM, ADDRESS, SUBSTRING(SALARY,1,1), 
        IFNULL(HEIGHT,''), IFNULL(WEIGHT,''), IFNULL(MILITARY,''), IFNULL(MARRY,''), LAST_EDU, PIC, DEPT_GROUP, SUBSTRING(SALARY,2,3), AGE, GENDER
        FROM MAIN_TABLE
        WHERE EMP_NUM = %s; 
        """
        self.cur.execute(query,(self.emp_num))
        self.result = self.cur.fetchone()

        self.w.w.dept.activated[str].connect(self.changeGroup)
        self.w.w.addImgBtn.clicked.connect(self.showAddImg)
        self.w.w.regnum_lineEdit2.setEchoMode(QLineEdit.Password)

        # 231201 입력 제한 by 정현아
        self.w.w.regnum_lineEdit.setValidator(QIntValidator(1,100000,self))
        self.w.w.regnum_lineEdit2.setValidator(QIntValidator(1,1000000,self))
        self.w.w.phone_lineEdit2.setValidator(QIntValidator(1,1000,self))
        self.w.w.phone_lineEdit3.setValidator(QIntValidator(1,1000,self))
        self.w.w.addressnum_lineEdit.setValidator(QIntValidator(1,10000,self))
        rep = QRegExp("[가-힣0-9\\s,()]{0,49}")
        self.w.w.address_lineEdit.setValidator(QRegExpValidator(rep))
        self.w.w.height_lineEdit.setValidator(QIntValidator(1,100,self))
        self.w.w.weight_lineEdit.setValidator(QIntValidator(1,100,self))

        # 231201 저장된 사원정보가져와 라벨 및 에디트에 세팅 by 정현아
        self.w.w.namekor.setText(self.result[0])
        self.w.w.nameeng.setText(self.result[1])
        self.w.w.empnum.setText(str(self.result[2]))
        date_str = self.result[3].strftime("%Y-%m-%d")
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        self.w.w.joindate.setDate(date)
        self.w.w.emprank.setCurrentText(self.result[4])
        self.w.w.regnum_lineEdit.setText(self.result[5])
        self.w.w.regnum_lineEdit2.setText(self.result[6])
        self.w.w.mail_lineEdit.setText(self.result[7])
        self.w.w.phone_combo.setCurrentText(self.result[8])
        self.w.w.phone_lineEdit2.setText(self.result[9])
        self.w.w.phone_lineEdit3.setText(self.result[10])
        self.w.w.dept.setCurrentText(self.result[11])

        self.w.w.work_pos.setCurrentText(self.result[12])
        self.w.w.position.setCurrentText(self.result[13])
        self.w.w.addressnum_lineEdit.setText(str(self.result[14]))
        self.w.w.address_lineEdit.setText(self.result[15])
        self.w.w.sal.setCurrentText(self.result[16])
        self.w.w.height_lineEdit.setText(str(self.result[17]))
        self.w.w.weight_lineEdit.setText(str(self.result[18]))
        mil = self.result[19]
        if mil == '군필':
            self.w.w.milBtn.setChecked(True)
        elif mil == '미필':
            self.w.w.milBtn2.setChecked(True)
        else:
            self.w.w.milBtn3.setChecked(True)
        
        marry = self.result[20]
        if marry == '기혼':
            self.w.w.maryyBtn.setChecked(True)
        else : 
            self.w.w.maryyBtn2.setChecked(True)
            
        self.w.w.lastedu_combo.setCurrentText(self.result[21])

        img = QPixmap()
        img.loadFromData(self.result[22], 'PNG')
        resize_pixmap = img.scaled(130,150)
        self.w.w.pic.setPixmap(resize_pixmap) 
        self.w.w.saveBtn.clicked.connect(self.saveEdit)
        
        self.changeGroup(self.result[11])
        self.w.w.dept_g.setCurrentText(self.result[23])
        self.w.w.sal2.setText(self.result[24])
    
    # 사업부 선택시 그룹명 동적으로 세팅
    def changeGroup(self,biz):
        self.w.w.dept_g.clear()
        if biz == '경영지원실':
            self.w.w.dept_g.addItems(self.BS)
        elif biz == 'TSP':
            self.w.w.dept_g.addItems(self.TSP)
            return
        elif biz == 'FAB':
            self.w.w.dept_g.addItems(self.FAB)
            return
        elif biz == 'MIS':
            self.w.w.dept_g.addItems(self.MIS)
            return
        elif biz == 'TC':
            self.w.w.dept_g.addItems(self.TC)
            return
        elif biz == '전략기획실':    
            self.w.w.dept_g.addItems(self.SP) 
            return        

    # 개인정보편집에서 수정한 내용 DB에 저장
    def saveEdit(self):
        date_str = self.result[3].strftime("%Y-%m-%d")
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        attrDict ={
            '주민번호': self.result[5] + self.result[6],  
            '메일': self.result[7], 
            '휴대폰번호': self.result[8] + self.result[9] + self.result[10],  
            '우편번호':self.result[14],
            '주소':self.result[15], 
            '신장': self.result[17],  
            '체중': self.result[18],             
            '군필여부': self.result[19], 
            '결혼여부': self.result[20],  
            '최종학력': self.result[21],            
            '사진': self.result[22],
            '한글성명': self.result[0],
            '영문성명': self.result[1],
            '사번': self.result[2],
            '입사일': date,
            '직급': self.result[4],
            '사업부': self.result[11],
            '직책': self.result[12],
            '그룹': self.result[23],
            '직무': self.result[13],
            '호봉': self.result[16] + self.result[24],
            '나이': self.result[25],
            '성별': self.result[26]
            }        
        attrDict['주민번호'] = self.w.w.regnum_lineEdit.text() + self.w.w.regnum_lineEdit2.text()
        reg_num = self.w.w.regnum_lineEdit.text() + self.w.w.regnum_lineEdit2.text()
        attrDict['메일'] = self.w.w.mail_lineEdit.text()
        attrDict['휴대폰번호'] = self.w.w.phone_combo.currentText() + self.w.w.phone_lineEdit2.text() + self.w.w.phone_lineEdit3.text()
        if self.w.w.addressnum_lineEdit.text() == '':
            QMessageBox.warning(self, "사원등록실패", "우편번호가 입력되지 않았습니다. 우편번호 입력바랍니다.")
            return
        else:
            attrDict['우편번호'] = int(self.w.w.addressnum_lineEdit.text())
        attrDict['주소'] = self.w.w.address_lineEdit.text()

        height = self.w.w.height_lineEdit.text()
        weight = self.w.w.weight_lineEdit.text()

        if height == '': 
            attrDict['신장'] = None
        else:
            attrDict['신장'] = int(height)

        if weight == '': 
            attrDict['체중'] = None
        else:
            attrDict['체중'] = int(weight)       


        if self.w.w.milBtn.isChecked():
            attrDict['군필여부'] = self.w.w.milBtn.text()
        elif self.w.w.milBtn2.isChecked():
            attrDict['군필여부'] = self.w.w.milBtn2.text()
        else:
            attrDict['군필여부'] = self.w.w.milBtn3.text()
            
        if self.w.w.maryyBtn.isChecked():
            attrDict['결혼여부'] = self.w.w.maryyBtn.text()
        else:
            attrDict['결혼여부'] = self.w.w.maryyBtn2.text()    
        attrDict['최종학력'] = self.w.w.lastedu_combo.currentText()

        if self.pixmap is not None:
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            self.pixmap.toImage().save(buffer, 'PNG')
            attrDict['사진'] = byte_array.data()  

        attrDict['한글성명'] = self.w.w.namekor.text()
        attrDict['영문성명'] = self.w.w.nameeng.text()
        # 사번은 int type
        if self.w.w.empnum.text() != '' :
            attrDict['사번'] = int(self.w.w.empnum.text())
        attrDict['입사일'] = self.w.w.joindate.date().toString("yyyy-MM-dd")
        attrDict['직급'] = self.w.w.emprank.currentText()
        attrDict['사업부'] = self.w.w.dept.currentText()
        attrDict['직책'] = self.w.w.work_pos.currentText()
        attrDict['그룹'] = self.w.w.dept_g.currentText()
        attrDict['직무'] = self.w.w.position.currentText()
        attrDict['호봉'] = self.w.w.sal.currentText() + self.w.w.sal2.text()


        for key, value in attrDict.items():
            if key =='휴대폰번호':
                if len(value) < 11 :
                    QMessageBox.warning(self, "개인정보변경실패", "{} 11자리가 입력되지 않았습니다. {} 입력바랍니다.".format(key, key))
                    return
            elif not (key == '신장' or key == '체중'):
                if value == '':
                    QMessageBox.warning(self, "개인정보변경실패", "{}이(가) 입력되지 않았습니다. {} 입력바랍니다.".format(key, key))
                    return
        
        if attrDict['주민번호'] == '' or len(attrDict['주민번호']) != 13:
            QMessageBox.warning(self, "개인정보변경실패", "주민번호 13자리가 입력되지 않았습니다. 주민번호 입력바랍니다.")
            return
        else:
            if reg_num[6] == '0' or reg_num[6] == '9' :
                QMessageBox.warning(self, "개인정보변경실패", "주민번호 2번째 첫자리는 1~8까지 입력가능합니다.")
                return
            elif reg_num[6] == '1' or reg_num[6] == '2' or reg_num[6] == '5' or reg_num[6] == '6':
                birthYear = 1900 + int(reg_num[:2])
            elif reg_num[6] == '3' or reg_num[6] == '4' or reg_num[6] == '7' or reg_num[6] == '8':
                birthYear = 2000 + int(reg_num[:2])
            

            if int(reg_num[2:4])>12 or reg_num[2:4] =='00' or reg_num[4:6] == '00':
                QMessageBox.warning(self, "개인정보변경실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                return
            elif reg_num[2:4] =='01' or  reg_num[2:4] =='03' or reg_num[2:4] =='05' or reg_num[2:4] == '07' or reg_num[2:4] == '08' or reg_num[2:4] == '10' or reg_num[2:4] == '12':
                if int(reg_num[4:6]) > 31:
                    QMessageBox.warning(self, "개인정보변경실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
            elif reg_num[2:4] =='04' or reg_num[2:4] =='06' or reg_num[2:4] =='09' or reg_num[2:4] =='11':
                if int(reg_num[4:6]) > 30:
                    QMessageBox.warning(self, "개인정보변경실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
            else:
                if int(reg_num[4:6]) > 28:
                    QMessageBox.warning(self, "개인정보변경실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
                
            age =  int(QDate(birthYear,int(reg_num[2:4]),int(reg_num[4:6])).daysTo(QDate.currentDate())/365)
            if age < 19:
                QMessageBox.warning(self, "개인정보변경실패", "나이가 만 19세보다 어립니다.주민번호 확인바랍니다.")
                return
            elif age > 80:
                QMessageBox.warning(self, "개인정보변경실패", "나이가 만 80세보다 많습니다.주민번호 확인바랍니다.")
                return
            else:
                attrDict['나이'] = age

            if int(reg_num[6]) % 2 == 1:
                attrDict['성별'] = '남'
            else : 
                attrDict['성별'] = '여'

        if len(str(attrDict['사번'])) < 8:
            QMessageBox.warning(self,'개인정보변경실패','사번은 8자리를 입력하셔야 합니다.')
            return
        
        if int(str(attrDict['사번'])[:2]) < 12 or int(str(attrDict['사번'])[:2]) > int(QDate.currentDate().year())-2000:
            QMessageBox.warning(self,'개인정보변경실패','사번은 앞 2자리는 12보다 작거나 현재년도보다 클 수 없습니다.')
            return

        
        if not re.match(r"^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", attrDict['메일']):
            QMessageBox.warning(self,'개인정보변경실패','메일 형식이 틀립니다.메일 확인바랍니다.')
            return
        
        if len(str(attrDict['우편번호'])) != 5:
            QMessageBox.warning(self, "개인정보변경실패", "우편번호는 5자리를 입력하셔야 합니다.")
            return
        
        if self.result[5] + self.result[6] != attrDict['주민번호'] or self.result[2] != attrDict['사번'] or self.result[8] + self.result[9] + self.result[10] != attrDict['휴대폰번호']:
            t1 = (attrDict['사번'], attrDict['주민번호'], attrDict['사번'], attrDict['주민번호'], attrDict['휴대폰번호'])
            query = """
            SELECT NULLIF(EMP_NUM, %s), NULLIF(REG_NUM, %s), PHONE FROM MAIN_TABLE WHERE EMP_NUM= %s OR REG_NUM = %s OR PHONE = %s;
            """
            try:
                self.cur.execute(query, t1)
                result = self.cur.fetchone()
                if result :
                    if result[0] is not None:
                        QMessageBox.warning(self, "개인정보변경실패", "이미 등록된 사번입니다.")
                        return
                    elif result[1] is not None: 
                        QMessageBox.warning(self, "개인정보변경실패", "이미 등록된 주민번호입니다.")
                        return
                    else: 
                        QMessageBox.warning(self, "개인정보변경실패", "이미 등록된 휴대폰번호입니다.")
                        return
            except Exception as e:
                QMessageBox.warning(self, "개인정보변경실패", "Error: " + str(e))
                return        

        query = """
        UPDATE MAIN_TABLE 
        SET REG_NUM = %s, MAIL = %s, PHONE = %s, ADDRESS_NUM = %s, ADDRESS = %s, HEIGHT = %s, WEIGHT = %s, MILITARY = %s, 
        MARRY = %s, LAST_EDU = %s, PIC = %s, NAME_KOR = %s, NAME_ENG = %s, EMP_NUM = %s, DATE_JOIN =%s, EMP_RANK = %s, 
        DEPT_BIZ = %s, WORK_POS = %s, DEPT_GROUP = %s, POSITION = %s, SALARY =%s, AGE = %s, GENDER = %s
        WHERE EMP_NUM = %s; 
        """
        reply = QMessageBox.question(self, '변경 확인', '변경하시겠습니까??', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cur.execute(query,tuple(attrDict.values()) + (self.emp_num,))
                self.conn.commit()
                self.w.w.familyTab.saveFamily(self.emp_num,self.cur,self.conn)
                self.w.w.contactTab.saveContact(self.emp_num,self.cur,self.conn)
                self.w.w.schoolTab.saveSchool(self.emp_num,self.cur,self.conn)
                self.w.w.certificationTab.saveCertification(self.emp_num,self.cur,self.conn)
                self.w.w.careerTab.saveCareer(self.emp_num,self.cur,self.conn)
                self.w.w.technicalTab.saveTechnical(self.emp_num,self.cur,self.conn)
                self.w.w.rpTab.saveRP(self.emp_num,self.cur,self.conn)
                self.w.w.rsTab.saveRS(self.emp_num,self.cur,self.conn)
                
                QMessageBox.information(self, "개인정보변경성공", "개인정보가 변경되었습니다.")
                self.w.w.close()

                self.showInfo(self.emp_num)              

            except Exception as e:
                QMessageBox.warning(self, "개인정보변경실패", "Error: " + str(e))
                return 

    # 이미지 저장 팝업창 생성
    def showAddImg(self):
        self.w1 = QDialog(self)
        addImg = uic.loadUi(resource_path('add_img.ui'), self.w1)
        self.w1.searchbutton.clicked.connect(self.openImage)
        self.w1.savebtn.clicked.connect(self.save_img)
        self.w1.cnlBtn.clicked.connect(self.w1.accept)
        result = self.w1.exec_() 
    
    # 231130 이미지 선택하고 다이알로그 텍스트 라인 에디트에 파일경로 세팅 by 정현아
    def openImage(self):
        self.path = None
        self.fname = None
        self.fname, _ = QFileDialog.getOpenFileName(self, '이미지 파일 찾기', 'C:/Program Files', '이미지 파일(*.jpg *.gif, *.png)')
        if self.fname:
            max_file_size_mb = 1
            max_file_size_bytes = max_file_size_mb * 1024 * 1024
            
            size, self.path = self.getFileSize(self.fname)
            if size >= max_file_size_bytes:
                QMessageBox.warning(self,'사진등록실패','사진 사이즈가 1MB를 초과하였습니다.')
                return
            else:
                self.w1.imgPath_textEdit.setText(self.path)
                self.w1.hide()
                self.w1.show()

    # 이미지 파일 사이즈 확인
    def getFileSize(self, file_path):
        return os.path.getsize(file_path), file_path
    
    # 231130 선택한 이미지 등록화면에 띄우기 by 정현아
    def save_img(self):
        if self.path is None :
            QMessageBox.warning(self,'사진등록실패','선택된 사진이 없습니다.')
            return
        else: 
                self.pixmap = QPixmap(self.fname)
                width = 130
                height = 150
                resize_pixmap = self.pixmap.scaled(width,height)
                self.w.w.pic.setPixmap(resize_pixmap)
        self.w1.close()

    # 231122 페이지 전환 함수 by정현아
    def showRegsit(self):
        self.w = Regist()
        self.w.show()
        self.hide()
        self.w.cnlBtn.clicked.connect(self.back)
        self.w.closed.connect(self.show)

    def back(self):
        self.w.hide()
        self.show()

    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
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
        border-radius: 9px;
        color: #404040;
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
    myWindow = Emplist() 
    myWindow.show() 
    app.exec_()