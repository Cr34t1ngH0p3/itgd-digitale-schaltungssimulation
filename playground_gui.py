from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal

class SplitButton(QWidget):
    inputClickEvent = pyqtSignal()
    outputClickEvent = pyqtSignal()

    def __init__(self, text1, text2, label_text, parent=None):
        super().__init__(parent)

        # Main layout for the SplitButton and label
        main_layout = QVBoxLayout(self)

        # Create the label above the SplitButton
        self.main_label = QPushButton(label_text, self)
        self.main_label.setStyleSheet("background-color: lightgray;")
        self.main_label.setEnabled(False)  # Make the label non-clickable

        # Create a horizontal layout for the two parts of the SplitButton
        button_layout = QHBoxLayout()

        # Create two buttons representing parts of the split button
        self.inputButton = QPushButton(text1, self)
        self.outputButton = QPushButton(text2, self)

        # Add buttons to the button layout
        button_layout.addWidget(self.inputButton)
        button_layout.addWidget(self.outputButton)

        # Adjust spacing and margins to minimize gap
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Style the buttons to look like button parts
        self.inputButton.setStyleSheet("background-color: lightblue; border-right: 1px solid gray;")
        self.outputButton.setStyleSheet("background-color: lightgreen;")

        # Add the label and SplitButton to the main layout
        main_layout.addWidget(self.main_label)
        main_layout.addLayout(button_layout)

        # Set the layout and fix the size
        self.setLayout(main_layout)
        self.setFixedSize(self.sizeHint())

        # Connect button click events to the corresponding slots
        self.inputButton.clicked.connect(self.inputClickEventHandler)
        self.outputButton.clicked.connect(self.outputClickEventHandler)

    def inputClickEventHandler(self):
        self.inputClickEvent.emit()

    def outputClickEventHandler(self):
        self.outputClickEvent.emit()

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        mimeData = QMimeData()
        mimeData.setText(self.objectName())

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        self.parent().startDrag(self, event)
        drag.exec_(Qt.MoveAction)

class Application(QWidget):

    def __init__(self):
        super().__init__()

        self.shadow = None  # Shadow widget placeholder
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        self.button1 = SplitButton('Part 1', 'Part 2', 'Button 1 Label')
        self.button1.setObjectName('button1')
        self.button1.move(100, 65)

        # Connect button click signals to slots
        self.button1.inputClickEvent.connect(lambda: print("Button 1 Part 1 Clicked"))
        self.button1.outputClickEvent.connect(lambda: print("Button 1 Part 2 Clicked"))

    #    self.button2 = AndButton('Button 2 Label')
    #    self.button2.setObjectName('button2')
    #    self.button2.move(100, 150)

        #self.button2.inputClickEvent.connect(lambda: print("Label 1 Clicked"))
 #       self.button2.outputClickEvent.connect(lambda: print("Label 2 Clicked"))
#
       # self.point1 = QPoint(50, 50)
       # self.point2 = QPoint(200, 200)

        # Create the widget
#        self.widget = Wire(self.point1, self.point2)

        self.setGeometry(300, 300, 400, 300)

    def startDrag(self, widget, event):
        # Create a shadow widget to show where the button will land
        self.shadow = SplitButton(widget.inputButton.text(), widget.outputButton.text(), widget.main_label.text(), self)
        self.shadow.setStyleSheet("background-color: rgba(128, 100, 100, 0.5);")  # Semi-transparent shadow
        self.shadow.inputButton.setStyleSheet("background-color: rgba(128, 100, 100, 0.5);")  # Semi-transparent shadow
        self.shadow.outputButton.setStyleSheet("background-color: rgba(128, 100, 100, 0.5);")  # Semi-transparent shadow
        self.shadow.resize(widget.size())
        self.shadow.show()

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        # Update shadow widget position
        if self.shadow:
            position = event.pos() - self.shadow.rect().center()
            self.shadow.move(position)
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        button_name = event.mimeData().text()
        button = self.findChild(QWidget, button_name)
        if button:
            # Calculate the offset to center the button under the mouse pointer
            button_center_offset = button.rect().center()
            new_position = position - button_center_offset
            button.move(new_position)

        # Hide and delete the shadow widget
        if self.shadow:
            self.shadow.hide()
            self.shadow.deleteLater()
            self.shadow = None

        event.accept()

def main():
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    import sys
    main()
