import os
import sys
import re
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from add_img import AddImg

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('emp_regist.ui')
form_class = uic.loadUiType(form)[0]

class Regist(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        
        self.regist.setLayout(self.regLayout)
        self.addImgBtn.clicked.connect(self.showAddImg)
        
        # 각 입력항목들 입력 제한
        self.namekr_lineEdit.textChanged.connect(self.setValKor)
        self.regnum_lineEdit.setValidator(QIntValidator(1,100000,self))
        self.regnum_lineEdit2.setValidator(QIntValidator(1,1000000,self))
        self.empNum_lineEdit.setValidator(QIntValidator(1,10000000,self))
        self.phone_lineEdit.setValidator(QIntValidator(1,100,self))
        self.phone_lineEdit2.setValidator(QIntValidator(1,1000,self))
        self.phone_lineEdit3.setValidator(QIntValidator(1,1000,self))
        self.addressNum_lineEdit.setValidator(QIntValidator(1,10000,self))
        self.sal_lineEdit.setValidator(QIntValidator(1,10,self))
        self.height_lineEdit.setValidator(QIntValidator(1,100,self))
        self.weight_lineEdit.setValidator(QIntValidator(1,100,self))
        self.lastEdu_combo.setCurrentIndex(1)
        self.searchAddress.setVisible(False)  
        self.dateEdit.setDate(QDate.currentDate())
        
        self.TSP = ['생산실행IT G','생산스케쥴IT G','생산품질IT G','TSP운영 1G','TSP운영 2G','TSP고객총괄','']
        self.FAB = ['빅데이터 G','인프라 G','스마트팩토리 G','']
        self.MIS = ['전기운영 G','PLM G','']
        self.TC = ['TC/TPSS개발파트','화성 TC2.5','SAS TC2.5','']
        self.SP = ['사업기획팀','기술전략팀','']
        self.group_combo.addItems(self.TSP)
        self.biz_combo.activated[str].connect(self.changeGroup)
        
        self.saveBtn.clicked.connect(self.saveEmp)
        
    # 231130 한글성명입력제한 함수 by 정현아
    def setValKor(self):
        text = self.namekr_lineEdit.text()
        if text == '':
            return
        elif not re.match("[가-힣]", text):
            QMessageBox.warning(self,'입력오류','한글을 입력해주세요')
            self.namekr_lineEdit.clear()
            return
        rep = QRegExp("[가-힣]{0,4}")
        self.namekr_lineEdit.setValidator(QRegExpValidator(rep))
    
    # 231130 사업부별 그룹 콤보박스 생성
    def changeGroup(self,biz):
        self.group_combo.clear()
        if biz == '경영지원실':
            return
        elif biz == 'TSP':
            self.group_combo.addItems(self.TSP)
        elif biz == 'FAB':
            self.group_combo.addItems(self.FAB)
        elif biz == 'MIS':
            self.group_combo.addItems(self.MIS)
        elif biz == 'TC':
            self.group_combo.addItems(self.TC)
        elif biz == '전략기획실':    
            self.group_combo.addItems(self.SP) 
    
    # 231130 사원정보저장 함수 by 정현아
    def saveEmp(self):
        birthYear = 0
        attrDict ={'사번':'', 
                   '한글성명':'',  
                   '영문성명':'',  
                   '주민번호':'',  
                   'pic':'',
                   'age':'',
                   '휴대폰번호':'', 
                   '메일':'',   
                   '주소':'',  
                   '우편번호':'',  
                   '사업부':'',  
                   '그룹':'',  
                   '입사일':'',  
                   '직급':'',  
                   '직책':'',  
                   '직무':'',  
                   '호봉':'',  
                   '최종학력':'',
                   '군필여부':'', 
                   '결혼여부':'',  
                   '신장':'',  
                   '체중':'',     
                   'gender':'',  
                    }
        if self.empNum_lineEdit.text() == '':
            QMessageBox.warning(self, "사원등록실패", "사번이 입력되지 않았습니다.사번 입력바랍니다.")
            return
        else:
            attrDict['emp_num'] = int(self.empNum_lineEdit.text())
        attrDict['name_kor'] = self.namekr_lineEdit.text()
        attrDict['name_eng'] = self.namekr_lineEdit.text()
        attrDict['reg_num'] = self.regnum_lineEdit.text() + self.regnum_lineEdit2.text()
        reg_num = self.regnum_lineEdit.text() + self.regnum_lineEdit2.text()
        attrDict['mail'] = self.email_lineEdit.text()
        attrDict['phone'] = self.phone_lineEdit.text() + self.phone_lineEdit2.text() + self.phone_lineEdit3.text()
        attrDict['address'] = self.addre_lineEdit.text()
        attrDict['dept_biz'] = self.biz_combo.currentText()
        attrDict['dept_group'] = self.group_combo.currentText()
        attrDict['date_join'] = self.dateEdit.date().toString("yyyy-MM-dd")
        attrDict['emp_rank'] = self.rank_combo.currentText()
        attrDict['work_pos'] = self.workPos_combo.currentText()
        attrDict['position'] = self.position_combo.currentText()
        attrDict['salary'] = self.sal_combo.currentText() + self.sal_lineEdit.text()
        attrDict['last_edu'] = self.lastEdu_combo.currentText() 
         
        if self.height_lineEdit.text() != '':
            attrDict['height'] = int(self.height_lineEdit.text())
        if self.weight_lineEdit.text() != '':
            attrDict['weight'] = int(self.weight_lineEdit.text())
        
        if self.military_btn.isChecked():
            attrDict['military'] = self.military_btn.text()
        elif self.military_btn2.isChecked():
            attrDict['military'] = self.military_btn2.text()
        else:
            attrDict['military'] = self.military_btn3.text()
            
        if self.marry_btn.isChecked():
            attrDict['marry'] = self.marry_btn.text()
        elif self.marry_btn2.isChecked():
            attrDict['marry'] = self.marry_btn2.text()
        
        # 231130 만나이계산 및 성별 by 정현아
        if attrDict['reg_num'] == '':
            QMessageBox.warning(self, "사원등록실패", "주민번호가 입력되지 않았습니다. 주민번호 입력바랍니다.")
            return
        else:
            if reg_num[6] == '0' or reg_num[6] == '9' :
                QMessageBox.warning(self, "사원등록실패", "주민번호2번째 첫자리는 1~8까지만 입력가능합니다.")
                return
            elif reg_num[6] == '1' or reg_num[6] == '2' or reg_num[6] == '5' or reg_num[6] == '6':
                birthYear = 1900 + int(reg_num[:2])
            elif reg_num[6] == '3' or reg_num[6] == '4' or reg_num[6] == '7' or reg_num[6] == '8':
                birthYear = 2000 + int(reg_num[:2])

            if int(reg_num[6]) % 2 == 1:
                attrDict['gender'] = '남'
            else : 
                attrDict['gender'] = '여'
        
            age =  int(QDate(birthYear,int(reg_num[2:4]),int(reg_num[4:6])).daysTo(QDate.currentDate())/365)
            if age < 19:
                QMessageBox.warning(self, "사원등록실패", "나이가 만 19세보다 어립니다.주민번호 확인바랍니다.")
                return
            elif age > 80:
                QMessageBox.warning(self, "사원등록실패", "나이가 만 80세보다 많습니다.주민번호 확인바랍니다.")
                return
            else:
                attrDict['age'] = age
        
        if self.addressNum_lineEdit.text() == '':
            QMessageBox.warning(self, "사원등록실패", "우편번호가 입력되지 않았습니다. 우편번호 입력바랍니다.")
            return
        else:
            attrDict['address_num'] = int(self.addressNum_lineEdit.text())        
            
        for key,value in attrDict.items():
            if not (key == '신장' or  key == '체중' or key == '그룹' or key == '직무' or key == 'pic' or key == 'age' or key == 'gender') :
                if value == '':
                    QMessageBox.warning(self, "사원등록실패", "{}가 입력되지 않았습니다. {} 입력바랍니다.".format(value))
        
        

        
    # 231123 페이지 전환 함수 by 정현아    
    def showAddImg(self):
        self.w = AddImg()
        self.w.show()
        self.w.cnlBtn.clicked.connect(self.w.close)
        
    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Regist() 
    myWindow.show() 
    app.exec_() 