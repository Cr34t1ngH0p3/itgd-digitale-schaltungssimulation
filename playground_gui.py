from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QWidget, QLabel,  QVBoxLayout, QHBoxLayout, QGraphicsLineItem
from PyQt5.QtGui import QPixmap, QColor, QDrag, QPainter, QPen
from PyQt5.QtCore import Qt, QMimeData, pyqtSlot, QPoint, pyqtSignal, QLineF, QRect


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

    def __init__(self, label_text, type_label='-', input_wires={}, output_wire=None, parent=None):
        super().__init__(label_text, parent)

        GatterButton.counter += 1
        self.id = GatterButton.counter
        self.name = label_text
        self.inputWireList = input_wires
        self.outWire = output_wire
        gateList[self.id] = self

        self.setFixedSize(100, 50)
        self.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        self.start_pos = QPoint(0, 0)
        self.is_in_drop_area = False

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
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.setHotSpot(event.pos() - self.rect().topLeft())

            if self.is_in_drop_area:
                drag.exec_(Qt.MoveAction)
            else:
                drag.exec_(Qt.CopyAction)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
        elif event.button() == Qt.RightButton:
            # Determine if the click was on the input or output side
            if isinstance(self.parent(), DropArea):
                if event.pos().x() < self.width() // 2:
                    # Clicked on the input side
                    self.parent().label_clicked(self, "input")
                else:
                    # Clicked on the output side
                    self.parent().label_clicked(self, "output")
    def move(self, pos):
        super().move(pos - self.start_pos)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # Draw the division between input and output sides
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        mid_x = self.width() // 2
        painter.drawLine(mid_x, 0, mid_x, self.height())

        # Label the sides (optional)
        painter.drawText(QRect(0, 0, mid_x, self.height()), Qt.AlignCenter, "IN")
        painter.drawText(QRect(mid_x, 0, self.width() - mid_x, self.height()), Qt.AlignCenter, "OUT")

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

class DropArea(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: lightgray;")
        self.setFixedSize(400, 400)
        self.source_label = None  # Track the first selected label (source)
        self.source_side = None  # Track whether the source is input or output
        self.lines = []  # Store the lines (connections)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            source = event.source()
            if isinstance(source, GatterButton) and not source.is_in_drop_area:
                # Create a new label in the drop area only if it's dragged from outside
                label = GatterButton(event.mimeData().text(), self)
                label.move(event.pos())
                label.is_in_drop_area = True
                label.show()
            elif isinstance(source, GatterButton) and source.is_in_drop_area:
                # Move the label within the drop area
                source.move(event.pos())

            self.update()  # Update the widget to redraw lines
            event.acceptProposedAction()

    def label_clicked(self, label, side):
        if self.source_label is None:
            if side == "output":
                # Select the first label (source) only if it's the output side
                self.source_label = label
                self.source_side = side
                self.source_label.setStyleSheet("background-color: yellow; border: 1px solid black;")
        else:
            if side == "input" and label != self.source_label:
                # Connect only if the second label's side is input and it's a different label
                self.draw_line(self.source_label, label)
                self.source_label.setStyleSheet("background-color: lightblue; border: 1px solid black;")
                self.source_label = None  # Reset the selection
                self.source_side = None

    def draw_line(self, source, destination):
        # Calculate global positions
        source_pos = source.mapToGlobal(source.rect().center())
        destination_pos = destination.mapToGlobal(destination.rect().center())
        # Adjust for input/output sides
        source_pos.setX(source.mapToGlobal(QPoint(source.width(), source.height() // 2)).x())  # Output side
        destination_pos.setX(destination.mapToGlobal(QPoint(0, destination.height() // 2)).x())  # Input side
        # Map global positions to DropArea coordinates
        source_in_drop = self.mapFromGlobal(source_pos)
        destination_in_drop = self.mapFromGlobal(destination_pos)
        line = QLineF(source_in_drop, destination_in_drop)
        self.lines.append(line)
        self.update()  # Trigger a repaint to draw the new line

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        # Draw all stored lines
        for line in self.lines:
            painter.drawLine(line)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Example with Inputs and Outputs")
        self.setGeometry(100, 100, 500, 500)

        main_layout = QVBoxLayout()

        self.draggable_label = GatterButton("Hi", self)
        main_layout.addWidget(self.draggable_label)

        self.drop_area = DropArea(self)
        main_layout.addWidget(self.drop_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    import sys
    main()