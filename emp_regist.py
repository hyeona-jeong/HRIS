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

        self.path = None
        self.fname = None
        self.pixmap = None
        self.regist.setLayout(self.regLayout)
        self.addImgBtn.clicked.connect(self.showAddImg)
        
        # 각 입력항목들 입력 제한
        self.namekr_lineEdit.textChanged.connect(self.setValKor)
        rep = QRegExp("[a-zA-Z\\s]{19}")
        self.nameEng_lineEdit.setValidator(QRegExpValidator(rep))
        self.regnum_lineEdit.setValidator(QIntValidator(1,100000,self))
        self.regnum_lineEdit2.setValidator(QIntValidator(1,1000000,self))
        rep = QRegExp("[a-z0-9]+@[a-z]+.[a-z]+.[a-z]{2}")
        self.email_lineEdit.setValidator(QRegExpValidator(rep))
        rep = QRegExp("[가-힣0-9\\s]{49}")
        self.addre_lineEdit.setValidator(QRegExpValidator(rep))
        self.empNum_lineEdit.setValidator(QIntValidator(1,10000000,self))
        self.phone_lineEdit2.setValidator(QIntValidator(1,1000,self))
        self.phone_lineEdit3.setValidator(QIntValidator(1,1000,self))
        self.addressNum_lineEdit.setValidator(QIntValidator(1,10000,self))
        self.sal_lineEdit.setValidator(QIntValidator(1,10,self))
        self.height_lineEdit.setValidator(QIntValidator(1,100,self))
        self.weight_lineEdit.setValidator(QIntValidator(1,100,self))
        self.lastEdu_combo.setCurrentIndex(1)
        self.searchAddress.setVisible(False)  
        self.dateEdit.setDate(QDate.currentDate())
        
        self.TSP = ['생산실행IT G','생산스케쥴IT G','생산품질IT G','TSP운영 1G','TSP운영 2G','TSP고객총괄']
        self.FAB = ['빅데이터 G','인프라 G','스마트팩토리 G']
        self.MIS = ['전기운영 G','PLM G']
        self.TC = ['TC/TPSS개발파트','화성 TC2.5','SAS TC2.5']
        self.SP = ['사업기획팀','기술전략팀']
        self.group_combo.addItems(self.TSP)
        self.biz_combo.activated[str].connect(self.changeGroup)

        self.conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        self.cur = self.conn.cursor()        
        
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
        rep = QRegExp("[가-힣]{4}")
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
        attrDict ={
            '한글성명':'',  
            '영문성명':'',             
            '사번':'', 
            '주민번호':'',
            'pic':'',  
            '메일':'', 
            '휴대폰번호':'',  
            '입사일':'',             
            '사업부':'',  
            '그룹':'',   
            '직급':'',  
            '직책':'',  
            '직무':'',    
            '우편번호':'',
            '주소':'', 
            '호봉':'',  
            '신장': None,  
            '체중': None,             
            '군필여부':'', 
            '결혼여부':'',  
            '최종학력':'',            
            'age':'',
            'gender':'',  
                    }
        if self.pixmap is not None:
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            self.pixmap.toImage().save(buffer, 'PNG')
            attrDict['pic'] = byte_array
        if self.empNum_lineEdit.text() == '':
            QMessageBox.warning(self, "사원등록실패", "사번이 입력되지 않았습니다.사번 입력바랍니다.")
            return
        else:
            attrDict['사번'] = int(self.empNum_lineEdit.text())
        attrDict['한글성명'] = self.namekr_lineEdit.text()
        attrDict['영문성명'] = self.namekr_lineEdit.text()
        attrDict['주민번호'] = self.regnum_lineEdit.text() + self.regnum_lineEdit2.text()
        reg_num = self.regnum_lineEdit.text() + self.regnum_lineEdit2.text()
        attrDict['메일'] = self.email_lineEdit.text()
        attrDict['휴대폰번호'] = self.phone_combo.currentText() + self.phone_lineEdit2.text() + self.phone_lineEdit3.text()
        attrDict['주소'] = self.addre_lineEdit.text()
        attrDict['사업부'] = self.biz_combo.currentText()
        attrDict['그룹'] = self.group_combo.currentText()
        attrDict['입사일'] = self.dateEdit.date().toString("yyyy-MM-dd")
        attrDict['직급'] = self.rank_combo.currentText()
        attrDict['직책'] = self.workPos_combo.currentText()
        attrDict['직무'] = self.position_combo.currentText()
        attrDict['호봉'] = self.sal_combo.currentText() + self.sal_lineEdit.text()
        attrDict['최종학력'] = self.lastEdu_combo.currentText() 

        if self.height_lineEdit.text() != '':
            attrDict['신장'] = int(self.height_lineEdit.text())
        if self.weight_lineEdit.text() != '':
            attrDict['체중'] = int(self.weight_lineEdit.text())
        
        if self.military_btn.isChecked():
            attrDict['군필여부'] = self.military_btn.text()
        elif self.military_btn2.isChecked():
            attrDict['군필여부'] = self.military_btn2.text()
        else:
            attrDict['군필여부'] = self.military_btn3.text()
            
        if self.marry_btn.isChecked():
            attrDict['결혼여부'] = self.marry_btn.text()
        elif self.marry_btn2.isChecked():
            attrDict['결혼여부'] = self.marry_btn2.text()
        
        # 231130 만나이계산 및 성별 by 정현아
        if attrDict['주민번호'] == '':
            QMessageBox.warning(self, "사원등록실패", "주민번호가 입력되지 않았습니다. 주민번호 입력바랍니다.")
            return
        else:
            if reg_num[6] == '0' or reg_num[6] == '9' :
                QMessageBox.warning(self, "사원등록실패", "주민번호 2번째 첫자리는 1~8까지 입력가능합니다.")
                return
            elif reg_num[6] == '1' or reg_num[6] == '2' or reg_num[6] == '5' or reg_num[6] == '6':
                birthYear = 1900 + int(reg_num[:2])
            elif reg_num[6] == '3' or reg_num[6] == '4' or reg_num[6] == '7' or reg_num[6] == '8':
                birthYear = 2000 + int(reg_num[:2])
            

            if int(reg_num[2:4])>12 or reg_num[2:4] =='00' or reg_num[4:6] == '00':
                QMessageBox.warning(self, "사원등록실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                return
            elif reg_num[2:4] =='01' or  reg_num[2:4] =='03' or reg_num[2:4] =='05' or reg_num[2:4] == '07' or reg_num[2:4] == '08' or reg_num[2:4] == '10' or reg_num[2:4] == '12':
                if int(reg_num[4:6]) > 31:
                    QMessageBox.warning(self, "사원등록실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
            elif reg_num[2:4] =='04' or reg_num[2:4] =='06' or reg_num[2:4] =='09' or reg_num[2:4] =='11':
                if int(reg_num[4:6]) > 30:
                    QMessageBox.warning(self, "사원등록실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
            else:
                if int(reg_num[4:6]) > 28:
                    QMessageBox.warning(self, "사원등록실패", "주민번호 형식이 맞지 않습니다. 생년월일 확인바랍니다.")
                    return
                
            age =  int(QDate(birthYear,int(reg_num[2:4]),int(reg_num[4:6])).daysTo(QDate.currentDate())/365)
            if age < 19:
                QMessageBox.warning(self, "사원등록실패", "나이가 만 19세보다 어립니다.주민번호 확인바랍니다.")
                return
            elif age > 80:
                QMessageBox.warning(self, "사원등록실패", "나이가 만 80세보다 많습니다.주민번호 확인바랍니다.")
                return
            else:
                attrDict['age'] = age

            if int(reg_num[6]) % 2 == 1:
                attrDict['gender'] = '남'
            else : 
                attrDict['gender'] = '여'

        if not re.match(r"^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", attrDict['메일']):
            QMessageBox.warning(self,'사원등록실패','메일 형식이 틀립니다.메일 확인바랍니다.')
            return
        
        if len(str(attrDict['사번'])) < 8:
            QMessageBox.warning(self,'사원등록실패','사번은 8자리를 입력하셔야 합니다.')
            return
        
        if int(str(attrDict['사번'])[:2]) < 12 or int(str(attrDict['사번'])[:2]) > int(QDate.currentDate().year())-2000:
            QMessageBox.warning(self,'사원등록실패','사번은 앞 2자리는 12보다 작거나 현재년도보다 클 수 없습니다.')
            return
        
        if self.addressNum_lineEdit.text() == '':
            QMessageBox.warning(self, "사원등록실패", "우편번호가 입력되지 않았습니다. 우편번호 입력바랍니다.")
            return
        else:
            attrDict['우편번호'] = int(self.addressNum_lineEdit.text())        

        if len(str(attrDict['우편번호'])) != 5:
            QMessageBox.warning(self, "사원등록실패", "우편번호는 5자리를 입력하셔야 합니다.")
            return
        
            
        for key, value in attrDict.items():
            if key == '호봉':
                if len(value) != 3 :
                    QMessageBox.warning(self, "사원등록실패", "{}이(가) 입력되지 않았습니다. {} 입력바랍니다.".format(key, key))
                    return

            elif not (key == '신장' or key == '체중' or key == '그룹' or key == '직무' or key == 'pic' or key == 'age' or key == 'gender'):
                if value == '':
                    QMessageBox.warning(self, "사원등록실패", "{}이(가) 입력되지 않았습니다. {} 입력바랍니다.".format(key, key))
                    return
        
        query = """
        INSERT INTO MAIN_TABLE (
            NAME_KOR,
            NAME_ENG,
            EMP_NUM,
            REG_NUM,
            PIC,
            MAIL,
            PHONE,
            DATE_JOIN,
            DEPT_BIZ,
            DEPT_GROUP,
            EMP_RANK,
            WORK_POS,
            POSITION,
            ADDRESS_NUM,
            ADDRESS,
            SALARY,
            HEIGHT,
            WEIGHT,
            MILITARY,
            MARRY,
            LAST_EDU,
            AGE,
            GENDER
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """  
        try:
            self.cur.execute(query, tuple(attrDict.values()))
            self.conn.commit()
            QMessageBox.information(self, "등록되었습니다.")
        except Exception as e:
                print(self, "사원등록실패", "Error: " + str(e))

        self.namekr_lineEdit.clear()
        self.regnum_lineEdit.clear()
        self.regnum_lineEdit2.clear()
        self.nameEng_lineEdit.clear()
        self.email_lineEdit.clear()
        self.empNum_lineEdit.clear()
        self.phone_lineEdit2.clear()
        self.phone_lineEdit3.clear()
        self.addressNum_lineEdit.clear()
        self.addre_lineEdit.clear()
        self.sal_lineEdit.clear()
        self.height_lineEdit.clear()
        self.weight_lineEdit.clear()
        
    # 231123 페이지 전환 함수 by 정현아    
    def showAddImg(self):
        self.w = AddImg()
        self.w.show()
        self.w.searchbutton.clicked.connect(self.open_image)
        self.w.savebtn.clicked.connect(self.save_img)
        self.w.cnlBtn.clicked.connect(self.w.close)
    
    # 231130 이미지 선택하고 다이알로그 텍스트 라인 에디트에 파일경로 세팅 by 정현아
    def open_image(self):
        self.path = None
        self.fname = None
        self.fname, _ = QFileDialog.getOpenFileName(self, '이미지 파일 찾기', 'C:/Program Files', '이미지 파일(*.jpg *.gif, *.png)')
        if self.fname:
            max_file_size_mb = 1
            max_file_size_bytes = max_file_size_mb * 1024 * 1024

            size, self.path = self.get_file_size(self.fname)
            if size >= max_file_size_bytes:
                QMessageBox.warning(self,'사진등록실패','사진 사이즈가 1MB를 초과하였습니다.')
                return
            else:
                self.w.imgPath_textEdit.setText(self.path)
                self.w.hide()
                self.w.show()

    def get_file_size(self, file_path):
        return os.path.getsize(file_path), file_path
    
    def save_img(self):
        if self.path is None :
            QMessageBox.warning(self,'사진등록실패','선택된 사진이 없습니다.\n사진을 선택해주세요.')
            return
        else: 
                self.pixmap = QPixmap(self.fname)
                width = 130
                height = 150
                resize_pixmap = self.pixmap.scaled(width,height)
                self.img_label.setPixmap(resize_pixmap)
        self.w.close()

    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Regist() 
    myWindow.show() 
    app.exec_() 