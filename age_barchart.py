import sys
import matplotlib.pyplot as plt
import pymysql
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.figure import Figure
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog


class Age_barchart(QMainWindow):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        conn = pymysql.connect(
            host='localhost',
            user='dev',
            password='nori1234',
            db='dev',
            port=3306,
            charset='utf8'
            )
        cur = conn.cursor()
        query= """
        select ages, count(a.ages) from 
        (select floor(age/10)*10 as ages from main_table) as a
        group by ages
        order by ages
        """
        cur.execute(query)
        result = cur.fetchall()
        ages = {}   
        for rank in result :     
            ages[str(rank[0])+'대'] = rank[1]
            
        years = list(ages.keys())
        values = list(ages.values())
            
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.main_widget)
        vbox.addWidget(self.canvas)
        
        plt.rcParams['font.family'] ='Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] =False

        self.ax = self.canvas.figure.subplots()
        self.ax.bar(years, values)
        
        self.printBtn = QPushButton("인쇄")
        self.printBtn.setFixedSize(98,28)
        
        self.cnlBtn = QPushButton("닫기")
        self.cnlBtn.setFixedSize(98,28)
        
        hs1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hs2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addItem(hs1)
        hbox.addWidget(self.printBtn)
        hbox.addWidget(self.cnlBtn)
        hbox.addItem(hs2)
        
        self.printBtn.clicked.connect(self.print)
        
        self.setWindowTitle('   ')
        self.setGeometry(600, 200, 1200, 800)
        self.show()
        
    def print(self):
        # 프린터 생성, 실행
        printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QDialog.Accepted:
            # Painter 생성
            qp = QPainter()
            qp.begin(printer)        
 
            # 여백 비율(프린터의 )
            wgap = printer.pageRect().width()*0.1
            hgap = printer.pageRect().height()*0.1
            
            # 화면 중앙에 위젯 배치
            xscale = (printer.pageRect().width()-wgap)/self.canvas.width()
            yscale = (printer.pageRect().height()-hgap)/self.canvas.height()
            scale = xscale if xscale < yscale else yscale        
            qp.translate(printer.paperRect().x() + printer.pageRect().width()/2, printer.paperRect().y() + printer.pageRect().height()/2)
            qp.scale(scale, scale)
            qp.translate(-self.canvas.width()/2, -self.canvas.height()/2)     
 
            # 인쇄
            self.canvas.render(qp)
            
            qp.end()
            
    # 231122 닫기 클릭시 이전 페이지로 넘어가기 위해 close이벤트 재정의 by정현아
    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = Age_barchart()
  sys.exit(app.exec_())