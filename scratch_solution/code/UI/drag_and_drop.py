#######################################################
#
# DRAGandDROP here you can build your cirle by moving
#
########################################################


from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor

from ..elements.gatter.and_gatter import AndButton
from ..elements.gatter.or_gatter import OrButton
from ..elements.gatter.parent_gatter import GatterButton
from ..elements.startElement import startElement
from ..helper.global_variables import wireList, gateList, button_color, background_color, startPoints
from ..helper.functions import is_point_on_line
from ..elements.wire import Wire

# Droppable area with connection handling
class DropArea(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet(f"background-color: {background_color};")
        self.setFixedSize(400, 400)
        self.source_label = None  # Track the first selected label (source)
        self.source_side = None  # Track whether the source is input or output

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            source = event.source()
            if isinstance(source, GatterButton) and not source.is_in_drop_area:
                # Create a new gatter in the drop area only if it's dragged from outside
                if isinstance(source, AndButton):
                    gatter = AndButton(parent=self, name="&", inList=[], outList=[], position_x=event.pos().x(), position_y=event.pos().y(), is_in_drop_area=True)
                else:
                    gatter = OrButton(parent=self, name="|", inList=[], outList=[], position_x=event.pos().x(), position_y=event.pos().y(), is_in_drop_area=True)
                gatter.move(event.pos())
                gatter.is_in_drop_area = True
                gatter.show() # display the new gatter
            elif isinstance(source, GatterButton) and source.is_in_drop_area:
                # Move the label within the drop area
                source.move(event.pos())
                source.updateWirePosition()

        self.update()  # Update the widget to redraw lines
        event.acceptProposedAction()

    # if gatter is clicked you can create a new wire between two gatters
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
                self.source_label.setStyleSheet(f"background-color: {button_color}; border: 1px solid black;")
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
        # create new wire
        newWire = Wire(self, source_in_drop, destination_in_drop, 0,[], [])
        # add wire to the two gates
        source.addOutputWire(newWire.id)
        destination.addInputWire(newWire.id)
        self.update()  # Trigger a repaint to draw the new line

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(button_color), 3)
        painter.setPen(pen)

        # Draw all stored lines
        for wireId, wire in wireList.items():
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
        gatter = GatterButton(self, gatter_data['name'], gatter_data['inputWireList'], gatter_data['outWire'], gatter_data['position_x'], gatter_data['position_y'])
        gatter.is_in_drop_area = True
        gatter.move(QPoint(gatter_data['position_x'], gatter_data['position_y']))
        gateList[gatter.id] = gatter
        gatter.show()

    # creates a gatterbutton and adds it to the UI
    def addWire(self, wire_data):
        wire = Wire(self, QPoint(wire_data['startPoint_x'], wire_data['startPoint_y']), QPoint(wire_data['endPoint_x'],
                    wire_data['endPoint_y']), wire_data['state'], wire_data['startpointGates'], wire_data['endpointGates'], wire_data['connectedToStartPoint'], wire_data['startPoint'])
        wireList[wire.id] = wire
        if wire_data['connectedToStartPoint']:
            startPoints[wire_data['startPoint']].addOutputWire(wire.id)
        else:
            gateList[wire_data['startpointGates'][0]].addOutputWire(wire.id) # right now there are just one gatter per endpoint, see #TODO in wireclass
        gateList[wire_data['endpointGates'][0]].addInputWire(wire.id) # right now there are just one gatter per endpoint, see #TODO in wireclass
        self.update()

    def addStartButton(self, state, position_x, position_y):
        startPoint = startElement(self, state, [])
        startPoint.move(QPoint(position_x, position_y))
        startPoint.show()
