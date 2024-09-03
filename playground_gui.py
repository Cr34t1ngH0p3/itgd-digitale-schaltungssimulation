import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt, QMimeData, QPoint, QLineF, QRect, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QPen, QColor
from math import sqrt

wireList = {}
gateList = {}
startingPointWire = None
endPointWire = None

class Wire(QWidget):
    counter = 0
    lines = []
    def __init__(self, parent, point1, point2, state=0, endpoint_gate_list={}, startpoint_gate_list={}):
        super().__init__(parent)
        print('created wire')
        print(point1)
        print(point2)
        Wire.counter += 1
        self.id = Wire.counter
        self.state = state
        self.endpointGateList = endpoint_gate_list
        self.startpointGateList = startpoint_gate_list
        wireList[self.id] = self

        self.point1 = point1
        self.point2 = point2

        self.line = QLineF(point1, point2)

        self.update()


    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def addOutputGate(self, gateId):
        self.endpointGateList[gateId] = gateList[gateId]

    def removeOutputGate(self, gateId):
        self.endpointGateList.pop(gateId)

    def addInputGate(self, gateId):
        self.startpointGateList[gateId] = gateList[gateId]

    def removeInputGate(self, gateId):
        self.startpointGateList.pop(gateId)

    def updateGates(self):
        for gateId in self.endpointGateList:
            gateList[gateId].update()

    def updateStartPoint(self, newPoint):
        self.line.setP1(newPoint)
        self.update()

    def updateEndPoint(self, newPoint):
        self.line.setP2(newPoint)
        self.update()

    def deleteWire(self):
        for gateId, gateItem in list(self.endpointGateList.items()):
            gateItem.deleteInputWire(self.id)
        for gateId, gateItem in list(self.startpointGateList.items()):
            gateItem.deleteOutputWire(self.id)
        wireList.pop(self.id)
        print('del wire')
        del self

    def mousePressEvent(self, event):
        print('clicked wire')
        if event.button() == Qt.LeftButton:
            print('press left on wire')
        elif event.button() == Qt.RightButton:
            print('press right on wire')


    def paintEvent(self, event):
        print('Paitn event')
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        # Draw all stored lines
        for line in Wire.lines:
            print('paint line')
            painter.drawLine(line)

