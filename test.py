from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextBlockFormat
from PyQt5.QtWidgets import QApplication, QTextEdit

app = QApplication([])

textEdit = QTextEdit()
textEdit.setPlainText("This is a sample text.")

# QTextCursor를 이용하여 현재 커서의 위치에 대한 정보를 가져옴
cursor = QTextEdit().textCursor()

# QTextBlockFormat 객체를 생성하고 정렬 설정
blockFormat = QTextBlockFormat()
blockFormat.setAlignment(Qt.AlignCenter)  # 예시로 가운데 정렬을 설정

# QTextCursor를 통해 설정한 QTextBlockFormat을 적용
cursor.setBlockFormat(blockFormat)

# 텍스트 편집기에 설정된 커서를 업데이트
textEdit.setTextCursor(cursor)

textEdit.show()
app.exec_()