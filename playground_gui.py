from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel,  QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QDrag
from PyQt5.QtCore import Qt, QMimeData, pyqtSlot, QPoint


class SplitButton(QWidget):

    def __init__(self, text1, text2, parent=None):
        super().__init__(parent)

        # Set layout and labels
        layout = QHBoxLayout(self)
        self.label1 = QLabel(text1, self)
        self.label2 = QLabel(text2, self)

        layout.addWidget(self.label1)
        layout.addWidget(self.label2)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Styling the labels to look like a button
        self.label1.setStyleSheet("background-color: lightblue; border-right: 1px solid gray; padding: 5px;")
        self.label2.setStyleSheet("background-color: lightgreen; padding: 5px;")

        # Set the layout and make it tight
        self.setLayout(layout)
        self.setFixedSize(self.sizeHint())

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        mimeData = QMimeData()
        mimeData.setText(self.objectName())

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            print(f'{self.label1.text()} | {self.label2.text()} pressed')


class Application(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        self.button1 = SplitButton('Part 1', 'Part 2', self)
        self.button1.setObjectName('button1')
        self.button1.move(100, 65)

        self.button2 = SplitButton('Left', 'Right', self)
        self.button2.setObjectName('button2')
        self.button2.move(100, 150)

        self.setGeometry(300, 300, 400, 300)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        button_name = event.mimeData().text()
        button = self.findChild(QWidget, button_name)
        if button:
            button.move(position)
        event.accept()


def main():
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    app.exec_()


if __name__ == '__main__':

    import sys
    main()()