# Draggable widget with input and output sides
class GatterButton(QLabel):
    counter = 0
    inputClickEvent = pyqtSignal()
    outputClickEvent = pyqtSignal()

    def __init__(self, parent, text, input_wires={}, output_wire={}):
        super().__init__(text, parent)

        GatterButton.counter += 1
        self.id = GatterButton.counter
        print('New gatter id:', self.id)

        self.name = text
        self.inputWireList = input_wires
        self.outWire = output_wire # dictonary with {wireId: wireElement, ....}

        self.setFixedSize(100, 50)
        self.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        self.start_pos = QPoint(0, 0)
        self.is_in_drop_area = False
        gateList[self.id] = self


    def addInputWire(self, wireId):
        print('addInputWire')
        print(self.pos())
        print(self.id)
        self.inputWireList[wireId] = wireList[wireId]
        wireList[wireId].addOutputGate(self.id)

    def deleteInputWire(self, wireId):
        print('delete InputWire')
        print(self.id)
        print(wireId)
        print(len(self.inputWireList))
        self.inputWireList.pop(wireId)
        wireList[wireId].removeOutputGate(self.id)

    def addOutputWire(self, wireId):
        print('gatter id')
        print(self.id)
        print('addOutputWire')
        print(wireId)
        print(wireList[wireId])
        self.outWire[wireId] = wireList[wireId]
        wireList[wireId].addInputGate(self.id)


    def deleteOutputWire(self, wireId):
        print('deleteOutpuWire')
        print(self.id)
        print(wireId)
        print(len(self.outWire))
        self.outWire.pop(wireId)
        wireList[wireId].removeInputGate(self.id)


    def inputClickEventHandler(self):
        print('presed input')
        self.inputClickEvent.emit()

    def outputClickEventHandler(self):
        print('pressed output')
        self.outputClickEvent.emit()

    def updateWirePosition(self):
        print(self.pos())
        print(self.x())
        newButtonOutPoint = QPoint(self.x() + self.width(), self.y() + self.height() // 2 )
        newButtonStartPoint = QPoint(self.x(), self.y() + self.height() // 2 )
        print('update wires')
        print(len(self.inputWireList))
        for wireId, outputWire in self.outWire.items():
            print('updated endpoint')
            print(wireId)
            outputWire.updateStartPoint(newButtonOutPoint)
        for wireId, inputWire in self.inputWireList.items():
            print('updated endpoint')
            print(wireId)
            inputWire.updateEndPoint(newButtonStartPoint)

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
    def __init__(self, name, _out=None, _inList={}):
        super().__init__(name)
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
        super().__init__(name)
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

# Droppable area with connection handling
class DropArea(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: lightgray;")
        self.setFixedSize(400, 400)
        self.source_label = None  # Track the first selected label (source)
        self.source_side = None  # Track whether the source is input or output
        self.wires = []  # Store the lines (connections)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            source = event.source()
            if isinstance(source, GatterButton) and not source.is_in_drop_area:
                # Create a new label in the drop area only if it's dragged from outside
                print(event.mimeData())
                label = GatterButton(self, event.mimeData().text(), {}, {})
                label.move(event.pos())
                label.is_in_drop_area = True
                label.show()
            elif isinstance(source, GatterButton) and source.is_in_drop_area:
                # Move the label within the drop area
                print('drop stuff')
                print(event)
                print(source.pos())
                print(event.pos())
              #  newButtonStartPoint = QPoint(event.pos())
              #  newButtonOutPoint =
                source.move(event.pos())
                print(source.pos())
                print('outwire')
                print(source.outWire)
                print('inputwire')
                print(source.inputWireList)
                print('-----')
                source.updateWirePosition()

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
        newWire = Wire(self, source_in_drop, destination_in_drop, 0,{}, {})
        print('start')
        print(source.pos())
        print('dest')
        print(destination.pos())
        source.addOutputWire(newWire.id)
        destination.addInputWire(newWire.id)
        if source.inputWireList is destination.inputWireList:
            print("source and destination have the same inputWireList reference!")
        else:
            print("source and destination have different inputWireList references.")
        print('+++')
        print(source.inputWireList)
        print('+++')
        print(destination.outWire)

    #line = QLineF(source_in_drop, destination_in_drop)
        self.wires.append(newWire)
        self.update()  # Trigger a repaint to draw the new line

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        # Draw all stored lines
        for wire in self.wires:
            painter.drawLine(wire.line)

    def mousePressEvent(self, event):
        print('mouse rpessed')
        if event.button() == Qt.RightButton:
            for wire in self.wires[:]:
                if is_point_on_line(wire.line, event.pos()):
                    print("Point is on the line!")
                    wire.deleteWire()
                    self.wires.remove(wire)
                    self.update()
                else:
                    print("Point is not on the line.")

# Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Example with Inputs and Outputs")
        self.setGeometry(100, 100, 500, 500)

        main_layout = QVBoxLayout()

        self.draggable_label = GatterButton(self, " ")
        main_layout.addWidget(self.draggable_label)

        self.drop_area = DropArea(self)
        main_layout.addWidget(self.drop_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

def distance_to_line_segment(line, point):
    """
    Calculate the shortest distance from a point to a line segment.

    :param line: QLineF object representing the line segment.
    :param point: QPointF object representing the point.
    :return: The shortest distance from the point to the line segment.
    """
    x1, y1 = line.p1().x(), line.p1().y()
    x2, y2 = line.p2().x(), line.p2().y()
    px, py = point.x(), point.y()

    # Calculate the line segment vector
    line_vec_x = x2 - x1
    line_vec_y = y2 - y1

    # Calculate the vector from the point to the line's start point
    point_vec_x = px - x1
    point_vec_y = py - y1

    # Calculate the projection of the point vector onto the line vector
    line_len_sq = line_vec_x ** 2 + line_vec_y ** 2
    if line_len_sq == 0:
        return sqrt(point_vec_x ** 2 + point_vec_y ** 2)  # Start and end points are the same

    t = (point_vec_x * line_vec_x + point_vec_y * line_vec_y) / line_len_sq

    # Clamp the projection to the segment
    t = max(0, min(1, t))

    # Find the closest point on the line segment
    closest_x = x1 + t * line_vec_x
    closest_y = y1 + t * line_vec_y

    # Calculate the distance from the point to the closest point on the line segment
    dist_x = px - closest_x
    dist_y = py - closest_y

    return sqrt(dist_x ** 2 + dist_y ** 2)

def is_point_on_line(line, point, tolerance=10.0):
    """
    Check if a point is close enough to a line to be considered as 'clicked' on it.

    :param line: QLineF object representing the line.
    :param point: QPointF object representing the point (click position).
    :param tolerance: Distance tolerance to determine if the point is on the line.
    :return: True if point is within tolerance distance from the line, otherwise False.
    """
    distance = distance_to_line_segment(line, point)
    return distance <= tolerance

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
