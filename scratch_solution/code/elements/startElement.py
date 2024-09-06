######################################
#
#  startpoints where wires can be connected to be ON or OFF
#  this points have the same right click logic like gatter, but cannot be changed in any way
#  the logic to calculate the status of circle starts here
#  there should just exist two elements, one with ON one with off
#  can not be deleted
#
######################################
import time
import threading

from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtCore import Qt, QPoint

from ..helper.functions import globalSimulationRun
from ..helper.global_variables import gatter_color, wireList, startPoints, gateList


class startElement(QLabel):
    counter = 0

    # state can be 0  or 1 / On or off
    # type can be "ON", "OFF" or "CLOCK"
    def __init__(self, parent, state=0, type='OFF', output_wire=[], position_x=100, position_y=0):
        super().__init__(parent)

        startElement.counter += 1
        if startElement.counter > 3:
            QMessageBox.critical(self, "Error", f" To many startElements. Just two are allowed!")

        self.id = state
        self.state = state
        self.outWire = output_wire
        self.setText(type)
        self.type = type
        # dictonary with {wireId: wireElement, ....}
        self.setFixedSize(40, 30)
        self.setStyleSheet(f"background-color: {gatter_color}; border: 1px solid black;")
        self.start_pos = QPoint(0, 0)
        startPoints[self.id] = self
        if self.type == 'CLOCK':
            self.startClock()
            print('clock started')

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

            # if start wire is deleted, set every state of gatter/wire to 0 and calculate again
            # for gateId in list(gateList.keys()):  # Create a list of the keys
            #    gateList[gateId].setState(0)
            # globalSimulationRun()

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
        elif event.button() == Qt.LeftButton:
            print('left clokc start element')
            if self.type == 'ON':
                self.changeType('CLOCK')
            elif self.type == 'OFF':
                self.changeType('ON')
            elif self.type == 'CLOCK':
                self.changeType('OFF')

# move button for the distance between new position and old position
    def move(self, pos):
        super().move(pos - self.start_pos)
        self.start_pos = pos

    def paintEvent(self, event):
        super().paintEvent(event)

    def changeType(self, new_type):
        self.type = new_type
        if self.type == 'ON':
            self.state = 1
        elif self.type == 'OFF':
            self.state = 0
        elif self.type == 'CLOCK':
            self.state = 0
            self.startClock()
        self.setText(self.type)
        for wireId in self.outWire:
            wireList[wireId].setState(self.state)
        self.parent().updateUI()

    def startClock(self):
        print('start clock')
        clock_thread = threading.Thread(target=self.runClock)
        clock_thread.daemon = True  # Ensures the thread will exit when the main program exits
        clock_thread.start()

    def stopClock(self):
        print('something')

    def runClock(self):
        print('run clock', self.state)
        if(self.type == 'CLOCK'):
            self.state = not(self.state)
            time.sleep(1)
            for wireId in self.outWire:
                wireList[wireId].setState(self.state)
            self.parent().updateUI()
            self.runClock()