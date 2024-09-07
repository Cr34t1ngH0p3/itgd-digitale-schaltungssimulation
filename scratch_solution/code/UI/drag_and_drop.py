#######################################################
#
# DRAGandDROP here you can build your cirle by moving
#
########################################################


from PyQt5.QtWidgets import QFrame, QMessageBox
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor
from prompt_toolkit.shortcuts import button_dialog

from ..elements.gatter.and_gatter import AndButton
from ..elements.gatter.not_gatter import NotButton
from ..elements.gatter.or_gatter import OrButton
from ..elements.gatter.parent_gatter import GatterButton
from ..elements.startElement import startElement
from ..helper.global_variables import wireList, gateList, gatter_color, background_color, startPoints, \
    active_wire_color, droparea_width, droparea_height
from ..helper.functions import is_point_on_line
from ..elements.wire import Wire
from ..helper.functions import globalSimulationRun

# Droppable area with connection handling
class DropArea(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet(f"background-color: {background_color};")
        self.setFixedSize(droparea_width, droparea_height)
        self.source_label = None  # Track the first selected label (source)
        self.source_side = None  # Track whether the source is input or output

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        gatter = None
        if event.mimeData().hasText():
            source = event.source()
            if isinstance(source, GatterButton) and not source.is_in_drop_area:
                # Create a new gatter in the drop area only if it's dragged from outside
                if isinstance(source, AndButton):
                    gatter = AndButton(parent=self, name="&", inList=[], outList=[], start_pos=source.getStartPos(), is_in_drop_area=True)
                elif isinstance(source, OrButton):
                    gatter = OrButton(parent=self, name="|", inList=[], outList=[], start_pos=source.getStartPos(), is_in_drop_area=True)
                elif isinstance(source, NotButton):
                    gatter = NotButton(parent=self, name="-", inList=[], outList=[], start_pos=source.getStartPos(), is_in_drop_area=True)
                else:
                    QMessageBox.critical(self, "Error", f"Source does not match any instance type.")
                gatter.create_move(event.pos()) # event.pos is where my mouse is, left corner of gatter will appear there
                gatter.is_in_drop_area = True
                gatter.show() # display the new gatter
            elif isinstance(source, GatterButton) and source.is_in_drop_area:
                # Move the label within the drop area
                source.move(event.pos())
                source.updateWirePosition()

        self.update()  # Update the widget to redraw lines
        event.acceptProposedAction()

        #globalSimulationRun()

    # if gatter is clicked you can create a new wire between two gatters
    def label_clicked(self, label, side):
        print("label clicked")
        print(side)
        if side == "output":
            if self.source_label is not None: # input side got pressed before -> draw line
                if self.source_side == "output" or self.source_label == label: # got pressed before -> overwrite source
                    self.source_label.setStyleSheet(f"background-color: {gatter_color}; border: 1px solid black;") # set color back of old pressed gatter
                    self.source_label = label
                    self.source_label.setStyleSheet("background-color: yellow; border: 1px solid black;")
                elif self.source_side == "input": # draw line
                    self.draw_line(label, self.source_label)
                    self.source_label.setStyleSheet(f"background-color: {gatter_color}; border: 1px solid black;")
                    self.source_label = None  # Reset the selection
                    self.source_side = None
            else: # nothing pressed before, mark source
                self.source_label = label
                self.source_label.setStyleSheet("background-color: yellow; border: 1px solid black;")
                self.source_side = side
        elif side == "input":
            if self.source_label != None: # input side got pressed before -> draw line
                if self.source_side == "input" or self.source_label == label: # got pressed before -> overwrite source
                    self.source_label.setStyleSheet(f"background-color: {gatter_color}; border: 1px solid black;") # set color back of old pressed gatter
                    self.source_label = label
                    self.source_label.setStyleSheet("background-color: green; border: 1px solid black;")
                elif self.source_side == "output": # draw line
                    self.draw_line(self.source_label, label)
                    self.source_label.setStyleSheet(f"background-color: {gatter_color}; border: 1px solid black;")
                    self.source_label = None  # Reset the selection
                    self.source_side = None
            else: # nothing pressed before, mark source
                self.source_label = label
                self.source_label.setStyleSheet("background-color: green; border: 1px solid black;")
                self.source_side = side
        else:
            print("pressed side is not defined: " + side)


    def updateUI(self):
        self.update()

    def checkIfGatterWasPressed(self, gatter):
        if self.source_label is gatter:
            self.source_label = None
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
        # create new wire
        newWire = Wire(self, source_in_drop, destination_in_drop, source.getState(),[], [])
        # add wire to the two gates
        source.addOutputWire(newWire.id)
        destination.addInputWire(newWire.id)
        self.update()  # Trigger a repaint to draw the new line

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(gatter_color), 3)
        pen_active = QPen(QColor(active_wire_color), 3)
        painter.setPen(pen)

        # Draw all stored lines
        for wireId, wire in wireList.items():
            if (wire.getState()):
                painter.setPen(pen_active)
                painter.drawLine(wire.line)
            else:
                painter.setPen(pen)
                painter.drawLine(wire.line)

    # mouse press on the droparea, if it is near a wire and it was a right click, this wire gets deleted
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            for wireId, wire in list(wireList.items()):
                if is_point_on_line(wire.line, event.pos()):
                    wire.deleteWire()
                    self.update()

    # creates a gatterbutton and adds it to the UI
    def addGatterButton(self, gatter_data):
        gatter = None
        if gatter_data['name'] == '&':
            gatter = AndButton(parent=self, name=gatter_data['name'], inList=gatter_data['inputWireList'], outList=gatter_data['outWire'], is_in_drop_area=False, gatter_id=gatter_data['id'])
        elif gatter_data['name'] == '|':
            gatter = OrButton(parent=self, name=gatter_data['name'], inList=gatter_data['inputWireList'], outList=gatter_data['outWire'], is_in_drop_area=False, gatter_id=gatter_data['id'])
        elif gatter_data['name'] == '-':
            gatter = NotButton(parent=self, name=gatter_data['name'], inList=gatter_data['inputWireList'], outList=gatter_data['outWire'], is_in_drop_area=False, gatter_id=gatter_data['id'])
        gatter.is_in_drop_area = True
        print('create button after loading: ', gatter_data["id"], gatter_data['position_x'], gatter_data['position_y'])
        gatter.move(QPoint(gatter_data['position_x'], gatter_data['position_y']))
        gateList[gatter.id] = gatter
        gatter.show()

    # creates a gatterbutton and adds it to the UI
    def addWire(self, wire_data):
        print(wire_data['state'])
        wire = Wire(self, QPoint(wire_data['startPoint_x'], wire_data['startPoint_y']), QPoint(wire_data['endPoint_x'],
                    wire_data['endPoint_y']), wire_data['state'], wire_data['endpointGates'], wire_data['startpointGates'], wire_data['connectedToStartPoint'], wire_data['startPoint'], wire_data['id'])
        wireList[wire.id] = wire
        if wire_data['connectedToStartPoint']:
            startPoints[wire_data['startPoint']].addOutputWire(wire.id)
        else:
            gateList[wire_data['startpointGates'][0]].addOutputWire(wire.id) # right now there are just one gatter per endpoint, see #TODO in wireclass
        gateList[wire_data['endpointGates'][0]].addInputWire(wire.id) # right now there are just one gatter per endpoint, see #TODO in wireclass
        self.update()

    def addStartButton(self, state, type, position_x, position_y):
        startPoint = startElement(self, state, type, [])
        startPoint.move(QPoint(position_x, position_y))
        startPoint.show()
