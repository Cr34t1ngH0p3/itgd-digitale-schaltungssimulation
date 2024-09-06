##############################################
#                                            #
# DISPLAY of the whole programm              #
# it contains menu with functions and        #
# the drag and drop area to build the circle #
#                                            #
##############################################


from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt

from ..UI.drag_and_drop import DropArea
from ..UI.menu import Menu
from ..elements.gatter.not_gatter import NotButton
from ..elements.gatter.or_gatter import OrButton
from ..elements.gatter.and_gatter import AndButton
from ..helper.global_variables import isTic, seconds
from ..helper.functions import globalSimulationRun

# Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Schaltkreissimulation")
        self.setGeometry(100, 100, 500, 500)

        #Tic creation
        if (isTic):
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.tick_function)
            self.timer.start(seconds)

        main_layout = QVBoxLayout()

        drop_area = DropArea(self)
        menu = Menu(self, drop_area) # give drop_area as argument to menu so it can create objets ther, (maybe store drop_area in a different variable?)

        main_layout.addWidget(menu)

        # create ON and OFF startpoint
        self.createStartPoints(drop_area)

        self.createGatterButton(main_layout)

        main_layout.addWidget(drop_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def tick_function(self):
        globalSimulationRun()

    # there should only exist one with ON and one with OFF
    def createStartPoints(self, drop_area):
        drop_area.addStartButton(1, 'ON', 0, 200)
        drop_area.addStartButton(0, 'OFF', 0, 150)
        drop_area.addStartButton(0, 'CLOCK', 0, 100)

    def createGatterButton(self, main_layout):
        # Create a horizontal layout
        button_layout = QHBoxLayout()

        # Create the buttons
        self.and_button = AndButton(parent=self, name="&")
        self.or_button = OrButton(parent=self, name="|")
        self.nor_button = NotButton(parent=self, name="-")

        # Add the buttons to the horizontal layout
        button_layout.addWidget(self.and_button)
        button_layout.addWidget(self.or_button)
        button_layout.addWidget(self.nor_button)

        # Set spacing between the buttons (padding)
        button_layout.setSpacing(50)  # 10 pixels of space between buttons

        # Align the buttons to the right
        button_layout.setAlignment(Qt.AlignLeft)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(button_layout)