from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPdfWriter, QPagedPaintDevice, QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import sys
import random
 
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
 
class MyWidget(QWidget):
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        vbox = QVBoxLayout()
 
        # 테이블 위젯생성(더미 데이터 용)
        self.table = QTableWidget(self)
        self.table.setRowCount(10)
        self.table.setColumnCount(3)
        col = ['first', 'second', 'third']
        self.table.setHorizontalHeaderLabels(col)
        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                self.table.setItem(r, c, QTableWidgetItem(str(random.randint(1,100))))
 
        # 버튼 생성
        self.btn = QPushButton('Print PDF File', self)
        self.btn.clicked.connect(self.btnClick)
 
        self.btn2 = QPushButton('Make PDF file', self)
        self.btn2.clicked.connect(self.btnClick2)
 
        # 컨트롤들 박스 레이아웃 배치
        vbox.addWidget(self.table)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.btn2)
        self.setLayout(vbox)
        self.resize(600,400)
 
    def btnClick(self):
        # 프린터 생성, 실행
        printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QDialog.Accepted:
            # Painter 생성
            qp = QPainter()
            qp.begin(printer)        
 
            # 여백 비율
            wgap = printer.pageRect().width()*0.1
            hgap = printer.pageRect().height()*0.1
 
            # 화면 중앙에 위젯 배치
            xscale = (printer.pageRect().width()-wgap)/self.table.width()
            yscale = (printer.pageRect().height()-hgap)/self.table.height()
            scale = xscale if xscale < yscale else yscale        
            qp.translate(printer.paperRect().x() + printer.pageRect().width()/2, printer.paperRect().y() + printer.pageRect().height()/2)
            qp.scale(scale, scale)
            qp.translate(-self.table.width()/2, -self.table.height()/2);        
 
            # 인쇄
            self.table.render(qp)
 
            qp.end()       
 
    def btnClick2(self):
        # pdf 생성
        pdf = QPdfWriter('test.pdf')
        pdf.setPageSize(QPagedPaintDevice.A4)
 
        # 화면 캡쳐        
        screen = QApplication.primaryScreen()
        img = screen.grabWindow(self.winId(), 0,0, self.rect().width(),self.rect().height())
 
        # 3항 연산자 (a if test else b, 만약 test가 참이면 a, 아니면 b)
        # 이미지 크기는 큰 값 기준, PDF 크기는 작은값 기준(화면 초과 방지)
        img_size = img.width() if img.width()-img.height() > 0 else img.height()
        pdf_size = pdf.width() if pdf.width()-pdf.height() < 0 else pdf.height()
 
        # 최적 비율 얻기
        ratio = pdf_size / img_size
         
        # pdf에 쓰기
        qp = QPainter()
        qp.begin(pdf)
        qp.drawPixmap(0, 0, img.width()*ratio, img.height()*ratio, img)
        qp.end()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())