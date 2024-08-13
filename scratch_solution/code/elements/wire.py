#####################################################################################
#                                                                                   #
# WIRE are used to transport a change state from one gatter to the next.            #
# endpoints of a wire will end at the input of a gatter                             #
# the startpoints will end at the output of a gatter                                #
# wires are stored global, each wire has a list of its startgatter and end gatter   #
# each wire has a state of ON(1) or OFF(2)                                          #
# we calculate if a wire is clicked in DropArea                                     #
#                                                                                   #
#####################################################################################

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPainter, QPen

from ..helper.global_variables import wireList, gateList

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
