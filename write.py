import os
import sys
import pymysql

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

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.img_path = []
        self.file_path = []
        self.atch_files = ''
        self.font = QFont("Malgun Gothic", 9)
        self.charFormat = QTextCharFormat()
        self.charFormat.setFont(self.font)
        self.cursor = self.contents_te.textCursor()
        
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
        self.submitBtn.clicked.connect(lambda: self.submit(emp_num=16120105))
        self.image_btn.clicked.connect(self.insert_image)
        self.file_btn.clicked.connect(self.attach_file)
        
    def submit(self, emp_num = 16120105):
        imgs_path = None
        files_path = None
        uploader = UploadFile()
        # 구글드라이브에 이미지 파일 업로드 by 정현아
        if self.img_path:
            imgs_path = ''
            for path in self.img_path:
                img_url = uploader.upload_file(path)
                imgs_path += img_url 
                imgs_path += "," 
        if self.file_path:
            files_path = ''
            for path in self.file_path:
                file_url = uploader.upload_file(path)
                files_path += file_url
                files_path += ","
        if self.atch_files == '':
            self.atch_files = None
        category = self.category_combo.currentText()
        title = self.title_le.text()
        contents = self.contents_te.toHtml()
        conn = pymysql.connect(
                host='localhost',
                user='dev',
                password='nori1234',
                db='dev',
                port=3306,
                charset='utf8'
        )
        cur = conn.cursor()
        query = "SELECT NAME_KOR FROM MAIN_TABLE WHERE EMP_NUM = %s"
        cur.execute(query,(emp_num))
        name = cur.fetchone()
        
        query = "INSERT INTO FORUM(WRITER, TITLE, CATEGORY, CONTENTS, EMP_NUM, ATCH_IMG_PATH, ATCH_FILE_PATH, ATCH_FILE_NAME) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        cur.execute(query, (name, title,category,contents,emp_num, imgs_path, files_path, self.atch_files))
        conn.commit()
        conn.close()
        
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

    def insert_image(self):
        # 231220 File dialog로 이미지 파일을 선택하고 선택한 파일 정보를 읽어옴 by 정현아
        fname,_ = QFileDialog.getOpenFileName(self, '이미지 파일 추가', 'C:/Program Files', '이미지 파일(*.jpg *.gif, *.png)')
        
        self.img_path.append(fname)
        img_format = QTextImageFormat()
        img_format.setName(fname)
        self.cursor.insertImage(img_format)
        
    def attach_file(self):
        fname,_ = QFileDialog.getOpenFileName(self, '이미지 파일 추가', 'C:/Program Files', '모든(*.*)')
        self.file_path.append(fname)
        attach_file = os.path.basename(fname)
        self.atch_files += attach_file
        self.atch_files += ", "
        self.file_lbl.setText(self.atch_files)
        
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Write() 
    myWindow.show() 
    app.exec_() 