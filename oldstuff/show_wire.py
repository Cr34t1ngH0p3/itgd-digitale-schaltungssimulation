from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint

class LineWidget(QWidget):
    def __init__(self, point1, point2, parent=None):
        super().__init__(parent)
        self.point1 = point1
        self.point2 = point2

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 255), 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(self.point1, self.point2)

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        # Create and configure layout
        main_layout = QVBoxLayout(self)

        # Create buttons
        self.button1 = QPushButton('Button 1', self)
        self.button1.move(100, 65)
        self.button1.setFixedSize(100, 40)
        main_layout.addWidget(self.button1)

        self.button2 = QPushButton('Button 2', self)
        self.button2.move(200, 65)
        self.button2.setFixedSize(100, 40)
        main_layout.addWidget(self.button2)

        # Create a LineWidget
        point1 = self.button1.pos() + QPoint(self.button1.width() // 2, self.button1.height() // 2)
        point2 = self.button2.pos() + QPoint(self.button2.width() // 2, self.button2.height() // 2)

        self.line_widget = LineWidget(point1, point2, self)
        self.line_widget.setGeometry(self.rect())  # Set geometry to match the parent widget
        self.line_widget.show()

        # Set main layout
        self.setLayout(main_layout)
        self.setGeometry(300, 300, 400, 300)

def main():
    app = QApplication([])
    ex = Application()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()
