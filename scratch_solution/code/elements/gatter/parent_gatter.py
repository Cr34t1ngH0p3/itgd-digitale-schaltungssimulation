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

from ...helper.global_variables import wireList, gateList, button_color
from ...helper.functions import globalSimulationRun

# Draggable widget with input and output sides
class GatterButton(QLabel):
    counter = 0
    inputClickEvent = pyqtSignal()
    outputClickEvent = pyqtSignal()

    @classmethod
    def get_counter(cls):
        return cls.counter

    @classmethod
    def set_counter(cls, counter):
        cls.counter = counter

    # TODO, use self.start_position when creating object, right now we need to use self.move after every creation
    def __init__(self, parent, text, input_wires=[], output_wire=[], position_x=100, position_y=0, is_in_drop_area=False, gatter_id=None):
        super().__init__(text, parent)
        if gatter_id: # Usefull for laoding configfiles or implementing a "back" button for deleted elements
            # TODO check if wire with this id exist already in gatelist.
            self.id = gatter_id
        else:
            GatterButton.counter += 1
            self.id = GatterButton.counter
        self.name = text
        self.inputWireList = input_wires
        self.outWire = output_wire # dictonary with {wireId: wireElement, ....}
        self.setFixedSize(100, 50)
        self.setStyleSheet(f"background-color: {button_color}; border: 1px solid black;")
        self.start_pos = QPoint(0, 0)
        # self.start_pos = QPoint(position_x, position_y) # set it always to 0,0
        self.is_in_drop_area = is_in_drop_area
        self.outputValue = 0
        if self.is_in_drop_area:
            gateList[self.id] = self

    # get actual state
    def getState(self):
        return self.outputValue

    # set actual state
    def setState(self, state):
        self.outputValue = state
        self.informWireAboutState()

    def informWireAboutState(self):
        for wireId in self.outWire:
            wireList[wireId].setState(self.outputValue)

    # tell gatter that the wire is connected
    # tell the wire that its endpoint is connected to this input
    def addInputWire(self, wireId):
        if wireId not in self.inputWireList:
            self.inputWireList.append(wireId)
        if wireList[wireId]:
            wireList[wireId].addOutputGate(self.id)
        self.updateState()


    # delete the wire from self-inputlist and tell wire it got disconnected
    def deleteInputWire(self, wireId):
        self.inputWireList.remove(wireId)
        if wireList[wireId]:
            wireList[wireId].removeOutputGate(self.id)
        self.updateState()

    def addOutputWire(self, wireId):
        if wireId not in self.outWire:
            self.outWire.append(wireId)
        if wireList[wireId]:
            wireList[wireId].addInputGate(self.id)

    def deleteOutputWire(self, wireId):
        self.outWire.remove(wireId)
        if wireList[wireId]:
            wireList[wireId].removeInputGate(self.id)

    def inputClickEventHandler(self):
        self.inputClickEvent.emit()

    def outputClickEventHandler(self):
        self.outputClickEvent.emit()

    # calculate new wire points and update each connected wire
    def updateWirePosition(self):
        newButtonOutPoint = QPoint(self.x() + self.width(), self.y() + self.height() // 2 ) # outputwire are in the half of the right border -> change point of "wire.startpoint"
        newButtonStartPoint = QPoint(self.x(), self.y() + self.height() // 2 ) # inputwire are at the half of the left border -> change point of "wire.endpoint"
        for wireId in self.outWire:
            wireList[wireId].updateStartPoint(newButtonOutPoint)
        for wireId in self.inputWireList:
            wireList[wireId].updateEndPoint(newButtonStartPoint)

    # write a nice json format to store gatterobject in file
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'inputWireList': self.inputWireList,
            'outWire': self.outWire,
            'position_x': self.start_pos.x(),
            'position_y': self.start_pos.y(),
        }

    # if button pressed with right click there is the option to create a new wire to an other gatter
    def mousePressEvent(self, event):
        #from scratch_solution.UI.drag_and_drop import DropArea
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos() # store start (acual position before move)
        elif event.button() == Qt.RightButton:
            # Determine if the click was on the input or output side
           # if isinstance(self.parent(), DropArea):
            if event.pos().x() < self.width() // 2:
                # Clicked on the input side
                self.parent().label_clicked(self, "input")
            else:
                # Clicked on the output side
                self.parent().label_clicked(self, "output")
        elif event.button() == Qt.MiddleButton:
            self.deleteGatter()
            self.update()

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

    # move button for the distance between new position and old position
    def move(self, pos):
        super().move(pos - self.start_pos)
        self.start_pos = pos

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
        painter.drawText(QRect(mid_x, 0, self.width() - mid_x, self.height()), Qt.AlignCenter, f"OUT: {self.outputValue}")

    def updateState(self):
        return

    def deleteGatter(self):
        inputWireListLength = len(self.inputWireList)
        wireListLength = len(list(wireList.keys()))

        wireListBuffer = wireList
        inputWireListBuffer = self.inputWireList

        keyToDelete = []

        for inputWireId in range(inputWireListLength):
            for wireListId in range(wireListLength):
                if list(wireListBuffer.keys())[wireListId] == inputWireListBuffer[inputWireId]:
                    temp = inputWireListBuffer[inputWireId]
                    keyToDelete.append(temp)

        for key in keyToDelete:
            if key in wireList and wireList[key]:
                wireList[key].deleteWire()


        outWireListLength = len(self.outWire)
        wireListLength = len(list(wireList.keys()))

        wireListBuffer = wireList
        outWireListBuffer = self.outWire

        keyToDelete = []

        for outWireId in range(outWireListLength):
            for wireListId in range(wireListLength):
                if list(wireListBuffer.keys())[wireListId] == outWireListBuffer[outWireId]:
                    temp = outWireListBuffer[outWireId]
                    keyToDelete.append(temp)

        for key in keyToDelete:
            wireList[key].deleteWire()

        gateList.pop(self.id)
        self.parent().updateUI()
        self.hide()

        self.deleteLater()
        self.setParent(None)

        del self


        #globalSimulationRun()



