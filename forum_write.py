import os
import sys
import re

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from upload_file import UploadFile

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('write.ui')
form_class = uic.loadUiType(form)[0]

class Write(QMainWindow, form_class):
    closed = pyqtSignal()

    def __init__(self, emp_num = 23098098, conn=None, cur=None):
        super( ).__init__( )
        self.setupUi(self)
        self.file_path_list = []
        self.del_btn_list = []
        self.file_lbl_list = [self.file_lbl]
        self.cnt = 0
        self.atch_files = ''
        
        self.font = QFont("Malgun Gothic", 9)
        self.charFormat = QTextCharFormat()
        self.charFormat.setFont(self.font)
        self.cursor = self.contents_te.textCursor()
        self.file_lbl.setText("파일은 최대 5개까지 첨부가능합니다.")
        
        self.title_le.setFocus()
        
        self.contents_te.setCurrentCharFormat(self.charFormat)
        self.contents_te.setAcceptRichText(True)
        
        self.bold_btn.setCheckable(True)
        self.italic_btn.setCheckable(True)
        self.underline_btn.setCheckable(True)
        
        self.font_combo.activated[str].connect(self.chg_font_famliy)
        self.font_size_combo.activated[str].connect(self.chg_font_size)
        self.align_combo.activated[int].connect(self.chg_align)
        
        self.bold_btn.clicked.connect(self.bold)
        self.italic_btn.clicked.connect(self.italic)
        self.underline_btn.clicked.connect(self.underline)
        self.submitBtn.clicked.connect(lambda: self.submit(emp_num, conn, cur))
        self.image_btn.clicked.connect(self.insert_image)
        self.file_btn.clicked.connect(self.attach_file)
        self.cnlBtn.clicked.connect(self.close)
        
    def submit(self, emp_num, conn, cur):
        self.setLoadingCursor(True)
        category = self.category_combo.currentText()
        title = self.title_le.text()
        content = self.contents_te.toPlainText()
        contents = self.contents_te.toHtml()
        imgs_path = None
        files_path = None
        
        if title == "":
            QMessageBox.warning(self,"게시글 등록 실패","제목을 입력해주세요.")
            return 
        
        if content == "":
            QMessageBox.warning(self,"게시글 등록 실패","내용을 입력해주세요.")
            return 
        
        query = "SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = %s"
        cur.execute(query,(emp_num))
        name = cur.fetchone()
        
        img_path_list = re.findall(r'<img\s+src="([^"]+)"[^>]*>', contents)
        files_path = None
        local_imgs_path = ",".join(img_path_list)
        local_files_path = ",".join(self.file_path_list) 
        uploader = UploadFile()
        
        # 구글드라이브에 이미지 파일 업로드 by 정현아
        if img_path_list:
            imgs_path = ''
            for path in img_path_list:
                img_url = uploader.upload_file(path)
                imgs_path += img_url  
                imgs_path += ","
                
        # 구글드라이브에 첨부 파일 업로드 by 정현아
        if self.file_path_list:
            files_path = ''
            for path in self.file_path_list:
                file_url = uploader.upload_file(path)
                files_path += file_url
                files_path += ","
        
        # 첨부파일 목록 저장 by 정현아
        if self.cnt != 0:
            for lbl in self.file_lbl_list:
                if lbl.text() == "":
                    break
                self.atch_files += lbl.text()
                self.atch_files += ","
            if self.atch_files == "" :
                self.atch_files = None

        query = "INSERT INTO FORUM(WRITER, TITLE, CATEGORY, CONTENTS, EMP_NUM, ATCH_IMG_PATH, ATCH_FILE_PATH, ATCH_FILE_NAME, ATCH_IMG_LOCAL_PATH, ATCH_FILE_LOCAL_PATH) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cur.execute(query, (name, title,category,contents, emp_num, imgs_path, files_path, self.atch_files, local_imgs_path, local_files_path))
        conn.commit()
        self.setLoadingCursor(False)
        self.close()
        
    # 231220 글씨체 변경 by 정현아
    def chg_font_famliy(self, font):
        if font == "맑은고딕":
            font_family = "Malgun Gothic"
        elif font == "돋움": 
            font_family = "Dotum"
        elif font == "돋움체":
            font_family = "Dotumche"
        elif font == "굴림":
            font_family = "Gulim"
        elif font == "굴림체":
            font_family = "Gulimche"
        elif font == "바탕":
            font_family = "Batang"
        elif font == "바탕체":
            font_family = "Batangche"
        elif font == "궁서":
            font_family = "Gungsuh"
        else:
            font_family = font
            
        self.font.setFamily(font_family)
        self.charFormat.setFont(self.font)
        self.contents_te.setCurrentCharFormat(self.charFormat)
    
    # 231220 글씨크기 변경 by 정현아
    def chg_font_size(self, size):
        # 콤보박스에서 pt를 제거하고 int타입으로 변경 후 size 변경
        size = int(size.replace("pt",""))
        self.font.setPointSize(size)
        self.charFormat.setFont(self.font)
        self.contents_te.setCurrentCharFormat(self.charFormat)
    
    # 231220 정렬 변경 by 정현아
    def chg_align(self, index):
        # QTextBlockFormat 객체를 생성하고 텍스트 블록 서식의 정렬 설정
        blockFormat = QTextBlockFormat()
        if index == 0:
            blockFormat.setAlignment(Qt.AlignLeft)
        elif index == 1:
            blockFormat.setAlignment(Qt.AlignHCenter)
        elif index == 2:
            blockFormat.setAlignment(Qt.AlignRight)
        elif index == 3:
            blockFormat.setAlignment(Qt.AlignJustify)
        self.cursor.setBlockFormat(blockFormat)
        self.contents_te.setTextCursor(self.cursor)
        
    # 231220 버튼이 클릭상태면 Bold 아니면 normal by 정현아
    def bold(self):
        self.charFormat.setFontWeight(QFont.Bold if self.bold_btn.isChecked() else QFont.Normal)
        self.contents_te.setCurrentCharFormat(self.charFormat)
    
    # 231220 버튼이 클릭상태면 Italic 아니면 normal by 정현아
    def italic(self):
        self.charFormat.setFontItalic(self.italic_btn.isChecked())
        self.contents_te.setCurrentCharFormat(self.charFormat)
        
    # 231220 버튼이 클릭상태면 Underline 아니면 normal by 정현아
    def underline(self):
        self.charFormat.setFontUnderline(self.underline_btn.isChecked())
        self.contents_te.setCurrentCharFormat(self.charFormat)
        
    # 231222 추가한 이미지 파일 정보 저장 by 정현아
    def insert_image(self):
        # 231220 File dialog로 이미지 파일을 선택하고 선택한 파일 정보를 읽어옴 by 정현아
        fname,_ = QFileDialog.getOpenFileName(self, '이미지 파일 추가', 'C:/Program Files', '이미지 파일(*.jpg *.gif, *.png)')
        
        if fname:
            img_format = QTextImageFormat()
            img_format.setName(fname)
            self.cursor.insertImage(img_format)
            self.contents_te.setFocus()
    
    # 231222 추가한 첨부 파일 정보 저장 by 정현아
    def attach_file(self):
        fname,_ = QFileDialog.getOpenFileName(self, '첨부 파일 추가', 'C:/Program Files', '모든 파일(*.*)')
        self.file_path_list.append(fname)
        attach_file = os.path.basename(fname)

        # 231227 카운트가 0일 경우 기존에 존재하는 라벨의 텍스트만 변경
        if self.cnt == 0 :
            self.file_lbl.setText(attach_file)
            self.del_btn_list.append(QPushButton('X'))
            self.del_btn_list[self.cnt].setFixedSize(28, 28)
            self.fileLay.insertWidget(2,self.del_btn_list[self.cnt])
            
        # 231227 카운트가 1이상이면 리스트에 값을 추가하고 레이아웃에 라벨 추가
        elif 0 < self.cnt < 5 and len(self.file_lbl_list) < 5:
            self.file_lbl_list.append(QLabel(attach_file))
            self.del_btn_list.append(QPushButton('X'))
            self.del_btn_list[self.cnt].setFixedSize(28, 28)
            
            self.fileLay.insertWidget(2*self.cnt+1,self.file_lbl_list[self.cnt])
            self.fileLay.insertWidget(2*(self.cnt+1),self.del_btn_list[self.cnt])
        
        elif 0 < self.cnt <5 and len(self.file_lbl_list) ==5:
            self.file_lbl_list[self.cnt].setText(attach_file)
            self.del_btn_list[self.cnt].setVisible(True)
            
        # 첨부파일이 5개 이상일 경우 경고
        elif self.cnt >= 5:
            QMessageBox.warning(self,"파일 첨부 실패","파일을 5개이상 추가하실 수 없습니다.")
            return

        self.del_btn_list[self.cnt].clicked.connect(lambda idx=self.cnt: self.del_attach_file(idx))
        self.cnt +=1
    # 첨부파일 제거 by 정현아
    def del_attach_file(self,index):
        # 첨부된 파일 목록에서 제거
        del self.file_path_list[index]
        
        if self.cnt == 1 :
            # 남아있는 라벨에 문구 설정
            self.file_lbl_list[0].setText("파일은 최대 5개까지 첨부 가능합니다.")

            # 삭제버튼 제거
            self.del_btn_list[0].setVisible(False)
            
        else:
            # 중간 항목을 앞으로 당김
            for i in range(index, self.cnt - 1):
                self.file_lbl_list[i].setText(self.file_lbl_list[i + 1].text())
            
            # 마지막 항목 제거
            last_index = self.cnt - 1
            self.file_lbl_list[last_index].setText("")
            self.del_btn_list[last_index].setVisible(False)
            
        self.cnt -= 1
        
    def setLoadingCursor(self, loading):
        if loading:
            QApplication.setOverrideCursor(Qt.WaitCursor)
        else:
            QApplication.restoreOverrideCursor()
                    
    def closeEvent(self, e): 
        self.closed.emit()
        super().closeEvent(e)

stylesheet = """
    QPushButton{
        border-radius: 5px;
        color: #868686; 
        font-weight: bold;
    }
"""
        
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Write() 
    myWindow.show() 
    app.exec_() 