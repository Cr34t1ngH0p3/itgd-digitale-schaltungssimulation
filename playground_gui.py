from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel,  QVBoxLayout, QHBoxLayout, QGraphicsLineItem
from PyQt5.QtGui import QPixmap, QColor, QDrag, QPainter, QPen
from PyQt5.QtCore import Qt, QMimeData, pyqtSlot, QPoint, pyqtSignal,QLineF


wireList = {}
gateList = {}
startingPointWire = None
endPointWire = None
class Wire(QWidget):
    counter = 0

    def __init__(self, parent, point1, point2, state=0, out_gate_list={}):
        super().__init__(parent)
        print('created wire')
        print(point1)
        print(point2)
        Wire.counter += 1
        self.id = Wire.counter
        self.state = state
        self.outputGateList = out_gate_list
        wireList[self.id] = self

        self.point1 = point1
        self.point2 = point2


    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def updateGates(self):
        for gate in self.outputGateList:
            gate.update()


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 255), 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(self.point1, self.point2)


class GatterButton(QWidget):
    counter = 0
    inputClickEvent = pyqtSignal()
    outputClickEvent = pyqtSignal()

    def __init__(self, parent, label_text, type_label='-', input_wires={}, output_wire=None):
        super().__init__(parent)

        GatterButton.counter += 1
        self.id = GatterButton.counter
        self.name = label_text
        self.inputWireList = input_wires
        self.outWire = output_wire
        gateList[self.id] = self

        # Main layout for the GatterButton and label
        main_layout = QVBoxLayout(self)

        # Create the label above the GatterButton
        self.main_label = QLabel(self.name, self)
        self.main_label.setAlignment(Qt.AlignCenter)

        # Create a horizontal layout for the two parts of the GatterButton
        button_layout = QHBoxLayout()

        # Create two labels representing parts of the button
        self.inputButton = QPushButton('Manage Inputs', self)
        self.outputButton = QPushButton('Manage Output', self)

        # Add labels to the button layout
        button_layout.addWidget(self.inputButton)
        button_layout.addWidget(self.outputButton)

        # Adjust spacing and margins to minimize gap
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Style the labels to look like button parts
        self.inputButton.setStyleSheet("background-color: lightblue; border: none; border-right: 1px solid gray; padding: 10px;")
        self.outputButton.setStyleSheet("background-color: lightgreen; border: none; padding: 10px;")

        # Add the label and GatterButton to the main layout
        main_layout.addWidget(self.main_label)
        main_layout.addLayout(button_layout)

        # Set the layout and fix the size
        self.setLayout(main_layout)
        self.setFixedSize(self.sizeHint())

        # Connect label click events to the corresponding slots
        self.inputButton.clicked.connect(self.inputClickEventHandler)
        self.outputButton.clicked.connect(self.outputClickEventHandler)

    def addInputWire(self, wireId):
        self.inputWireList[wireId] = wireList[wireId]

    def deleteInputWire(self, wireId):
        self.inputWireList.pop(wireId)

    def inputClickEventHandler(self):
        print('presed input')
        self.inputClickEvent.emit()

    def outputClickEventHandler(self):
        print('pressed output')
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
        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        global startingPointWire
        if event.button() == Qt.LeftButton:
            print(f'{self.inputButton.text()} | {self.outputButton.text()} pressed')
        if event.button() == Qt.RightButton:
            if (startingPointWire == None):
                print(self.inputButton.text())
                print(self.x())
                print(self.y())
                startingPointWire = QPoint(self.x() + self.width(), self.y() + self.height() // 2)
            else:
                print('endpint')
                endPointWire = QPoint(self.x(), self.y() + self.height() // 2)
                app.addWire(startingPointWire, endPointWire)
                startingPointWire = None
                endPointWire = None
                # TODO warning if same gatter

class AndButton(GatterButton):
    def __init__(self, parent, name, _out=None, _inList={}):
        super().__init__(parent, name, '&')
        self.out = _out
        self.inputWireList = _inList
        self.update()
        #self.inputButton.text('AND')

    def update(self):
        for wire in self.inputWireList:
            if (wire.getState() == 0):
                self.outWire.setState(0)
                return
        if (self.outWire):
            self.outWire.setState(1)

class OrButton(GatterButton):
    def __init__(self, _out, _inList, name):
        super().__init__(name, '&')
        self.out = _out
        self.inputWireList = _inList
        self.update()
        self.inputButton.text('OR')

    def update(self):
        for wire in self.inputWireList:
            if (wire.getState() == 1):
                self.outWire.setState(1)
                return
        self.outWire.setState(0)

class Application(QWidget):

    def __init__(self):
        super().__init__()

        self.shadow = None  # Shadow widget placeholder
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        main_layout = QVBoxLayout(self)

        self.button1 = GatterButton(self,'Part 1', 'Part 2', None, None)
        self.button1.setObjectName('button1')
        self.button1.move(100, 65)

        self.button1.inputClickEvent.connect(lambda: print("Label 1 Clicked"))
        self.button1.outputClickEvent.connect(lambda: print("Label 2 Clicked"))

        self.button2 = AndButton(self, 'Button 2 Label')
        self.button2.setObjectName('button2')
        self.button2.move(100, 150)

        self.button2.inputClickEvent.connect(lambda: print("Label 1 Clicked"))
        self.button2.outputClickEvent.connect(lambda: print("Label 2 Clicked"))
#
        point1 = QPoint(50, 50)
        point2 = QPoint(200, 200)

        # Create the widget
        self.addWire(point1, point2)

        # Set main layout
        self.setLayout(main_layout)
        self.setGeometry(300, 300, 400, 300)

    def addWire(self, start_point, end_point):
        if self.wire:
            self.wire.deleteLater()  # Remove the existing wire if any
        self.wire = Wire(self, start_point, end_point)
        self.wire.setGeometry(self.rect())
        self.wire.lower()  # Move the wire behind other widgets

    def startDrag(self, widget, event):
        # Create a shadow widget to show where the button will land
        self.shadow = GatterButton(self, widget.inputButton.text(), widget.outputButton.text(), widget.main_label.text(), None)
        self.shadow.setStyleSheet("background-color: rgba(128, 100, 100, 0.5);")  # Semi-transparent shadow
        self.shadow.inputButton.setStyleSheet("background-color: rgba(128, 100, 100, 0.5); padding: 10px;")  # Semi-transparent shadow
        self.shadow.outputButton.setStyleSheet("background-color: rgba(128, 100, 100, 0.5); padding: 10px;")  # Semi-transparent shadow
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