import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QButtonGroup

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # QButtonGroup 생성
        button_group = QButtonGroup(self)

        # 라디오 버튼 생성 및 그룹에 추가
        radio_btn1 = QRadioButton('Option 1')
        button_group.addButton(radio_btn1)

        radio_btn2 = QRadioButton('Option 2')
        button_group.addButton(radio_btn2)

        radio_btn3 = QRadioButton('Option 3')
        button_group.addButton(radio_btn3)

        # 그룹 내에서 하나만 선택 가능하도록 설정
        button_group.setExclusive(True)

        # 라디오 버튼의 상태가 변경될 때 호출될 함수 연결
        button_group.buttonClicked.connect(self.on_button_clicked)

        vbox.addWidget(radio_btn1)
        vbox.addWidget(radio_btn2)
        vbox.addWidget(radio_btn3)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QButtonGroup Example')
        self.show()

    def on_button_clicked(self, button):
        print(f'Selected button: {button.text()}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    sys.exit(app.exec_())