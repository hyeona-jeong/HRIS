import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QToolButton, QButtonGroup

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # QButtonGroup 생성
        button_group = QButtonGroup(self)

        # 툴버튼 1
        tool_btn1 = QToolButton()
        tool_btn1.setText('Tool 1')
        tool_btn1.setCheckable(True)
        button_group.addButton(tool_btn1)

        # 툴버튼 2
        tool_btn2 = QToolButton()
        tool_btn2.setText('Tool 2')
        tool_btn2.setCheckable(True)
        button_group.addButton(tool_btn2)

        # 툴버튼 3
        tool_btn3 = QToolButton()
        tool_btn3.setText('Tool 3')
        tool_btn3.setCheckable(True)
        button_group.addButton(tool_btn3)

        # 그룹 내에서 하나만 선택 가능하도록 설정
        button_group.setExclusive(True)
        
        button_group.buttonClicked.connect(self.printBtn)

        vbox.addWidget(tool_btn1)
        vbox.addWidget(tool_btn2)
        vbox.addWidget(tool_btn3)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QButtonGroup with QToolButton Example')
        self.show()
        
    def printBtn(self,Btn):
        print(Btn.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    sys.exit(app.exec_())
