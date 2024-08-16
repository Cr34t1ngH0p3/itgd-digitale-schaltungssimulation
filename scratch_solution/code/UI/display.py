##############################################
#                                            #
# DISPLAY of the whole programm              #
# it contains menu with functions and        #
# the drag and drop area to build the circle #
#                                            #
##############################################


from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton

from ..UI.drag_and_drop import DropArea
from ..UI.menu import Menu
from ..elements.gatter.or_gatter import OrButton
from ..elements.gatter.and_gatter import AndButton

# Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Example with Inputs and Outputs")
        self.setGeometry(100, 100, 500, 500)

        main_layout = QVBoxLayout()

        drop_area = DropArea(self)
        menu = Menu(self, drop_area) # give drop_area as argument to menu so it can create objets ther, (maybe store drop_area in a different variable?)

        main_layout.addWidget(menu)

        self.and_button = AndButton(parent=self, name="&") # "parent" button from which copys can be drag and dropped into the area to create a new one
        self.or_button = OrButton(parent=self, name="|") # "parent" button from which copys can be drag and dropped into the area to create a new one
        main_layout.addWidget(self.and_button)
        main_layout.addWidget(self.or_button)

        main_layout.addWidget(drop_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)