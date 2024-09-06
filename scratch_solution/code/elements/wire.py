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

import time
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPainter, QPen

from ..helper.global_variables import wireList, gateList, startPoints
from ..helper.functions import globalSimulationRun


class Wire(QWidget):
    counter = 0
    lines = []

    @classmethod
    def get_counter(cls):
        return cls.counter

    @classmethod
    def set_counter(cls, counter):
        cls.counter = counter

    #  TODO discuss: wires werden immer neu erzeugt und haben damit nur ein gatter, brauchen wir listen oder soll bei
    #  erzeugen eines wires bei einem gatter, welches bereit ein output wire hat dieses verwendet werden und statt ein
    #  neues zu erzeugen einfach bei dem bestehenden wire das zweite endgatter hinzufügen?
    def __init__(self, parent, point1, point2, state=0, endpoint_gate_list=[], startpoint_gate_list=[], connected_to_start_point=False, starelement_point=0, wire_id=None):
        super().__init__(parent)
        #globalSimulationRun()
        if wire_id: # Usefull for laoding configfiles or implementing a "back" button for deleted elements
            # TODO check if wire with this id exist already.
            self.id = wire_id
        else:
            Wire.counter += 1
            self.id = Wire.counter
        print('create wire: ', wire_id, state)
        self.state = state
        self.endpointGateList = endpoint_gate_list
        self.startpointGateList = startpoint_gate_list
        wireList[self.id] = self

        self.point1 = point1
        self.point2 = point2
        self.connectedToStartPoint = connected_to_start_point
        self.startPoint = starelement_point

        self.line = QLineF(point1, point2)
        self.parent = parent

        self.update()


    def getState(self):
        return self.state

    def setState(self, state, force=False):
        print('change wire state', self.id, state, self, force)
        if self.state != state or force:
            self.state = state
            for gatterId in self.endpointGateList:
                gateList[gatterId].updateState()

    def addOutputGate(self, gateId):
        if gateId not in self.endpointGateList:
            self.endpointGateList.append(gateId)

    def removeOutputGate(self, gateId):
        self.endpointGateList.remove(gateId)

    def addInputGate(self, gateId):
        if gateId not in self.startpointGateList:
            self.startpointGateList.append(gateId)

    def removeInputGate(self, gateId):
        if gateId in self.startpointGateList:
            self.startpointGateList.remove(gateId)

    # used if wire connects directly to the startpoints
    def addToStartPointElement(self, startPointId):
        self.connectedToStartPoint = True
        self.startPoint = startPointId

    def updateGates(self):
        for gateId in self.endpointGateList:
            gateList[gateId].update()

    def updateStartPoint(self, newPoint):
        self.line.setP1(newPoint)
        self.point1 = newPoint

    def updateEndPoint(self, newPoint):
        self.line.setP2(newPoint)
        self.point2 = newPoint

    def deleteWire(self):
        for gateId in self.endpointGateList:
            gateList[gateId].deleteInputWire(self.id)
        if self.connectedToStartPoint:
            startPoints[self.startPoint].deleteOutputWire(self.id)
        else:
            for gateId in self.startpointGateList:
                gateList[gateId].deleteOutputWire(self.id)
        wireList.pop(self.id)
        del self

    # write a nice json format to store gatterobject in file
    def to_dict(self):
        return {
            'id': self.id,
            'state': self.state,
            'endpointGates': self.endpointGateList,
            'startpointGates': self.startpointGateList,
            'startPoint_x': self.point1.x(),
            'startPoint_y': self.point1.y(),
            'endPoint_x': self.point2.x(),
            'endPoint_y': self.point2.y(),
            'connectedToStartPoint': self.connectedToStartPoint,
            'startPoint': self.startPoint
        }

    def mousePressEvent(self, event):
        print('clicked wire')
        if event.button() == Qt.LeftButton:
            print('press left on wire')
        elif event.button() == Qt.RightButton:
            print('press right on wire')


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        # Draw all stored lines
        for line in Wire.lines:
            painter.drawLine(line)