import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt, QMimeData, QPoint, QLineF, QRect
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QPen

# Draggable widget with input and output sides
class DraggableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(100, 50)
        self.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        self.start_pos = QPoint(0, 0)
        self.is_in_drop_area = False

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
        self.lines = []  # Store the lines (connections)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            source = event.source()
            if isinstance(source, DraggableLabel) and not source.is_in_drop_area:
                # Create a new label in the drop area only if it's dragged from outside
                label = DraggableLabel(event.mimeData().text(), self)
                label.move(event.pos())
                label.is_in_drop_area = True
                label.show()
            elif isinstance(source, DraggableLabel) and source.is_in_drop_area:
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

# Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Example with Inputs and Outputs")
        self.setGeometry(100, 100, 500, 500)

        main_layout = QVBoxLayout()

        self.draggable_label = DraggableLabel(" ", self)
        main_layout.addWidget(self.draggable_label)

        self.drop_area = DropArea(self)
        main_layout.addWidget(self.drop_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

# Entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
