######################################
#
#  startpoints where wires can be connected to be ON or OFF
#  this points have the same right click logic like gatter, but cannot be changed in any way
#  the logic to calculate the status of circle starts here
#  there should just exist two elements, one with ON one with off
#  can not be deleted
#
######################################
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtCore import Qt, QPoint

from ..helper.global_variables import button_color, wireList, startPoints


class startElement(QLabel):
    counter = 0


    def __init__(self, parent, state=0, output_wire=[], position_x=100, position_y=0):
        super().__init__(parent)

        startElement.counter += 1
        if startElement.counter > 2:
            QMessageBox.critical(self, "Error", f" To many startElements. Just two are allowed!")

        self.id = state
        self.state = state
        self.outWire = output_wire
        self.setText('ON' if state else 'OFF')
        # dictonary with {wireId: wireElement, ....}
        self.setFixedSize(40, 30)
        self.setStyleSheet(f"background-color: {button_color}; border: 1px solid black;")
        self.start_pos = QPoint(0, 0)
        startPoints[self.id] = self

    # get actual state
    def getState(self):
        return self.state

    def addOutputWire(self, wireId):
        self.outWire.append(wireId)
        if wireList[wireId]:
            wireList[wireId].addToStartPointElement(self.id)

    def deleteOutputWire(self, wireId):
        self.outWire.remove(wireId)
        if wireList[wireId]:
            wireList[wireId].removeInputGate(self.id)

    # write a nice json format to store gatterobject in file
    def to_dict(self):
        return {
            'id': self.id,
            'state': self.state,
            'outWire': self.outWire,
            'position_x': self.start_pos.x(),
            'position_y': self.start_pos.y(),
        }
    # if button pressed with right click there is the option to create a new wire to an other gatter
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
                self.parent().label_clicked(self, "output")


    # move button for the distance between new position and old position
    def move(self, pos):
        super().move(pos - self.start_pos)
        self.start_pos = pos

    def paintEvent(self, event):
        super().paintEvent(event)
