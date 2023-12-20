import os
import sys
import pymysql
import smtplib
import string
import random

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('write.ui')
form_class = uic.loadUiType(form)[0]

class Write(QMainWindow, form_class):

    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        font_family = "Malgun Gothic"
        font_size = 9
        self.font = QFont(font_family, font_size)
        self.charFormat = QTextCharFormat()
        self.charFormat.setFont(self.font)
        
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
        
    def submit(self, emp_num = 16120105):
        category = self.category_combo.currentText()
        title = self.title_le.text()
        contents = self.contents_te.toHtml()
        print(emp_num)
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
        
        query = "INSERT INTO FORUM(WRITER, TITLE, CATEGORY, CONTENTS, EMP_NUM) VALUES (%s,%s,%s,%s,%s);"
        cur.execute(query, (name, title,category,contents,emp_num))
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
        # QTextCursor를 이용하여 현재 커서의 위치에 대한 정보를 가져옴
        cursor = self.contents_te.textCursor()
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
        cursor.setBlockFormat(blockFormat)
        self.contents_te.setTextCursor(cursor)
        
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


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    myWindow = Write() 
    myWindow.show() 
    app.exec_() 