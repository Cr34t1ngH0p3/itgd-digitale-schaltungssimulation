#####################################################################################
#                                                                                   #
# GATTER get a list of input wires and calculate of their states an output value    #
# at the inputpoint the endpoints of wires ends                                     #
# at the outputpoint the startpoints of wires are connected                         #
# all gates are stored globally
# if a gate is moved, the position of the connected wire move with it
# to create a wire between to gatter right-click on out and then on in of the other #
#                                                                                   #
#####################################################################################


from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QMimeData, QPoint, QRect, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QPen

from ...helper.global_variables import wireList, gateList

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

    # tell gatter that the wire is connected
    # tell the wire that its endpoint is connected to this input
    def addInputWire(self, wireId):
        self.inputWireList[wireId] = wireList[wireId]
        wireList[wireId].addOutputGate(self.id)

    def deleteInputWire(self, wireId):
        self.inputWireList.pop(wireId)
        wireList[wireId].removeOutputGate(self.id)

    def addOutputWire(self, wireId):
        self.outWire[wireId] = wireList[wireId]
        wireList[wireId].addInputGate(self.id)

    def deleteOutputWire(self, wireId):
        self.outWire.pop(wireId)
        wireList[wireId].removeInputGate(self.id)

    def inputClickEventHandler(self):
        self.inputClickEvent.emit()

    def outputClickEventHandler(self):
        self.outputClickEvent.emit()

    # calculate new wire points and update each connected wire
    def updateWirePosition(self):
        newButtonOutPoint = QPoint(self.x() + self.width(), self.y() + self.height() // 2 )
        newButtonStartPoint = QPoint(self.x(), self.y() + self.height() // 2 )
        for wireId, outputWire in self.outWire.items():
            outputWire.updateStartPoint(newButtonOutPoint)
        for wireId, inputWire in self.inputWireList.items():
            inputWire.updateEndPoint(newButtonStartPoint)

    def mousePressEvent(self, event):
        #from scratch_solution.UI.drag_and_drop import DropArea
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
        elif event.button() == Qt.RightButton:
            # Determine if the click was on the input or output side
           # if isinstance(self.parent(), DropArea):
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
