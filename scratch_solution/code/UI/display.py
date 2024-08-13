##############################################
#                                            #
# DISPLAY of the whole programm              #
# it contains menu with functions and        #
# the drag and drop area to build the circle #
#                                            #
##############################################


from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QFrame

from ..UI.drag_and_drop import DropArea
from ..elements.gatter.parent_gatter import GatterButton

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