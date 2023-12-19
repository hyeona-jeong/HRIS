import pymysql

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class FamilyTab(QWidget):
    def __init__(self, emp_num, type):
        super(FamilyTab, self).__init__()
        self.cnt = 0
        self.no_del_cnt = 0
        self.result_num = 0
        self.edit_num = 0
        self.emp_num = emp_num
        self.type = type
        self.initUI()

    def initUI(self):
        self.family = QScrollArea()
        self.widget = QWidget()
        self.family.setWidget(self.widget)
        self.lay = QGridLayout(self.widget)
        self.family.setWidgetResizable(True)

        self.fName_lbl = []
        self.fName_le = []
        self.fYear_lbl = []
        self.fYear_de = []
        self.fRel_lbl = []
        self.fRel_cb = []
        self.fLive_lbl = []
        self.fLive_cb = []
        self.familyWidget = [self.fName_lbl, self.fName_le, self.fYear_lbl, self.fYear_de, self.fRel_lbl, 
                             self.fRel_cb, self.fLive_lbl, self.fLive_cb]
        self.ignored_result = False
        if self.type == 'info':
            self.addFamilyMember()
        else: 
            self.add_btn = QPushButton("추가")
            self.btnGroup = QButtonGroup(self)
            self.del_btn = []
            self.idx_list = []
            self.editFamilyMember()
            self.cnt = self.result_num
            self.edit_num = self.result_num
            self.del_idx = []
            self.add_btn.clicked.connect(self.editFamilyMember)
            self.btnGroup.buttonClicked[int].connect(self.disappearFamily)

    # info화면에서 DB정보를 가져와서 라벨에 세팅
    def addFamilyMember(self):
        result = self.setData(self.emp_num)
        if not result :
            return
        else :
            self.cnt = len(result)
        #데이터 세팅
        for i in range(self.cnt):
            self.fName_lbl.append(QLabel("가족성명:"))
            self.fName_le.append(QLabel(result[i][0]))
            self.fYear_lbl.append(QLabel("생년월일:"))
            self.fYear_de.append(QLabel(str(result[i][1])))
            self.fRel_lbl.append(QLabel("관계:"))
            self.fRel_cb.append(QLabel(result[i][2]))
            self.fLive_lbl.append(QLabel("동거여부:"))
            self.fLive_cb.append(QLabel(result[i][3]))

        for j in range(self.cnt):
            for i in range(len(self.familyWidget)):
                if i == 0:
                    self.lay.addWidget(self.familyWidget[i][j],0 + 4 * j,0)
                elif i % 2 == 0:
                    self.lay.addWidget(self.familyWidget[i][j],int(i/2) + 4 * j,0)
                elif i % 2 == 1:
                    self.lay.addWidget(self.familyWidget[i][j],int(i/2) + 4 * j,1)
        
        self.lay.setRowStretch(self.lay.rowCount(), 1)
        rightmost_column_index = len(self.familyWidget) - 1
        self.lay.setColumnStretch(rightmost_column_index, 1)

    def editFamilyMember(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result or self.ignored_result:
            self.cnt = len(self.fName_le)
            if(self.cnt<=4):
                self.fName_lbl.append(QLabel("가족성명"))
                self.fName_le.append(QLineEdit(self))
                self.fYear_lbl.append(QLabel("생년월일"))
                self.fYear_de.append(QDateEdit(self))
                self.fRel_lbl.append(QLabel("관계"))
                self.fRel_cb.append(QComboBox())
                self.f_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
                for i in range(len(self.f_list)):
                    self.fRel_cb[self.cnt].addItem(self.f_list[i])
                self.fLive_lbl.append(QLabel("동거여부"))
                self.fLive_cb.append(QComboBox())
                self.fLive_cb[self.cnt].addItem('Y')
                self.fLive_cb[self.cnt].addItem('N')
                
                for i in range(len(self.familyWidget)):
                    if i == 0:
                        self.lay.addWidget(self.familyWidget[i][self.cnt],0 + 4 * self.cnt,0)
                    elif i % 2 == 0:
                        self.lay.addWidget(self.familyWidget[i][self.cnt],int(i/2) + 4 * self.cnt,0)
                    elif i % 2 == 1:
                        self.lay.addWidget(self.familyWidget[i][self.cnt],int(i/2) + 4 * self.cnt,1)
                        if i % 4 == 3:
                            self.lay.addWidget(self.add_btn,int(i/2) + 4 * self.cnt,2)
                
                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.cnt+=1
            else:
                QMessageBox.information(self,"경고","5번 이상 등록하실 수 없습니다.")
        # 231205 있을 경우 등록된 데이터를 각 에디터에 세팅 by 정현아
        else :
            self.result_num = len(result)
            if(len(result) + self.no_del_cnt<=5):            
                #데이터 세팅
                if self.no_del_cnt == 0:
                    for i in range(len(result)):
                        self.fName_lbl.append(QLabel("가족성명:"))
                        self.fName_le.append(QLineEdit(result[i][0]))
                        self.fYear_lbl.append(QLabel("생년월일:"))
                        self.fYear_de.append(QDateEdit(QDate.fromString(result[i][1].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.fRel_lbl.append(QLabel("관계:"))
                        self.fRel_cb.append(QComboBox())
                        self.f_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
                        for j in range(len(self.f_list)):
                            self.fRel_cb[i].addItem(self.f_list[j])
                        self.fRel_cb[i].setCurrentText(result[i][2])
                        self.fLive_lbl.append(QLabel("동거여부:"))
                        self.fLive_cb.append(QComboBox())
                        self.fLive_cb[i].addItems(['Y', 'N'])
                        self.fLive_cb[i].setCurrentText(result[i][3])
                        self.del_btn.append(QPushButton("삭제",self))
                        self.btnGroup.addButton(self.del_btn[i])
                        self.idx_list.append(result[i][4])
                        
                elif self.no_del_cnt != 0:
                    self.fName_lbl.append(QLabel("가족성명"))
                    self.fName_le.append(QLineEdit())
                    self.fYear_lbl.append(QLabel("생년월일"))
                    self.fYear_de.append(QDateEdit())
                    self.fRel_lbl.append(QLabel("관계"))
                    self.fRel_cb.append(QComboBox())
                    self.f_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
                    for i in range(len(self.f_list)):
                        self.fRel_cb[self.no_del_cnt+len(result)-1].addItem(self.f_list[i])
                    self.fLive_lbl.append(QLabel("동거여부"))
                    self.fLive_cb.append(QComboBox())
                    self.fLive_cb[self.no_del_cnt+len(result)-1].addItem('Y')
                    self.fLive_cb[self.no_del_cnt+len(result)-1].addItem('N')
                    
                # 라벨 및 에디터 레이아웃에 세팅(홀수번째는 라벨, 짝수번째는 에디터로 각 레이아웃에 배치)
                for j in range(len(result)+self.no_del_cnt):
                    for i in range(len(self.familyWidget)):
                        if i == 0:
                            self.lay.addWidget(self.familyWidget[i][j],0 + 4 * j,0)
                        elif i % 2 == 0:
                            self.lay.addWidget(self.familyWidget[i][j],int(i/2) + 4 * j,0)
                            if i % 4 == 2:
                                if j < len(result):
                                    self.lay.addWidget(self.del_btn[j], int(i/2)-1 + 4 * j,2)
                        elif i % 2 == 1:
                            self.lay.addWidget(self.familyWidget[i][j],int(i/2) + 4 * j,1)
                            if i % 4 == 3:
                                self.lay.addWidget(self.add_btn,int(i/2) + 4 * j,2)
                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.no_del_cnt+=1
                self.cnt+=1
            else:
                QMessageBox.information(self,"경고","5번 이상 등록하실 수 없습니다.")
            
    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT NAME_FAMILY, BIRTH, REL, LIVE, IDX FROM FAMILY WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    # 231205 변경된 데이터 저장, 기존에 등록된 정보가 있을 경우 UPDATE, 없으면 INSERT
    def saveFamily(self, emp_num, cur, conn):
        # 저장된 정보를 가져옴
        result = self.setData(self.emp_num)
        # 저장된 정보가 있으면 update 없으면 insert
        if not result and self.fName_le[0].text() == '':
            return
        for i in range(len(self.fName_lbl)):
            fName = self.fName_le[i].text()
            fYear = self.fYear_de[i].date().toString("yyyy-MM-dd")
            birth = self.fYear_de[i].date()
            age = int(birth.daysTo(QDate.currentDate())/365)
            fRel = self.fRel_cb[i].currentText()
            fLive = self.fLive_cb[i].currentText()
            # 저장된 데이터가 있으면 UPDATE, 없으면 INSERT
            if i < len(self.idx_list):
                idx = self.idx_list[i]
                query = "UPDATE FAMILY SET NAME_FAMILY = %s, BIRTH = %s, AGE = %s, REL = %s, LIVE = %s WHERE IDX = %s;"
                cur.execute(query, (fName, fYear, age, fRel, fLive, idx,))
            elif self.fName_le[i].text() != '':
                query = "INSERT INTO FAMILY(EMP_NUM, NAME_FAMILY, BIRTH, AGE, REL, LIVE) VALUES(%s, %s, %s, %s, %s, %s)"
                cur.execute(query, (emp_num, fName, fYear, age, fRel, fLive))
            conn.commit() 
        # 저장된 삭제리스트가 있으면 삭제
        if self.del_idx:
            for idx in self.del_idx:
                query = "DELETE FROM FAMILY WHERE EMP_NUM = %s AND IDX = %s;"
                cur.execute(query, (emp_num, idx,))
                conn.commit() 

    # 231217 UI에서 위젯 삭제 by 정현아    
    def disappearFamily(self,index):
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까?\n삭제 후 저장버튼을 누르면 삭제됩니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        else:
            j=0
            btn = self.btnGroup.button(index)
            # 삭제할 위젯 행 찾기
            for i in range(len(self.del_btn)):
                if btn == self.del_btn[i]:
                    j = i
            # 삭제할 위젯의 인덱스 저장 
            del_item = self.idx_list.pop(j)
            self.del_idx.append(del_item)
            # j번째 행의 값을 뺀 후, 그 다음 행의 값을 해당 위치로 이동
            for i in range(len(self.fName_lbl) - 1):
                if i >= j:
                    # 현재 행을 j행으로 이동
                    self.fName_le[i].setText(self.fName_le[i + 1].text())
                    self.fYear_de[i].setDate(self.fYear_de[i + 1].date())
                    self.fRel_cb[i].setCurrentText(self.fRel_cb[i + 1].currentText())
                    self.fLive_cb[i].setCurrentText(self.fLive_cb[i + 1].currentText())
            # 위젯이 하나 남기 전까지 위젯 삭제
            if self.edit_num != 1:
                # 위젯 한줄씩 삭제
                for i in range(len(self.familyWidget)):
                    self.lay.removeWidget(self.familyWidget[i][self.edit_num-1])
                    self.familyWidget[i].pop(self.edit_num-1)
                self.lay.removeWidget(self.del_btn[self.edit_num-1])
                self.btnGroup.removeButton(self.del_btn[self.edit_num-1])
                self.del_btn.pop(self.edit_num-1)  
                self.cnt-=1
            # 위젯이 하나 남을 경우 에디터 초기화
            else : 
                self.fName_le[i].setText("")
                self.fYear_de[i].setDate(QDate(2000, 1, 1))
                self.fRel_cb[i].setCurrentIndex(0)
                self.fLive_cb[i].setCurrentIndex(0)
            self.edit_num-=1
            # 위젯이 전부 제거되기 전까지만 추가 버튼 위치 변경
            if self.edit_num != 0:
                self.lay.addWidget(self.add_btn, 3 + 4 * (len(self.fName_lbl)-1), 2)
            self.lay.setRowStretch(self.lay.rowCount(), 1)      
            # 위젯이 전부 제거 되면 다시 입력창 생성
            if self.cnt == 0:
                self.editFamilyMember()
            self.ignored_result = True
        
class ContactTab(QWidget):
    def __init__(self, emp_num, type):
        super(ContactTab, self).__init__()
        self.cnt = 0
        self.no_del_cnt = 0
        self.result_num = 0
        self.edit_num = 0
        self.emp_num = emp_num
        self.type = type
        self.initUI()

    def initUI(self):
        self.contact = QScrollArea()
        self.cwidget = QWidget()
        self.contact.setWidget(self.cwidget)
        self.lay = QGridLayout(self.cwidget)
        self.contact.setWidgetResizable(True)

        self.cName_lbl = []
        self.cName_le = []
        self.cRel_lbl = []
        self.cRel_cb = []
        self.cCont_lbl = []
        self.cCont_le = []
        self.contactWidget = [self.cName_lbl, self.cName_le, self.cRel_lbl, self.cRel_cb, self.cCont_lbl, self.cCont_le]
        self.ignored_result = False
        if self.type =='info':
            self.addContact()
        else:
            self.add_btn = QPushButton("추가")
            self.btnGroup = QButtonGroup(self)
            self.del_btn = []
            self.idx_list = []
            self.editContact()
            self.cnt = self.result_num
            self.edit_num = self.result_num
            self.del_idx = []
            self.add_btn.clicked.connect(self.editContact)
            self.btnGroup.buttonClicked[int].connect(self.disappearContact)
            
    # info화면에서 DB정보를 가져와서 라벨에 세팅
    def addContact(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.cName_lbl.append(QLabel("성명:"))
            self.cName_le.append(QLabel(result[i][0]))
            self.cRel_lbl.append(QLabel("관계:"))
            self.cRel_cb.append(QLabel(result[i][1]))
            self.cCont_lbl.append(QLabel("연락처:"))
            self.cCont_le.append(QLabel(result[i][2]))

        for j in range(self.cnt):
            for i in range(len(self.contactWidget)):
                if i % 2 == 0:
                    self.lay.addWidget(self.contactWidget[i][j], int(i/2) + 3 * j, 0)
                elif i % 2 == 1:
                    self.lay.addWidget(self.contactWidget[i][j], int(i/2) + 3 * j, 1)

        self.lay.setRowStretch(self.lay.rowCount(), 1)
        rightmost_column_index = len(self.contactWidget) - 1
        self.lay.setColumnStretch(rightmost_column_index, 1)

    def editContact(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 또는 위젯이 삭제되었을 경우 by 정현아
        if not result or self.ignored_result:
            self.cnt = len(self.cName_le)
            if(self.cnt<=1):
                self.cName_lbl.append(QLabel("성명"))
                self.cName_le.append(QLineEdit(self))
                self.cRel_lbl.append(QLabel("관계"))
                self.cRel_cb.append(QComboBox())
                self.c_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
                for i in range(len(self.c_list)):
                    self.cRel_cb[self.cnt].addItem(self.c_list[i])
                self.cCont_lbl.append(QLabel("연락처"))
                self.cCont_le.append(QLineEdit(self))
                
                for i in range(len(self.contactWidget)):
                    if i == 0:
                        self.lay.addWidget(self.contactWidget[i][self.cnt],0 + 3 * self.cnt,0)
                    elif i % 2 == 0:
                        self.lay.addWidget(self.contactWidget[i][self.cnt],int(i/2) + 3 * self.cnt,0)
                    elif i % 2 == 1:
                        self.lay.addWidget(self.contactWidget[i][self.cnt],int(i/2) + 3 * self.cnt,1)
                        if i % 3 == 2:
                            self.lay.addWidget(self.add_btn,int(i/2) + 3 * self.cnt,2)
                # 연락처 라인에디트에 입력제한 by 정현아
                for i in range(self.cnt+1):
                    self.cCont_le[i].setValidator(QIntValidator())
                    self.cCont_le[i].setMaxLength(11)
                    
                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.cnt+=1
                
            else:
                QMessageBox.information(self,"경고","2번 이상 등록하실 수 없습니다.")
        else:
            self.result_num = len(result)
            if(len(result) + self.no_del_cnt <= 2):            
                # 데이터 세팅
                if self.no_del_cnt == 0:
                    for i in range(len(result)):
                        self.cName_lbl.append(QLabel("성명"))
                        self.cName_le.append(QLineEdit(result[i][0]))
                        self.cRel_lbl.append(QLabel("관계"))
                        self.cRel_cb.append(QComboBox())
                        self.c_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
                        for j in range(len(self.c_list)):
                            self.cRel_cb[i].addItem(self.c_list[j])
                        self.cRel_cb[i].setCurrentText(result[i][1])
                        self.cCont_lbl.append(QLabel("연락처"))
                        self.cCont_le.append(QLineEdit(result[i][2]))
                        self.del_btn.append(QPushButton("삭제",self))
                        self.btnGroup.addButton(self.del_btn[i])
                        self.idx_list.append(result[i][3])
                        
                elif self.no_del_cnt != 0:
                    self.cName_lbl.append(QLabel("성명"))
                    self.cName_le.append(QLineEdit())
                    self.cRel_lbl.append(QLabel("관계"))
                    self.cRel_cb.append(QComboBox())
                    self.c_list = ['부','모','형제','배우자','자녀','조부','조모','외조부','외조모','빙부','빙모']
                    for i in range(len(self.c_list)):
                        self.cRel_cb[self.no_del_cnt + len(result) - 1].addItem(self.c_list[i])
                    self.cCont_lbl.append(QLabel("연락처"))
                    self.cCont_le.append(QLineEdit())
                    
                # 라벨 및 에디터 레이아웃에 세팅(홀수번째는 라벨, 짝수번째는 에디터로 각 레이아웃에 배치)        
                for j in range(len(result) + self.no_del_cnt):
                    for i in range(len(self.contactWidget)):
                        if i == 0:
                            self.lay.addWidget(self.contactWidget[i][j],0 + 3 * j,0)
                        elif i % 2 == 0:
                            self.lay.addWidget(self.contactWidget[i][j],int(i/2) + 3 * j,0)
                            if j < len(result):
                                    self.lay.addWidget(self.del_btn[j], int(i/2)-1 + 3 * j,2)
                        elif i % 2 == 1:
                            self.lay.addWidget(self.contactWidget[i][j],int(i/2) + 3 * j,1)
                            if i % 3 == 2:
                                self.lay.addWidget(self.add_btn,int(i/2) + 3 * j,2)
                
                for i in range(len(result) + self.no_del_cnt):
                    self.cCont_le[i].setValidator(QIntValidator())
                    self.cCont_le[i].setMaxLength(11)
                
                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.no_del_cnt+=1
                self.cnt += 1
                
            else:
                QMessageBox.information(self, "경고", "2번 이상 등록하실 수 없습니다.")
            
            
    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT NAME, REL, PHONE, IDX FROM CONTACT WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveContact(self, emp_num, cur, conn):
        # 저장된 정보를 가져옴
        result = self.setData(self.emp_num)
        # 저장된 정보가 없고 첫 라인에디트가 비어있으면 리턴
        if not result and self.cName_le[0].text() == '':
            return
        for i in range(len(self.cName_lbl)):
            contact_info = False
            cName = self.cName_le[i].text()
            cRel = self.cRel_cb[i].currentText()
            cCont = self.cCont_le[i].text()
            # 저장된 데이터가 있으면 UPDATE, 없으면 INSERT
            if i < len(self.idx_list):
                idx = self.idx_list[i]
                query = "UPDATE CONTACT SET NAME = %s, REL = %s, PHONE = %s WHERE EMP_NUM = %s AND IDX = %s;"
                cur.execute(query, (cName, cRel, cCont, emp_num, idx,))
            elif self.cName_le[i].text() != '':
                query = "INSERT INTO CONTACT(EMP_NUM, NAME, REL, PHONE) VALUES(%s, %s, %s, %s)"
                cur.execute(query, (emp_num, cName, cRel, cCont))
            conn.commit()
        # 삭제리스트가 있으면 삭제
        if self.del_idx:
            for idx in self.del_idx:
                query = "DELETE FROM CONTACT WHERE EMP_NUM = %s AND IDX = %s;"
                cur.execute(query, (emp_num, idx,))
                conn.commit() 
                
    def disappearContact(self,index):
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까?\n삭제 후 저장버튼을 누르면 삭제됩니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        else:
            j=0
            btn = self.btnGroup.button(index)
            # 삭제할 위젯 행 찾기
            for i in range(len(self.del_btn)):
                if btn == self.del_btn[i]:
                    j = i
            # 삭제할 위젯의  저장 
            del_item = self.idx_list.pop(j)
            self.del_idx.append(del_item)
            # j번째 행의 값을 뺀 후, 그 다음 행의 값을 해당 위치로 이동
            for i in range(len(self.cName_lbl) - 1):
                if i >= j:
                    # 현재 행을 j행으로 이동
                    self.cName_le[i].setText(self.cName_le[i + 1].text())
                    self.cRel_cb[i].setCurrentText(self.cRel_cb[i + 1].currentText())
                    self.cCont_le[i].setText(self.cCont_le[i + 1].text())
            # 위젯이 하나 남기 전까지 위젯 삭제
            if self.edit_num != 1:
                # 위젯 한줄씩 삭제
                for i in range(len(self.contactWidget)):
                    self.lay.removeWidget(self.contactWidget[i][self.edit_num-1])
                    self.contactWidget[i].pop(self.edit_num-1)
                self.lay.removeWidget(self.del_btn[self.edit_num-1])
                self.btnGroup.removeButton(self.del_btn[self.edit_num-1])
                self.del_btn.pop(self.edit_num-1)  
                self.cnt-=1
            # 위젯이 하나 남을 경우 에디터 초기화
            else : 
                self.cName_le[i].setText("")
                self.cRel_cb[i].setCurrentIndex(0)
                self.cCont_le[i].setText("")
                self.cCont_le[i].setValidator(QIntValidator())
                self.cCont_le[i].setMaxLength(11)
            self.edit_num-=1
            # 위젯이 전부 제거되기 전까지만 추가 버튼 위치 변경
            if self.edit_num != 0:
                self.lay.addWidget(self.add_btn, 2 + 3 * (len(self.cName_lbl)-1), 2)
            self.lay.setRowStretch(self.lay.rowCount(), 1)      
            # 위젯이 전부 제거 되면 다시 입력창 생성
            if self.cnt == 0:
                self.editContact()
            self.ignored_result = True        
            
    
class SchoolTab(QWidget):
    def __init__(self, emp_num, type):
        super(SchoolTab, self).__init__()
        self.cnt = 0
        self.no_del_cnt = 0
        self.result_num = 0
        self.edit_num = 0
        self.emp_num = emp_num
        self.type = type
        self.initUI()

    def initUI(self):
        self.school = QScrollArea()
        self.cnt = 0
        self.schwidget = QWidget()
        self.school.setWidget(self.schwidget)
        self.lay = QGridLayout(self.schwidget)
        self.school.setWidgetResizable(True)

        self.scheadmit_lbl = []
        self.scheadmit_de = []
        self.schgrad_lbl = []
        self.schgrad_de = []
        self.schname_lbl = []
        self.schname_le = []
        self.schloc_lbl = []
        self.schloc_le = []
        self.schmajor_lbl = []
        self.schmajor_le = []
        self.schsubmajor_lbl = []
        self.schsubmajor_le = []
        self.comment_lbl = []
        self.comment_le = []
        self.schWidget = [self.scheadmit_lbl, self.scheadmit_de, self.schgrad_lbl, self.schgrad_de, self.schname_lbl, self.schname_le, self.schloc_lbl , self.schloc_le ,
                          self.schmajor_lbl , self.schmajor_le , self.schsubmajor_lbl , self.schsubmajor_le , self.comment_lbl , self.comment_le ]
        self.ignored_result = False
        if self.type == 'info':
            self.addSchoolInfo()
        else:    
            self.add_btn = QPushButton("추가")
            self.btnGroup = QButtonGroup(self)
            self.del_btn = []
            self.idx_list = []
            self.editSchool()
            self.cnt = self.result_num
            self.edit_num = self.result_num
            self.del_idx = []
            self.add_btn.clicked.connect(self.editSchool)
            self.btnGroup.buttonClicked[int].connect(self.disappearSchool)

    def addSchoolInfo(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.scheadmit_lbl.append(QLabel("입학일:"))
            self.scheadmit_de.append(QLabel(str(result[i][0])))
            self.schgrad_lbl.append(QLabel("졸업일:"))
            self.schgrad_de.append(QLabel(str(result[i][1])))
            self.schname_lbl.append(QLabel("학교명:"))
            self.schname_le.append(QLabel(result[i][2]))
            self.schloc_lbl.append(QLabel("소재지:"))
            self.schloc_le.append(QLabel(result[i][3]))
            self.schmajor_lbl.append(QLabel("전공:"))
            self.schmajor_le.append(QLabel(result[i][4]))
            self.schsubmajor_lbl.append(QLabel("복수전공:"))
            self.schsubmajor_le.append(QLabel(result[i][5]))
            self.comment_lbl.append(QLabel("특기사항:"))
            self.comment_le.append(QLabel(result[i][6]))

        for j in range(self.cnt):
            for i in range(len(self.schWidget)):
                if i % 2 == 0:
                    self.lay.addWidget(self.schWidget[i][j], int(i / 2) + 7 * j, 0)
                elif i % 2 == 1:
                    self.lay.addWidget(self.schWidget[i][j], int(i / 2) + 7 * j, 1)

        self.lay.setRowStretch(self.lay.rowCount(), 1)
        rightmost_column_index = len(self.schWidget) - 1
        self.lay.setColumnStretch(rightmost_column_index, 1)
 
    def editSchool(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result or self.ignored_result:
            self.cnt = len(self.scheadmit_de)
            if self.cnt <= 3:
                self.scheadmit_lbl.append(QLabel("입학일"))
                self.scheadmit_de.append(QDateEdit(self))
                self.schgrad_lbl.append(QLabel("졸업일"))
                self.schgrad_de.append(QDateEdit(self))
                self.schname_lbl.append(QLabel("학교명"))
                self.schname_le.append(QLineEdit(self))
                self.schloc_lbl.append(QLabel("소재지"))
                self.schloc_le.append(QLineEdit(self))
                self.schmajor_lbl.append(QLabel("전공"))
                self.schmajor_le.append(QLineEdit(self))
                self.schsubmajor_lbl.append(QLabel("복수전공"))
                self.schsubmajor_le.append(QLineEdit(self))
                self.comment_lbl.append(QLabel("특기사항"))
                self.comment_le.append(QLineEdit(self))

                for i in range(len(self.schWidget)):
                    if i == 0:
                        self.lay.addWidget(self.schWidget[i][self.cnt], 0 + 7 * self.cnt, 0)
                    elif i % 2 == 0:
                        self.lay.addWidget(self.schWidget[i][self.cnt], int(i / 2) + 7 * self.cnt, 0)
                    elif i % 2 == 1:
                        self.lay.addWidget(self.schWidget[i][self.cnt], int(i / 2) + 7 * self.cnt, 1)
                        if i % 7 == 6:
                            self.lay.addWidget(self.add_btn, int(i / 2) + 7 * self.cnt, 2)

                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.cnt += 1

            else:
                QMessageBox.information(self, "경고", "4번 이상 등록하실 수 없습니다.")
        else:
            self.result_num = len(result)
            if len(result) + self.no_del_cnt <= 4:
                # 데이터 세팅
                if self.no_del_cnt == 0:
                    for i in range(len(result)):
                        self.scheadmit_lbl.append(QLabel("입학일:"))
                        self.scheadmit_de.append(QDateEdit(QDate.fromString(result[i][0].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.schgrad_lbl.append(QLabel("졸업일:"))
                        self.schgrad_de.append(QDateEdit(QDate.fromString(result[i][1].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.schname_lbl.append(QLabel("학교명:"))
                        self.schname_le.append(QLineEdit(result[i][2]))
                        self.schloc_lbl.append(QLabel("소재지:"))
                        self.schloc_le.append(QLineEdit(result[i][3]))
                        self.schmajor_lbl.append(QLabel("전공:"))
                        self.schmajor_le.append(QLineEdit(result[i][4]))
                        self.schsubmajor_lbl.append(QLabel("복수전공:"))
                        self.schsubmajor_le.append(QLineEdit(result[i][5]))
                        self.comment_lbl.append(QLabel("특기사항:"))
                        self.comment_le.append(QLineEdit(result[i][6]))
                        self.del_btn.append(QPushButton("삭제",self))
                        self.btnGroup.addButton(self.del_btn[i])
                        self.idx_list.append(result[i][7])

                elif self.no_del_cnt != 0:
                    self.scheadmit_lbl.append(QLabel("입학일"))
                    self.scheadmit_de.append(QDateEdit(self))
                    self.schgrad_lbl.append(QLabel("졸업일"))
                    self.schgrad_de.append(QDateEdit(self))
                    self.schname_lbl.append(QLabel("학교명"))
                    self.schname_le.append(QLineEdit())
                    self.schloc_lbl.append(QLabel("소재지"))
                    self.schloc_le.append(QLineEdit())
                    self.schmajor_lbl.append(QLabel("전공"))
                    self.schmajor_le.append(QLineEdit())
                    self.schsubmajor_lbl.append(QLabel("복수전공"))
                    self.schsubmajor_le.append(QLineEdit())
                    self.comment_lbl.append(QLabel("특기사항"))
                    self.comment_le.append(QLineEdit())

                for j in range(len(result) + self.no_del_cnt):
                    for i in range(len(self.schWidget)):
                        if i == 0:
                            self.lay.addWidget(self.schWidget[i][j], 0 + 7 * j, 0)
                        elif i % 2 == 0:
                            self.lay.addWidget(self.schWidget[i][j], int(i / 2) + 7 * j, 0)
                            if i % 7 == 5:
                                if j < len(result):
                                    self.lay.addWidget(self.del_btn[j], int(i / 2) + 7 * j -1,2)
                        elif i % 2 == 1:
                            self.lay.addWidget(self.schWidget[i][j], int(i / 2) + 7 * j, 1)
                            if i % 7 == 6:
                                self.lay.addWidget(self.add_btn, int(i / 2) + 7 * j, 2)

                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.no_del_cnt+=1
                self.cnt += 1

            else:
                QMessageBox.information(self, "경고", "4번 이상 등록하실 수 없습니다.")    

    
    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT DATE_ADMITION, DATE_GRADUATE, NAME_SCHOOL, LOCATION, MAJOR, SUB_MAJOR, COMMENT, IDX FROM SCHOOL_EDUCATION WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    # 231218 변경된 데이터 저장, 기존에 등록된 정보가 있을 경우 UPDATE, 없으면 INSERT
    def saveSchool(self, emp_num, cur, conn):
        result = self.setData(emp_num)
        # 저장된 정보가 없고 첫 라인에디트가 비어있으면 리턴
        if not result and self.schname_le[0].text() == '':
            return
        for i in range(len(self.scheadmit_lbl)):
            sAdmit = self.scheadmit_de[i].date().toString("yyyy-MM-dd")
            sGrad = self.schgrad_de[i].date().toString("yyyy-MM-dd")
            sName = self.schname_le[i].text()
            sLoc = self.schloc_le[i].text()
            sMajor = self.schmajor_le[i].text()
            sSubMajor = self.schsubmajor_le[i].text()
            sComment = self.comment_le[i].text()
            
            # 저장된 데이터가 있으면 UPDATE, 없으면 INSERT
            if i < len(self.idx_list):
                idx = self.idx_list[i]
                query = "UPDATE SCHOOL_EDUCATION SET DATE_ADMITION = %s, DATE_GRADUATE = %s, NAME_SCHOOL = %s, LOCATION = %s, MAJOR = %s, SUB_MAJOR = %s, COMMENT = %s WHERE EMP_NUM = %s AND IDX = %s;"
                cur.execute(query, (sAdmit, sGrad, sName, sLoc, sMajor, sSubMajor, sComment, emp_num, idx,))
            elif self.schname_le[i].text() != '':
                query = "INSERT INTO SCHOOL_EDUCATION(EMP_NUM, DATE_ADMITION, DATE_GRADUATE, NAME_SCHOOL, LOCATION, MAJOR, SUB_MAJOR, COMMENT) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(query, (emp_num, sAdmit, sGrad, sName, sLoc, sMajor, sSubMajor, sComment))
            conn.commit()
            
        if self.del_idx:
            for idx in self.del_idx:
                query = "DELETE FROM SCHOOL_EDUCATION WHERE EMP_NUM = %s AND IDX = %s;"
                cur.execute(query, (emp_num, idx,))
                conn.commit() 

    # 231217 UI에서 위젯 삭제 by 정현아    
    def disappearSchool(self,index):
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까?\n삭제 후 저장버튼을 누르면 삭제됩니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        else:
            j=0
            btn = self.btnGroup.button(index)
            # 삭제할 위젯 행 찾기
            for i in range(len(self.del_btn)):
                if btn == self.del_btn[i]:
                    j = i
            # 삭제할 위젯의 데이터 저장 
            del_item = self.idx_list.pop(j) 
            self.del_idx.append(del_item)
            # j번째 행의 값을 뺀 후, 그 다음 행의 값을 해당 위치로 이동
            for i in range(len(self.scheadmit_lbl) - 1):
                if i >= j:
                    # 현재 행을 j행으로 이동
                    self.scheadmit_de[i].setDate(self.scheadmit_de[i + 1].date())
                    self.schgrad_de[i].setDate(self.schgrad_de[i + 1].date())
                    self.schname_le[i].setText(self.schname_le[i + 1].text())
                    self.schloc_le[i].setText(self.schloc_le[i + 1].text())
                    self.schmajor_le[i].setText(self.schmajor_le[i + 1].text())
                    self.schsubmajor_le[i].setText(self.schsubmajor_le[i + 1].text())
                    self.comment_le[i].setText(self.comment_le[i + 1].text())
            # 위젯이 하나 남기 전까지 위젯 삭제
            if self.edit_num != 1:
                # 위젯 한줄씩 삭제
                for i in range(len(self.schWidget)):
                    self.lay.removeWidget(self.schWidget[i][self.edit_num-1])
                    self.schWidget[i].pop(self.edit_num-1)
                self.lay.removeWidget(self.del_btn[self.edit_num-1])
                self.btnGroup.removeButton(self.del_btn[self.edit_num-1])
                self.del_btn.pop(self.edit_num-1)  
                self.cnt-=1
            # 위젯이 하나 남을 경우 에디터 초기화
            else : 
                self.scheadmit_de[i].setDate(QDate(2000, 1, 1))
                self.schgrad_de[i].setDate(QDate(2000, 1, 1))
                self.schname_le[i].setText("")
                self.schloc_le[i].setText("")
                self.schmajor_le[i].setText("")
                self.schsubmajor_le[i].setText("")
                self.comment_le[i].setText("")
            self.edit_num-=1
            # 위젯이 전부 제거되기 전까지만 추가 버튼 위치 변경
            if self.edit_num != 0:
                self.lay.addWidget(self.add_btn, 6 + 7 * (len(self.scheadmit_lbl)-1), 2)
            self.lay.setRowStretch(self.lay.rowCount(), 1)      
            # 위젯이 전부 제거 되면 다시 입력창 생성
            if self.cnt == 0:
                self.editSchool()
            self.ignored_result = True                   
    
    
class CertificationTab(QWidget):
    def __init__(self, emp_num, type):
        super(CertificationTab, self).__init__()
        self.cnt = 0
        self.no_del_cnt = 0
        self.result_num = 0
        self.edit_num = 0
        self.type = type
        self.emp_num = emp_num
        self.initUI()

    def initUI(self):
        self.certificate = QScrollArea()
        self.cnt = 0
        self.certwidget = QWidget()
        self.certificate.setWidget(self.certwidget)
        self.lay = QGridLayout(self.certwidget)
        self.certificate.setWidgetResizable(True)

        self.certName_lbl = []
        self.certName_le = []
        self.certDate_lbl = []
        self.certDate_de = []
        self.certwidget = [self.certName_lbl, self.certName_le, self.certDate_lbl, self.certDate_de]
        self.ignored_result = False
        if self.type == 'info':
            self.addCertification()
        else:
            self.add_btn = QPushButton("추가")   
            self.btnGroup = QButtonGroup(self)
            self.del_btn = []
            self.idx_list = []
            self.editCertification()
            self.cnt = self.result_num
            self.edit_num = self.result_num
            self.del_idx = []
            self.add_btn.clicked.connect(self.editCertification)
            self.btnGroup.buttonClicked[int].connect(self.disappearCertification)


    def addCertification(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        for i in range(self.cnt):
            self.certName_lbl.append(QLabel("자격증명:"))
            self.certName_le.append(QLabel(result[i][0]))

            self.certDate_lbl.append(QLabel("취득일:"))
            self.certDate_de.append(QLabel(str(result[i][1])))

        for j in range(self.cnt):
            for i in range(len(self.certwidget)):
                if i % 2 == 0:
                    self.lay.addWidget(self.certwidget[i][j], int(i/2) + 2 * j, 0)
                elif i % 2 == 1:
                    self.lay.addWidget(self.certwidget[i][j], int(i/2) + 2 * j, 1)

        self.lay.setRowStretch(self.lay.rowCount(), 1)
        rightmost_column_index = len(self.certwidget) - 1
        self.lay.setColumnStretch(rightmost_column_index, 1)
        
    def editCertification(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        if not result or self.ignored_result:
            self.cnt = len(self.certName_le)
            if(self.cnt<=9):
                self.certName_lbl.append(QLabel("자격증명"))
                self.certName_le.append(QLineEdit(self))
                self.certDate_lbl.append(QLabel("취득일"))
                self.certDate_de.append(QDateEdit(self))
                
                for i in range(len(self.certwidget)):
                    if i == 0:
                        self.lay.addWidget(self.certwidget[i][self.cnt],0 + 2 * self.cnt,0)
                    elif i % 2 == 0:
                        self.lay.addWidget(self.certwidget[i][self.cnt],int(i/2) + 2 * self.cnt,0)
                    elif i % 2 == 1:
                        self.lay.addWidget(self.certwidget[i][self.cnt],int(i/2) + 2 * self.cnt,1)
                        self.lay.addWidget(self.add_btn,int(i/2) + 2 * self.cnt,2)
                
                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.cnt+=1
            else:
                QMessageBox.information(self, "경고", "10번 이상 등록하실 수 없습니다.")
        else:
            self.result_num = len(result)
            if len(result) + self.no_del_cnt <= 9:
                # 데이터 세팅
                if self.no_del_cnt == 0:
                    for i in range(len(result)):
                        self.certName_lbl.append(QLabel("자격증명"))
                        self.certName_le.append(QLineEdit(result[i][0]))
                        self.certDate_lbl.append(QLabel("취득일"))
                        self.certDate_de.append(QDateEdit(QDate.fromString(result[i][1].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.del_btn.append(QPushButton("삭제",self))
                        self.btnGroup.addButton(self.del_btn[i])
                        self.idx_list.append(result[i][2])
                
                elif self.no_del_cnt != 0:
                    self.certName_lbl.append(QLabel("자격증명"))
                    self.certName_le.append(QLineEdit())
                    self.certDate_lbl.append(QLabel("취득일"))
                    self.certDate_de.append(QDateEdit())

                for j in range(len(result) + self.no_del_cnt):
                    for i in range(len(self.certwidget)):
                        if i == 0:
                            self.lay.addWidget(self.certwidget[i][j], 0 + 2 * j, 0)
                        elif i % 2 == 0:
                            self.lay.addWidget(self.certwidget[i][j], int(i / 2) + 2 * j, 0)
                            if j < len(result):
                                self.lay.addWidget(self.del_btn[j], int(i/2)-1 + 2 * j,2)
                        elif i % 2 == 1:
                            self.lay.addWidget(self.certwidget[i][j], int(i / 2) + 2 * j, 1)
                            self.lay.addWidget(self.add_btn, int(i / 2) + 2 * j, 2)

                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.no_del_cnt+=1
                self.cnt += 1
            else:
                QMessageBox.information(self, "경고", "10번 이상 등록하실 수 없습니다.")

    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT NAME_LICENSE, DATE_ACQUI, IDX FROM CERTIFICATE WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveCertification(self, emp_num, cur, conn):
        # 저장된 정보를 가져옴
        result = self.setData(self.emp_num)
        # 저장된 정보가 없고 첫 라인에디트가 비어있으면 리턴
        if not result and self.certName_le[0].text() == '':
            return
        for i in range(len(self.certName_lbl)):
            certName = self.certName_le[i].text()
            certDate = self.certDate_de[i].date().toString("yyyy-MM-dd")
            # 저장된 데이터가 있으면 UPDATE, 없으면 INSERT
            if i < len(self.idx_list):
                idx = self.idx_list[i]
                query = "UPDATE CERTIFICATE SET NAME_LICENSE = %s, DATE_ACQUI = %s WHERE EMP_NUM = %s AND IDX = %s;"
                cur.execute(query, (certName, certDate, emp_num, idx,))
                conn.commit()
            else:
                query = "INSERT INTO CERTIFICATE(EMP_NUM, NAME_LICENSE, DATE_ACQUI) VALUES(%s, %s, %s)"
                cur.execute(query, (emp_num, certName, certDate))
            conn.commit()
        if self.del_idx:
            for idx in self.del_idx:
                query = "DELETE FROM CERTIFICATE WHERE EMP_NUM = %s AND IDX = %s;"
                cur.execute(query, (emp_num, idx,))
                conn.commit()         

    def disappearCertification(self,index):
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까?\n삭제 후 저장버튼을 누르면 삭제됩니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        else:
            j=0
            btn = self.btnGroup.button(index)
            # 삭제할 위젯 행 찾기
            for i in range(len(self.del_btn)):
                if btn == self.del_btn[i]:
                    j = i
            # 삭제할 위젯의 데이터 저장 
            del_item = self.idx_list.pop(j)
            self.del_idx.append(del_item)
            # j번째 행의 값을 뺀 후, 그 다음 행의 값을 해당 위치로 이동
            for i in range(len(self.certName_lbl) - 1):
                if i >= j:
                    # 현재 행을 j행으로 이동
                    self.certName_le[i].setText(self.certName_le[i + 1].text())
                    self.certDate_de[i].setDate(self.certDate_de[i + 1].date())
            # 위젯이 하나 남기 전까지 위젯 삭제
            if self.edit_num != 1:
                # 위젯 한줄씩 삭제
                for i in range(len(self.certwidget)):
                    self.lay.removeWidget(self.certwidget[i][self.edit_num-1])
                    self.certwidget[i].pop(self.edit_num-1)
                self.lay.removeWidget(self.del_btn[self.edit_num-1])
                self.btnGroup.removeButton(self.del_btn[self.edit_num-1])
                self.del_btn.pop(self.edit_num-1)  
                self.cnt-=1
            # 위젯이 하나 남을 경우 에디터 초기화
            else : 
                self.certName_le[i].setText("")
                self.certDate_de[i].setDate(QDate(2000, 1, 1))
            self.edit_num-=1
            # 위젯이 전부 제거되기 전까지만 추가 버튼 위치 변경
            if self.edit_num != 0:
                self.lay.addWidget(self.add_btn, 1 + 2 * (len(self.certName_lbl)-1), 2)
            self.lay.setRowStretch(self.lay.rowCount(), 1)      
            # 위젯이 전부 제거 되면 다시 입력창 생성
            if self.cnt == 0:
                self.editContact()
            self.ignored_result = True    

class CareerTab(QWidget):
    def __init__(self, emp_num, type):
        super(CareerTab, self).__init__()
        self.cnt = 0
        self.no_del_cnt = 0
        self.result_num = 0
        self.edit_num = 0
        self.emp_num = emp_num
        self.type = type
        self.initUI()

    def initUI(self):
        self.career = QScrollArea()
        self.cnt = 0
        self.widget = QWidget()
        self.career.setWidget(self.widget)
        self.lay = QGridLayout(self.widget)
        self.career.setWidgetResizable(True)

        self.company_lbl = []
        self.company_le = []
        self.dept_lbl = []
        self.dept_le = []
        self.datejoin_lbl = []
        self.datejoin_de = []
        self.dateleave_lbl = []
        self.dateleave_de = []
        self.finalrank_lbl = []
        self.finalrank_le = []
        self.workinfo_lbl = []
        self.workinfo_le = []
        self.widget = [self.company_lbl, self.company_le, self.dept_lbl, self.dept_le, self.datejoin_lbl, self.datejoin_de, self.dateleave_lbl , self.dateleave_de ,
                          self.finalrank_lbl , self.finalrank_le , self.workinfo_lbl , self.workinfo_le ]
        self.ignored_result = False
        if self.type == 'info':
            self.addCareerInfo()
        else: 
            self.add_btn = QPushButton("추가")
            self.btnGroup = QButtonGroup(self)
            self.del_btn = []
            self.editCareerInfo()
            self.cnt = self.result_num
            self.edit_num = self.result_num
            self.del_name = []
            self.del_dept = []
            self.add_btn.clicked.connect(self.editCareerInfo)
            self.btnGroup.buttonClicked[int].connect(self.disappearCareer)

    def addCareerInfo(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.company_lbl.append(QLabel("근무회사:"))
            self.company_le.append(QLabel(result[i][0]))
            self.dept_lbl.append(QLabel("근무부서:"))
            self.dept_le.append(QLabel(result[i][1]))
            self.datejoin_lbl.append(QLabel("입사일:"))
            self.datejoin_de.append(QLabel(str(result[i][2])))
            self.dateleave_lbl.append(QLabel("퇴사일:"))
            self.dateleave_de.append(QLabel(str(result[i][3])))
            self.finalrank_lbl.append(QLabel("최종 직급:"))
            self.finalrank_le.append(QLabel(result[i][4]))
            self.workinfo_lbl.append(QLabel("근무 내용:"))
            self.workinfo_le.append(QLabel(result[i][5]))

        for j in range(self.cnt):
            for i in range(len(self.widget)):
                if i % 2 == 0:
                    self.lay.addWidget(self.widget[i][j], int(i/2) + 6 * j, 0)
                elif i % 2 == 1:
                    self.lay.addWidget(self.widget[i][j], int(i/2) + 6 * j, 1)

        self.lay.setRowStretch(self.lay.rowCount(), 1)
        rightmost_column_index = len(self.widget) - 1
        self.lay.setColumnStretch(rightmost_column_index, 1)
        
    def editCareerInfo(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result or self.ignored_result:
            self.cnt = len(self.company_le)
            if(self.cnt<=9):
                self.company_lbl.append(QLabel("근무회사"))
                self.company_le.append(QLineEdit(self))
                self.dept_lbl.append(QLabel("근무부서"))
                self.dept_le.append(QLineEdit(self))
                self.datejoin_lbl.append(QLabel("입사일"))
                self.datejoin_de.append(QDateEdit(self))
                self.dateleave_lbl.append(QLabel("퇴사일"))
                self.dateleave_de.append(QDateEdit(self))
                self.finalrank_lbl.append(QLabel("최종직급"))
                self.finalrank_le.append(QLineEdit(self))
                self.workinfo_lbl.append(QLabel("업무내용"))
                self.workinfo_le.append(QLineEdit(self))

                for i in range(len(self.widget)):
                    if i == 0:
                        self.lay.addWidget(self.widget[i][self.cnt],0 + 6 * self.cnt,0)
                    elif i % 2 == 0:
                        self.lay.addWidget(self.widget[i][self.cnt],int(i/2) + 6 * self.cnt,0)
                    elif i % 2 == 1:
                        self.lay.addWidget(self.widget[i][self.cnt],int(i/2) + 6 * self.cnt,1)
                        if i % 6 == 5:
                            self.lay.addWidget(self.add_btn,int(i/2) + 6 * self.cnt,2)
                
                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.cnt+=1     
            else:
                QMessageBox.information(self, "경고", "10번 이상 등록하실 수 없습니다.")
                
        else:
            self.result_num = len(result)
            if len(result) + self.no_del_cnt <= 9:
                # 데이터 세팅
                if self.no_del_cnt == 0:
                    for i in range(len(result)):
                        self.company_lbl.append(QLabel("근무회사:"))
                        self.company_le.append(QLineEdit(result[i][0]))
                        self.dept_lbl.append(QLabel("근무부서:"))
                        self.dept_le.append(QLineEdit(result[i][1]))
                        self.datejoin_lbl.append(QLabel("입사일:"))
                        self.datejoin_de.append(QDateEdit(QDate.fromString(result[i][2].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.dateleave_lbl.append(QLabel("퇴사일:"))
                        self.dateleave_de.append(QDateEdit(QDate.fromString(result[i][3].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.finalrank_lbl.append(QLabel("최종 직급:"))
                        self.finalrank_le.append(QLineEdit(result[i][4]))
                        self.workinfo_lbl.append(QLabel("근무 내용:"))
                        self.workinfo_le.append(QLineEdit(result[i][5]))
                        self.del_btn.append(QPushButton("삭제",self))
                        self.btnGroup.addButton(self.del_btn[i])

                elif self.no_del_cnt != 0:
                    self.company_lbl.append(QLabel("근무회사"))
                    self.company_le.append(QLineEdit())
                    self.dept_lbl.append(QLabel("근무부서"))
                    self.dept_le.append(QLineEdit())
                    self.datejoin_lbl.append(QLabel("입사일"))
                    self.datejoin_de.append(QDateEdit())
                    self.dateleave_lbl.append(QLabel("퇴사일"))
                    self.dateleave_de.append(QDateEdit())
                    self.finalrank_lbl.append(QLabel("최종직급"))
                    self.finalrank_le.append(QLineEdit())
                    self.workinfo_lbl.append(QLabel("업무내용"))
                    self.workinfo_le.append(QLineEdit())

                for j in range(len(result)+self.no_del_cnt):
                    for i in range(len(self.widget)):
                        if i == 0:
                            self.lay.addWidget(self.widget[i][j], 0 + 6 * j, 0)
                        elif i % 2 == 0:
                            self.lay.addWidget(self.widget[i][j], int(i / 2) + 6 * j, 0)
                            if i % 6 == 4:
                                if j < len(result):
                                    self.lay.addWidget(self.del_btn[j], int(i / 2) + 6 * j -1,2)
                        elif i % 2 == 1:
                            self.lay.addWidget(self.widget[i][j], int(i / 2) + 6 * j, 1)
                            if i % 6 == 5:
                                self.lay.addWidget(self.add_btn, int(i / 2) + 6 * j, 2)

                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.no_del_cnt+=1
                self.cnt += 1
            else:
                QMessageBox.information(self, "경고", "10번 이상 등록하실 수 없습니다.")
                
    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT COMPANY, DEPARTMENT, DATE_JOIN, DATE_LEAVE, FINAL_RANK, WORK_INFO FROM CAREER WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveCareer(self, emp_num, cur, conn):
        result = self.setData(emp_num)
        # 저장된 정보가 없고 첫 라인에디트가 비어있으면 리턴
        if not result and self.company_le[0].text() == '':
            return
        for i in range(len(self.company_lbl)):
            career_info = False
            company = self.company_le[i].text()
            dept = self.dept_le[i].text()
            datejoin = self.datejoin_de[i].date().toString("yyyy-MM-dd")
            dateleave = self.dateleave_de[i].date().toString("yyyy-MM-dd")
            workdays = self.datejoin_de[i].date().daysTo(self.dateleave_de[i].date())
            years, months = divmod(workdays, 365)
            months = months/30.44/12
            workperiod = round(years + months, 1)
            finalrank = self.finalrank_le[i].text()
            workinfo = self.workinfo_le[i].text()
            
            # 저장된 데이터가 있으면 UPDATE, 없으면 INSERT
            query = "SELECT * FROM CAREER WHERE EMP_NUM = %s AND COMPANY = %s AND DEPARTMENT = %s"
            cur.execute(query, (self.emp_num, company, dept,))
            career_info = cur.fetchone()
            if career_info:
                query = """
                    UPDATE CAREER
                    SET COMPANY = %s, DEPARTMENT = %s, DATE_JOIN = %s, DATE_LEAVE = %s, WORK_PERIOD = %s, FINAL_RANK = %s, WORK_INFO = %s
                    WHERE EMP_NUM = %s AND COMPANY = %s  AND DEPARTMENT = %s;
                """
                values = (company, dept, datejoin, dateleave, workperiod, finalrank, workinfo, emp_num, company, dept,)
                cur.execute(query, values)
            elif self.company_le[i].text() != '':
                query = """
                    INSERT INTO CAREER (EMP_NUM, COMPANY, DEPARTMENT, DATE_JOIN, DATE_LEAVE, WORK_PERIOD, FINAL_RANK, WORK_INFO)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                values = (emp_num, company, dept, datejoin, dateleave, workperiod, finalrank, workinfo)
                cur.execute(query, values)
            conn.commit()

            if self.del_name:
                for i in range(len(self.del_name)):
                    query = "DELETE FROM CAREER WHERE EMP_NUM = %s AND COMPANY = %s AND DEPARTMENT = %s;"
                    cur.execute(query, (emp_num, self.del_name[i],self.del_dept[i],))
                    conn.commit() 

    def disappearCareer(self,index):
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까?\n삭제 후 저장버튼을 누르면 삭제됩니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        else:
            j=0
            btn = self.btnGroup.button(index)
            # 삭제할 위젯 행 찾기
            for i in range(len(self.del_btn)):
                if btn == self.del_btn[i]:
                    j = i
            # 삭제할 위젯의 데이터 저장 
            self.del_name.append(self.company_le[j].text())
            self.del_dept.append(self.dept_le[j].text())
            # j번째 행의 값을 뺀 후, 그 다음 행의 값을 해당 위치로 이동
            for i in range(len(self.company_lbl) - 1):
                if i >= j:
                    # 현재 행을 j행으로 이동
                    self.company_le[i].setDate(self.company_le[i + 1].text())
                    self.dept_le[i].setText(self.dept_le[i + 1].text())
                    self.datejoin_de[i].setText(self.datejoin_de[i + 1].date())
                    self.dateleave_de[i].setDate(self.dateleave_de[i + 1].date())
                    self.finalrank_le[i].setDate(self.finalrank_le[i + 1].text())
                    self.workinfo_le[i].setText(self.workinfo_le[i + 1].text())
            # 위젯이 하나 남기 전까지 위젯 삭제
            if self.edit_num != 1:
                # 위젯 한줄씩 삭제
                for i in range(len(self.widget)):
                    self.lay.removeWidget(self.widget[i][self.edit_num-1])
                    self.widget[i].pop(self.edit_num-1)
                self.lay.removeWidget(self.del_btn[self.edit_num-1])
                self.btnGroup.removeButton(self.del_btn[self.edit_num-1])
                self.del_btn.pop(self.edit_num-1)  
                self.cnt-=1
            # 위젯이 하나 남을 경우 에디터 초기화
            else : 
                self.company_le[i].setText("")
                self.dept_le[i].setText("")
                self.datejoin_de[i].setDate(QDate(2000, 1, 1))
                self.dateleave_de[i].setDate(QDate(2000, 1, 1))
                self.finalrank_le[i].setText("")
                self.workinfo_le[i].setText("")
            self.edit_num-=1
            # 위젯이 전부 제거되기 전까지만 추가 버튼 위치 변경
            if self.edit_num != 0:
                self.lay.addWidget(self.add_btn, 6 + 7 * (len(self.company_lbl)-1), 2)
            self.lay.setRowStretch(self.lay.rowCount(), 1)      
            # 위젯이 전부 제거 되면 다시 입력창 생성
            if self.cnt == 0:
                self.editCareerInfo()
            self.ignored_result = True  
    
class TechnicalTab(QWidget):
    def __init__(self, emp_num, type):
        super(TechnicalTab, self).__init__()
        self.cnt = 0
        self.no_del_cnt = 0
        self.result_num = 0
        self.edit_num = 0
        self.emp_num = emp_num
        self.type = type
        self.initUI()

    def initUI(self):
        self.technical = QScrollArea()
        self.cnt = 0
        self.widget = QWidget()
        self.technical.setWidget(self.widget)
        self.lay = QGridLayout(self.widget)
        self.technical.setWidgetResizable(True)

        self.techDet_lbl = []
        self.techDet_le = []
        self.pro_lbl = []
        self.pro_cb = []
        self.note_lbl = []
        self.note_le = []
        self.widget = [self.techDet_lbl, self.techDet_le, self.pro_lbl, self.pro_cb, self.note_lbl, self.note_le]
        self.ignored_result = False
        if self.type == 'info':
            self.addTechMember()
        else:
            self.add_btn = QPushButton("추가")
            self.btnGroup = QButtonGroup(self)
            self.del_btn = []
            self.editTechMember()
            self.cnt = self.result_num
            self.edit_num = self.result_num
            self.del_name = []
            self.add_btn.clicked.connect(self.editTechMember)
            self.btnGroup.buttonClicked[int].connect(self.disappearTech)

    def addTechMember(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.techDet_lbl.append(QLabel("기술사항:"))
            self.techDet_le.append(QLabel(result[i][0]))
            self.pro_lbl.append(QLabel("숙련도:"))
            self.pro_cb.append(QLabel(result[i][1]))
            self.note_lbl.append(QLabel("비고:"))
            self.note_le.append(QLabel(result[i][2]))

        for j in range(self.cnt):
            for i in range(len(self.widget)):
                if i % 2 == 0:
                    self.lay.addWidget(self.widget[i][j], int(i/2) + 3 * j, 0)
                elif i % 2 == 1:
                    self.lay.addWidget(self.widget[i][j], int(i/2) + 3 * j, 1)

        self.lay.setRowStretch(self.lay.rowCount(), 1)
        rightmost_column_index = len(self.widget) - 1
        self.lay.setColumnStretch(rightmost_column_index, 1)
        
    def editTechMember(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result or self.ignored_result:
            self.cnt = len(self.techDet_le)
            if(self.cnt<=9):
                self.techDet_lbl.append(QLabel("기술사항"))
                self.techDet_le.append(QLineEdit(self))
                self.pro_lbl.append(QLabel("숙련도"))
                self.pro_cb.append(QComboBox())
                self.pro_cb[self.cnt].addItem('상')
                self.pro_cb[self.cnt].addItem('중')
                self.pro_cb[self.cnt].addItem('하')
                self.note_lbl.append(QLabel("비고"))
                self.note_le.append(QLineEdit(self))
                
                for i in range(len(self.widget)):
                    if i == 0:
                        self.lay.addWidget(self.widget[i][self.cnt],0 + 3 * self.cnt,0)
                    elif i % 2 == 0:
                        self.lay.addWidget(self.widget[i][self.cnt],int(i/2) + 3 * self.cnt,0)
                    elif i % 2 == 1:
                        self.lay.addWidget(self.widget[i][self.cnt],int(i/2) + 3 * self.cnt,1)
                        if i % 3 == 2:
                            self.lay.addWidget(self.add_btn,int(i/2) + 3 * self.cnt,2)
                
                self.lay.setRowStretch((self.lay.rowCount()*(4-self.cnt)),1)
                self.cnt+=1;
                
            else:
                QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")
        else : 
            self.result_num = len(result)
            if len(result) + self.no_del_cnt <= 9:
                if self.no_del_cnt == 0:
                    for i in range(len(result)):
                        self.techDet_lbl.append(QLabel("기술사항:"))
                        self.techDet_le.append(QLineEdit(result[i][0]))
                        self.pro_lbl.append(QLabel("숙련도:"))
                        self.pro_cb.append(QComboBox())
                        self.pro_cb[i].addItem('상')
                        self.pro_cb[i].addItem('중')
                        self.pro_cb[i].addItem('하')
                        self.pro_cb[i].setCurrentText(result[i][1])
                        self.note_lbl.append(QLabel("비고:"))
                        self.note_le.append(QLineEdit(result[i][2]))
                        self.del_btn.append(QPushButton("삭제",self))
                        self.btnGroup.addButton(self.del_btn[i])

                elif self.no_del_cnt != 0:
                    self.techDet_lbl.append(QLabel("기술사항"))
                    self.techDet_le.append(QLineEdit())
                    self.pro_lbl.append(QLabel("숙련도"))
                    self.pro_cb.append(QComboBox())
                    self.pro_cb[self.no_del_cnt+len(result)-1].addItem('상')
                    self.pro_cb[self.no_del_cnt+len(result)-1].addItem('중')
                    self.pro_cb[self.no_del_cnt+len(result)-1].addItem('하')
                    self.note_lbl.append(QLabel("비고"))
                    self.note_le.append(QLineEdit())

                for j in range(len(result) + self.no_del_cnt):
                    for i in range(len(self.widget)):
                        if i == 0:
                            self.lay.addWidget(self.widget[i][j], 0 + 3 * j, 0)
                        elif i % 2 == 0:
                            self.lay.addWidget(self.widget[i][j], int(i / 2) + 3 * j, 0)
                            if j < len(result):
                                    self.lay.addWidget(self.del_btn[j], int(i/2)-1 + 3 * j,2)
                        elif i % 2 == 1:
                            self.lay.addWidget(self.widget[i][j], int(i / 2) + 3 * j, 1)
                            if i % 3 == 2:
                                self.lay.addWidget(self.add_btn, int(i / 2) + 3 * j, 2)

                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.no_del_cnt+=1
                self.cnt += 1
            else:
                QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")
        

    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT TEC_DETAIL, PROFICIENCY,NOTE FROM TECHNICAL WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveTechnical(self, emp_num, cur, conn):
        result = self.setData(emp_num)
        # 저장된 정보가 없고 첫 라인에디트가 비어있으면 리턴
        if not result and self.techDet_le[0].text() == '':
            return
        for i in range(len(self.techDet_lbl)):
            tech_info = False
            techDet = self.techDet_le[i].text()
            proficiency = self.pro_cb[i].currentText()
            note = self.note_le[i].text()
            # 저장된 데이터가 있으면 UPDATE, 없으면 INSERT
            query = "SELECT * FROM TECHNICAL WHERE EMP_NUM = %s AND TEC_DETAIL = %s;"
            cur.execute(query, (self.emp_num, techDet,))
            tech_info = cur.fetchone()
            if tech_info:
                query = "UPDATE TECHNICAL SET TEC_DETAIL = %s, PROFICIENCY = %s, NOTE = %s WHERE EMP_NUM = %s AND TEC_DETAIL = %s;"
                cur.execute(query, (techDet, proficiency, note, emp_num, techDet))
            else:
                query = "INSERT INTO TECHNICAL (EMP_NUM, TEC_DETAIL, PROFICIENCY, NOTE) VALUES (%s, %s, %s, %s);"
                cur.execute(query, (emp_num, techDet, proficiency, note))
            conn.commit()
        # 삭제리스트가 있으면 삭제
        if self.del_name:
            for name in self.del_name:
                query = "DELETE FROM TECHNICAL WHERE EMP_NUM = %s AND TEC_DETAIL = %s;"
                cur.execute(query, (emp_num, name,))
                conn.commit() 

    def disappearTech(self,index):
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까?\n삭제 후 저장버튼을 누르면 삭제됩니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        else:
            j=0
            btn = self.btnGroup.button(index)
            # 삭제할 위젯 행 찾기
            for i in range(len(self.del_btn)):
                if btn == self.del_btn[i]:
                    j = i
            # 삭제할 위젯의 데이터 저장 
            self.del_name.append(self.techDet_le[j].text())
            # j번째 행의 값을 뺀 후, 그 다음 행의 값을 해당 위치로 이동
            for i in range(len(self.techDet_lbl) - 1):
                if i >= j:
                    # 현재 행을 j행으로 이동
                    self.techDet_le[i].setText(self.techDet_le[i + 1].text())
                    self.pro_cb[i].setCurrentText(self.pro_cb[i + 1].currentText())
                    self.note_le[i].setText(self.note_le[i + 1].text())
            # 위젯이 하나 남기 전까지 위젯 삭제
            if self.edit_num != 1:
                # 위젯 한줄씩 삭제
                for i in range(len(self.widget)):
                    self.lay.removeWidget(self.widget[i][self.edit_num-1])
                    self.widget[i].pop(self.edit_num-1)
                self.lay.removeWidget(self.del_btn[self.edit_num-1])
                self.btnGroup.removeButton(self.del_btn[self.edit_num-1])
                self.del_btn.pop(self.edit_num-1)  
                self.cnt-=1
            # 위젯이 하나 남을 경우 에디터 초기화
            else : 
                self.techDet_le[i].setText("")
                self.pro_cb[i].setCurrentIndex(0)
                self.note_le[i].setText("")
            self.edit_num-=1
            # 위젯이 전부 제거되기 전까지만 추가 버튼 위치 변경
            if self.edit_num != 0:
                self.lay.addWidget(self.add_btn, 2 + 3 * (len(self.techDet_lbl)-1), 2)
            self.lay.setRowStretch(self.lay.rowCount(), 1)      
            # 위젯이 전부 제거 되면 다시 입력창 생성
            if self.cnt == 0:
                self.editTechMember()
            self.ignored_result = True   
    
class RPTab(QWidget):
    def __init__(self, emp_num, type):
        super(RPTab, self).__init__()
        self.emp_num = emp_num
        self.cnt = 0
        self.no_del_cnt = 0
        self.result_num = 0
        self.edit_num = 0
        self.type = type
        self.initUI()

    def initUI(self):
        self.rp = QScrollArea()
        self.widget = QWidget()
        self.rp.setWidget(self.widget)
        self.lay = QGridLayout(self.widget)
        self.rp.setWidgetResizable(True)

        self.rpName_lbl = []
        self.rpName_le = []
        self.rpScore_lbl = []
        self.rpScore_le = []
        self.rpDate_lbl = []
        self.rpDate_de = []
        self.rpNote_lbl = []
        self.rpNote_le = []
        self.widget = [self.rpName_lbl, self.rpName_le, self.rpScore_lbl, self.rpScore_le, 
                             self.rpDate_lbl, self.rpDate_de, self.rpNote_lbl, self.rpNote_le]
        self.ignored_result = False
        if self.type == 'info':
            self.addRPMember()
        else: 
            self.add_btn = QPushButton("추가")
            self.btnGroup = QButtonGroup(self)
            self.del_btn = []
            self.editRPMember()
            self.cnt = self.result_num
            self.edit_num = self.result_num
            self.del_name = []
            self.del_date = []
            self.add_btn.clicked.connect(self.editRPMember)            
            self.btnGroup.buttonClicked[int].connect(self.disappearRP)

    def addRPMember(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.rpName_lbl.append(QLabel("상벌명:"))
            self.rpName_le.append(QLabel(result[i][0]))
            self.rpScore_lbl.append(QLabel("점수:"))
            self.rpScore_le.append(QLabel(str(result[i][1])))
            self.rpDate_lbl.append(QLabel("일자:"))
            self.rpDate_de.append(QLabel(str(result[i][2])))
            self.rpNote_lbl.append(QLabel("상벌내용:"))
            self.rpNote_le.append(QLabel(result[i][3]))

        for j in range(self.cnt):
            for i in range(len(self.widget)):
                if i % 2 == 0:
                    self.lay.addWidget(self.widget[i][j], int(i/2) + 4 * j, 0)
                elif i % 2 == 1:
                    self.lay.addWidget(self.widget[i][j], int(i/2) + 4 * j, 1)

        self.lay.setRowStretch(self.lay.rowCount(), 1)
        rightmost_column_index = len(self.widget) - 1
        self.lay.setColumnStretch(rightmost_column_index, 1)
        
    def editRPMember(self):
        # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result or self.ignored_result:
            self.cnt = len(self.rpName_le)
            if(self.cnt<=19):
                self.rpName_lbl.append(QLabel("상벌명"))
                self.rpName_le.append(QLineEdit(self))
                self.rpScore_lbl.append(QLabel("점수"))
                self.rpScore_le.append(QLineEdit(self))
                self.rpDate_lbl.append(QLabel("상벌일"))
                self.rpDate_de.append(QDateEdit(self))
                self.rpNote_lbl.append(QLabel("상벌내용"))
                self.rpNote_le.append(QLineEdit(self))
                
                for i in range(len(self.widget)):
                    if i == 0:
                        self.lay.addWidget(self.widget[i][self.cnt],0 + 4 * self.cnt,0)
                    elif i % 2 == 0:
                        self.lay.addWidget(self.widget[i][self.cnt],int(i/2) + 4 * self.cnt,0)
                    elif i % 2 == 1:
                        self.lay.addWidget(self.widget[i][self.cnt],int(i/2) + 4 * self.cnt,1)
                        if i % 4 == 3:
                            self.lay.addWidget(self.add_btn,int(i/2) + 4 * self.cnt,2)
                            
                for i in range(self.cnt+1):
                    self.rpScore_le[i].setValidator(QIntValidator())
                
                self.lay.setRowStretch((self.lay.rowCount()*(4-self.cnt)),1)
                self.cnt+=1;
                
            else:
                QMessageBox.information(self,"경고","20번 이상 등록하실 수 없습니다.")
        
        else:
            self.result_num = len(result)
            if(len(result) + self.no_del_cnt<=19):            
                #데이터 세팅
                if self.no_del_cnt == 0:
                    for i in range(len(result)):
                        self.rpName_lbl.append(QLabel("상벌명:"))
                        self.rpName_le.append(QLineEdit(result[i][0]))
                        self.rpScore_lbl.append(QLabel("점수:"))
                        self.rpScore_le.append(QLineEdit(str(result[i][1])))
                        self.rpDate_lbl.append(QLabel("일자:"))
                        self.rpDate_de.append(QDateEdit(QDate.fromString(result[i][2].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.rpNote_lbl.append(QLabel("상벌내용:"))
                        self.rpNote_le.append(QLineEdit(result[i][3]))    
                        self.del_btn.append(QPushButton("삭제",self))
                        self.btnGroup.addButton(self.del_btn[i])                    
                        
                elif self.no_del_cnt != 0:    
                    for i in range(len(result)):
                        self.rpName_lbl.append(QLabel("상벌명"))
                        self.rpName_le.append(QLineEdit())
                        self.rpScore_lbl.append(QLabel("점수"))
                        self.rpScore_le.append(QLineEdit())
                        self.rpDate_lbl.append(QLabel("상벌일"))
                        self.rpDate_de.append(QDateEdit())
                        self.rpNote_lbl.append(QLabel("상벌내용"))
                        self.rpNote_le.append(QLineEdit())        

                for j in range(len(result)+self.no_del_cnt):
                    for i in range(len(self.widget)):
                        if i == 0:
                            self.lay.addWidget(self.widget[i][j], 0 + 4 * j, 0)
                        elif i % 2 == 0:
                            self.lay.addWidget(self.widget[i][j], int(i / 2) + 4 * j, 0)
                            if i % 4 == 2:
                                if j < len(result):
                                    self.lay.addWidget(self.del_btn[j], int(i/2)-1 + 4 * j,2)
                        elif i % 2 == 1:
                            self.lay.addWidget(self.widget[i][j], int(i / 2) + 4 * j, 1)
                            if i % 4 == 3:
                                self.lay.addWidget(self.add_btn, int(i / 2) + 4 * j, 2)
                                
                for i in range(len(result) + self.no_del_cnt):
                    self.rpScore_le[i].setValidator(QIntValidator())

                self.lay.setRowStretch(self.lay.rowCount(), 1)
                self.no_del_cnt+=1
                self.cnt+=1
            else:
                QMessageBox.information(self,"경고","20번 이상 등록하실 수 없습니다.")        

    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT NAME_REW_PUNI, SCORE, DATE_REW_PUNI, NOTE PROFICIENCY,NOTE FROM R_P WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveRP(self, emp_num, cur, conn):
        result = self.setData(self.emp_num)
        # 저장된 정보가 있으면 update 없으면 insert
        if not result and self.rpName_le[0].text() == '':
            return
        for i in range(len(self.rpName_lbl)):
            rp_info = False
            rpName = self.rpName_le[i].text()
            rpScore = int(self.rpScore_le[i].text())
            rpDate = self.rpDate_de[i].date().toString("yyyy-MM-dd")
            rpNote = self.rpNote_le[i].text()

            query = "SELECT * FROM R_P WHERE EMP_NUM = %s AND NAME_REW_PUNI = %s AND DATE_REW_PUNI = %s"
            cur.execute(query, (self.emp_num, rpName, rpDate,))
            rp_info = cur.fetchone()
            # 저장된 데이터가 있으면 UPDATE, 없으면 INSERT
            if rp_info:
                query = "UPDATE R_P SET NAME_REW_PUNI = %s, SCORE = %s, DATE_REW_PUNI = %s, NOTE = %s WHERE EMP_NUM = %s AND NAME_REW_PUNI = %s AND DATE_REW_PUNI = %s;"
                cur.execute(query, (rpName, rpScore, rpDate, rpNote, emp_num, rpName, rpDate,))
            else:
                query = "INSERT INTO R_P (EMP_NUM, NAME_REW_PUNI, SCORE, DATE_REW_PUNI, NOTE) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(query, (emp_num, rpName, rpScore, rpDate, rpNote))
            conn.commit()
        if self.del_name:
            for i in range(len(self.del_name)):
                query = "DELETE FROM R_P WHERE EMP_NUM = %s AND NAME_REW_PUNI = %s AND DATE_REW_PUNI = %s;"
                cur.execute(query, (emp_num, self.del_name[i], self.del_date[i],))
                conn.commit() 

    def disappearRP(self,index):
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까?\n삭제 후 저장버튼을 누르면 삭제됩니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        else:
            j=0
            btn = self.btnGroup.button(index)
            # 삭제할 위젯 행 찾기
            for i in range(len(self.del_btn)):
                if btn == self.del_btn[i]:
                    j = i
            # 삭제할 위젯의 데이터 저장 
            self.del_name.append(self.rpName_le[j].text())
            self.del_date.append(self.rpDate_de[j].date().toString("yyyy-MM-dd"))
            # j번째 행의 값을 뺀 후, 그 다음 행의 값을 해당 위치로 이동
            for i in range(len(self.rpName_lbl) - 1):
                if i >= j:
                    # 현재 행을 j행으로 이동
                    self.rpName_le[i].setText(self.rpName_le[i + 1].text())
                    self.rpScore_le[i].setText(self.rpScore_le[i + 1].text())
                    self.rpDate_de[i].setDate(self.rpDate_de[i + 1].date())
                    self.rpNote_le[i].setText(self.rpNote_le[i + 1].text())
            # 위젯이 하나 남기 전까지 위젯 삭제
            if self.edit_num != 1:
                # 위젯 한줄씩 삭제
                for i in range(len(self.widget)):
                    self.lay.removeWidget(self.widget[i][self.edit_num-1])
                    self.widget[i].pop(self.edit_num-1)
                self.lay.removeWidget(self.del_btn[self.edit_num-1])
                self.btnGroup.removeButton(self.del_btn[self.edit_num-1])
                self.del_btn.pop(self.edit_num-1)  
                self.cnt-=1
            # 위젯이 하나 남을 경우 에디터 초기화
            else : 
                self.rpName_le[i].setText("")
                self.rpScore_le[i].setText("")
                self.rpDate_de[i].setDate(QDate(2000, 1, 1))
                self.rpNote_le[i].setText("")
                self.rpScore_le[i].setValidator(QIntValidator())
            self.edit_num-=1
            # 위젯이 전부 제거되기 전까지만 추가 버튼 위치 변경
            if self.edit_num != 0:
                self.lay.addWidget(self.add_btn, 2 + 3 * (len(self.rpName_lbl)-1), 2)
            self.lay.setRowStretch(self.lay.rowCount(), 1)      
            # 위젯이 전부 제거 되면 다시 입력창 생성
            if self.cnt == 0:
                self.editRPMember()
            self.ignored_result = True     
    
class RSTab(QWidget):
    def __init__(self, emp_num, type):
        super(RSTab, self).__init__()
        self.cnt = 0
        self.cnt = 0
        self.no_del_cnt = 0
        self.result_num = 0
        self.emp_num = emp_num
        self.type = type
        self.initUI()

    def initUI(self):
        self.rs = QScrollArea()
        self.cnt = 0
        self.widget = QWidget()
        self.rs.setWidget(self.widget)
        self.lay = QGridLayout(self.widget)
        self.rs.setWidgetResizable(True)

        self.rsRANK_lbl = []
        self.rsRANK_le = []
        self.rsSal_lbl = []
        self.rsSal_le = []
        self.rsDate_lbl = []
        self.rsDate_de = []
        self.widget = [self.rsRANK_lbl, self.rsRANK_le, self.rsSal_lbl, self.rsSal_le, self.rsDate_lbl, self.rsDate_de]
        self.ignored_result = False
        if self.type == 'info':
            self.addRSMember()
        else:
            self.add_btn = QPushButton("추가")
            self.btnGroup = QButtonGroup(self)
            self.del_btn = []
            self.editRSMember()
            self.cnt = self.result_num
            self.edit_num = self.result_num
            self.del_rank = []
            self.add_btn.clicked.connect(self.editRSMember)
            self.btnGroup.buttonClicked[int].connect(self.disappearRS)

    def addRSMember(self):
        result = self.setData(self.emp_num)
        if not result:
            return
        else:
            self.cnt = len(result)

        # 데이터 세팅
        for i in range(self.cnt):
            self.rsRANK_lbl.append(QLabel("직급:"))
            self.rsRANK_le.append(QLabel(result[i][0]))

            self.rsSal_lbl.append(QLabel("호봉:"))
            self.rsSal_le.append(QLabel(str(result[i][1])))

            self.rsDate_lbl.append(QLabel("시작일:"))
            self.rsDate_de.append(QLabel(str(result[i][2])))

        for j in range(self.cnt):
            for i in range(len(self.widget)):
                if i % 2 == 0:
                    self.lay.addWidget(self.widget[i][j], int(i/2) + 3 * j, 0)
                elif i % 2 == 1:
                    self.lay.addWidget(self.widget[i][j], int(i/2) + 3 * j, 1)

        self.lay.setRowStretch(self.lay.rowCount(), 1)
        rightmost_column_index = len(self.widget) - 1
        self.lay.setColumnStretch(rightmost_column_index, 1)
        
    def editRSMember(self):
                # 기존에 등록한 데이터가 있는지 확인
        result = self.setData(self.emp_num)
        # 231205 없을 경우 등록화면과 동일하게 동작 by 정현아
        if not result or self.ignored_result:
            if(self.cnt<=29):
                self.rsRANK_lbl.append(QLabel("직급"))
                self.rsRANK_le.append(QLineEdit(self))
                self.rsSal_lbl.append(QLabel("호봉"))
                self.rsSal_le.append(QLineEdit(self))
                self.rsDate_lbl.append(QLabel("시작일"))
                self.rsDate_de.append(QDateEdit(self))
                
                for i in range(len(self.widget)):
                    if i == 0:
                        self.lay.addWidget(self.widget[i][self.cnt],0 + 3 * self.cnt,0)
                    elif i % 2 == 0:
                        self.lay.addWidget(self.widget[i][self.cnt],int(i/2) + 3 * self.cnt,0)
                    elif i % 2 == 1:
                        self.lay.addWidget(self.widget[i][self.cnt],int(i/2) + 3 * self.cnt,1)
                        if i % 3 == 2:
                            self.lay.addWidget(self.add_btn,int(i/2) + 3 * self.cnt,2)
                
                self.lay.setRowStretch((self.lay.rowCount()*(4-self.cnt)),1)
                self.cnt+=1
            else:
                QMessageBox.information(self,"경고","30번 이상 등록하실 수 없습니다.")
        # 231205 있을 경우 등록된 데이터를 각 에디터에 세팅 by 정현아
        else :
            self.result_num = len(result)
            if(len(result) + self.no_del_cnt<=29):            
                #데이터 세팅
                if self.no_del_cnt == 0:
                    for i in range(len(result)):
                        self.rsRANK_lbl.append(QLabel("직급:"))
                        self.rsRANK_le.append(QLineEdit(result[i][0]))
                        self.rsSal_lbl.append(QLabel("호봉:"))
                        self.rsSal_le.append(QLineEdit(str(result[i][1])))
                        self.rsDate_lbl.append(QLabel("시작일:"))
                        self.rsDate_de.append(QDateEdit(QDate.fromString(result[i][2].strftime("%Y-%m-%d"), "yyyy-MM-dd")))
                        self.del_btn.append(QPushButton("삭제",self))
                        self.btnGroup.addButton(self.del_btn[i])
                
                elif self.no_del_cnt != 0:
                    self.rsRANK_lbl.append(QLabel("직급"))
                    self.rsRANK_le.append(QLineEdit())
                    self.rsSal_lbl.append(QLabel("호봉"))
                    self.rsSal_le.append(QLineEdit())
                    self.rsDate_lbl.append(QLabel("시작일"))
                    self.rsDate_de.append(QDateEdit())
                        
                for j in range(len(result) + self.no_del_cnt):
                    for i in range(len(self.widget)):
                        if i == 0:
                            self.lay.addWidget(self.widget[i][j], 0 + 4 * j, 0)
                        elif i % 2 == 0:
                            self.lay.addWidget(self.widget[i][j], int(i / 2) + 4 * j, 0)
                            if j < len(result):
                                self.lay.addWidget(self.del_btn[j], int(i / 2) + 4 * j-1,2)
                        elif i % 2 == 1:
                            self.lay.addWidget(self.widget[i][j], int(i / 2) + 4 * j, 1)
                            if i % 3 == 2:
                                self.lay.addWidget(self.add_btn, int(i / 2) + 4 * j, 2)

                self.lay.setRowStretch((self.lay.rowCount()*(4-self.no_del_cnt)),1)
                self.no_del_cnt+=1
                self.cnt += 1
            else:
                QMessageBox.information(self,"경고","10번 이상 등록하실 수 없습니다.")
            
    def setData(self,emp_num):
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT EMP_RANK, SALARY, DATE_JOIN FROM R_S WHERE EMP_NUM = %s;"
        cur.execute(query,(emp_num,))
        result = cur.fetchall()
        conn.close()
        return result
    
    def saveRS(self, emp_num, cur, conn):
        result = self.setData(self.emp_num)
        # 저장된 정보가 있으면 update 없으면 insert
        if not result and self.rsRANK_le[0].text() == '':
            return
        for i in range(len(self.rsRANK_lbl)):
            rs_info = False
            rsRANK = self.rsRANK_le[i].text()
            rsSal = self.rsSal_le[i].text()
            rsDate = self.rsDate_de[i].date().toString("yyyy-MM-dd")
            query = "SELECT * FROM R_S WHERE EMP_NUM = %s AND EMP_RANK = %s;"
            cur.execute(query, (self.emp_num, rsRANK,))
            rs_info = cur.fetchone()
            # 저장된 데이터가 있으면 UPDATE, 없으면 INSERT
            if rs_info:
                query = "UPDATE R_S SET EMP_RANK = %s, SALARY = %s, DATE_JOIN = %s WHERE EMP_NUM = %s AND EMP_RANK = %s;"
                cur.execute(query, (rsRANK, rsSal, rsDate, emp_num, rsRANK))
            else:
                query = "INSERT INTO R_S (EMP_NUM, EMP_RANK, SALARY, DATE_JOIN) VALUES (%s, %s, %s, %s)"
                cur.execute(query, (emp_num, rsRANK, rsSal, rsDate))
            conn.commit()
        if self.del_rank:
            for rank in self.del_rank:
                query = "DELETE FROM R_S WHERE EMP_NUM = %s AND EMP_RANK = %s;"
                cur.execute(query, (emp_num, rank,))
                conn.commit() 

    def disappearRS(self,index):
        reply = QMessageBox.question(self, '삭제 확인', '삭제하시겠습니까?\n삭제 후 저장버튼을 누르면 삭제됩니다.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        else:
            j=0
            btn = self.btnGroup.button(index)
            # 삭제할 위젯 행 찾기
            for i in range(len(self.del_btn)):
                if btn == self.del_btn[i]:
                    j = i
            # 삭제할 위젯의 데이터 저장 
            self.del_rank.append(self.rsRANK_le[j].text())
            # j번째 행의 값을 뺀 후, 그 다음 행의 값을 해당 위치로 이동
            for i in range(len(self.rsRANK_lbl) - 1):
                if i >= j:
                    # 현재 행을 j행으로 이동
                    self.rsRANK_le[i].setText(self.rsRANK_le[i + 1].text())
                    self.rsSal_le[i].setText(self.rsSal_le[i + 1].text())
                    self.rsDate_de[i].setDate(self.rsDate_de[i + 1].date())
            # 위젯이 하나 남기 전까지 위젯 삭제
            if self.edit_num != 1:
                # 위젯 한줄씩 삭제
                for i in range(len(self.widget)):
                    self.lay.removeWidget(self.widget[i][self.edit_num-1])
                    self.widget[i].pop(self.edit_num-1)
                self.lay.removeWidget(self.del_btn[self.edit_num-1])
                self.btnGroup.removeButton(self.del_btn[self.edit_num-1])
                self.del_btn.pop(self.edit_num-1)  
                self.cnt-=1
            # 위젯이 하나 남을 경우 에디터 초기화
            else : 
                self.rsRANK_le[i].setText("")
                self.rsSal_le[i].setText("")
                self.rsDate_de[i].setDate(QDate(2000, 1, 1))
            self.edit_num-=1
            # 위젯이 전부 제거되기 전까지만 추가 버튼 위치 변경
            if self.edit_num != 0:
                self.lay.addWidget(self.add_btn, 2 + 3 * (len(self.rsRANK_lbl)-1), 2)
            self.lay.setRowStretch(self.lay.rowCount(), 1)      
            # 위젯이 전부 제거 되면 다시 입력창 생성
            if self.cnt == 0:
                self.editRSMember()
            self.ignored_result = True 
