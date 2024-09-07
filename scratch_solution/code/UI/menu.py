###########################################
#                                         #
# MENU area to manage config              #
# start and stop the circlecalculation    #
#                                         #
###########################################

import json

from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout, QMessageBox, QFileDialog, QToolTip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .drag_and_drop import DropArea
from ..elements.startElement import startElement
from ..helper.functions import globalSimulationRun
from ..helper.global_variables import wireList, gateList, background_color, gatter_color, startPoints
from ..elements.gatter.parent_gatter import GatterButton
from ..elements.wire import Wire
#from ..elements.gatter.parent_gatter import GatterButton
#from .drag_and_drop import DropArea


class Menu(QFrame):

    ###################  functions   ###########################

    # cerate json out of the global wire and gatter dictionarys and store them in config.json
    def store_config(self):
        # choice path to store file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Config File", "", "JSON Files (*.json);;All Files (*)", options=options)


    # Your logic for storing the config
        print("Config stored successfully!")
        config_gatter = [{'gatterId': id, 'gatter': gate.to_dict()} for id, gate in gateList.items()]
        config_wire = [{'wireId': id, 'wire': wire.to_dict()} for id, wire in wireList.items()]
        config_start_element = [{'eleId': id, 'ele': ele.to_dict()} for id, ele in startPoints.items()]
        config_data = {'gatter': config_gatter, 'wire': config_wire, 'wire_id': Wire.get_counter(), 'gatter_id': GatterButton.get_counter(), 'startElement': config_start_element} # store id counter to prevent id errors when loading config
        try:
            with open(file_path, 'w') as config_file:
                json.dump(config_data, config_file, indent=4)
            QMessageBox.information(self, "Store Config", "Config stored successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to store config: {e}")

    # TODO check if ids are correct, specially if there were gatters before
    def get_config_file(self):
        if (len(wireList) != 0 or len(gateList) != 0):
            # ask user if he want to load config and overwrite existing elements
            reply = QMessageBox.question(self, 'Load configuration',
                                         "Are you sure you want to load this config? Your actual config will be deleted.",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            # Handle the user's response
            if reply == QMessageBox.Yes:
                self.load_config()
            else:
                print("Deletion canceled.")
        else:
            self.load_config()

    def load_config(self):
        # Your logic for loading the config
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Config File", "", "JSON Files (*.json);;All Files (*)", options=options)

        if file_path:
            with open(file_path, 'r') as config_file:
                config_data = json.load(config_file)

            self.delete_config()

            GatterButton.set_counter(config_data['gatter_id'])
            Wire.set_counter(config_data['wire_id'])

            for entry in config_data['gatter']:
                gatter_data = entry['gatter']
                self.dropArea.addGatterButton(gatter_data)

            for entry in config_data['wire']:
                wire_data = entry['wire']
                self.dropArea.addWire(wire_data)

            for entry in config_data['startElement']:
                print(entry)
                startPoints[entry['eleId']].changeType(entry['ele']['type'])

            globalSimulationRun()

            QMessageBox.information(self, "Load Config", f"Config loaded successfully from {file_path}!")

    # run simulation by "updating" every wire that is connected to one of the startpoints, this should trigger the update function of all connected gatter and so on
    def runSimulation(self):
        for id, startPoint in startPoints.items():
            for wireId in startPoint.outWire:
                wireList[wireId].setState(startPoint.getState())

    def delete_config(self):
        if (len(wireList) != 0 or len(gateList) != 0):
            # ask user if he want to load config and overwrite existing elements
            reply = QMessageBox.question(self, 'Delete configuration',
                                 "Are you sure you want to delete the actual config?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            # Handle the user's response
            if reply == QMessageBox.Yes:
                # Clear the existing gateList
                for gateId in list(gateList.keys()):  # Create a list of the keys
                    gate = gateList[gateId]
                    gate.deleteGatter()

                for wireId in list(wireList.keys()):
                    wire = wireList[wireId]
                    wire.deleteWire()

                gateList.clear()
                wireList.clear()
                self.dropArea.update()
                GatterButton.set_counter(0)
                Wire.set_counter(0)
            else:
                print("Deletion canceled.")

    def show_info(self):
        # Display a QMessageBox with information
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Program Info")
        msg.setText(" <b>Gatter:</b> <br> -   Pull gatter from the menu box into the drop area to add them. <br> -   Use middle mouse button to delete a gatter with all its wires. <br><b> Wire: </b> <br> -   Right click on two an existing gatter to create a wire. If you click on the left half it will be the input gatter-point of the wire. Click on the right half of the other gatter to set it as endpoint. <br>  -   Right click on a wire to delete it.<br> <b>Startpoints: </b> <br>-   Change type if startpoint by leftclick. The change order is: OFF - ON - CLOCK")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def __init__(self, parent, drop_area):
        super().__init__(parent)
        self.dropArea = drop_area
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet(f"background-color: {background_color}; color: white")
        self.setFixedSize(400, 50)
        self.source_label = None  # Track the first selected label (source)
        self.source_side = None  # Track whether the source is input or output

        # Use QHBoxLayout to arrange buttons horizontally
        main_layout = QHBoxLayout()

    ###################   buttons  ############################

        storeConfigButton = QPushButton("Store config", self)
        storeConfigButton.clicked.connect(self.store_config)  # Connect to store_config function
        main_layout.addWidget(storeConfigButton)
        # Set custom style using setStyleSheet
        storeConfigButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {gatter_color}; /* white */
                color: black;
                border: none;
                padding: 3px 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                margin: 3px;
                cursor: pointer;
                border-radius: 5px;
                height: 20px;
                width: 100px;
            }}
            QPushButton:hover {{
                background-color: #45a049; /* Darker green */
            }}
            QPushButton:pressed {{
                background-color: #3e8e41; /* Even darker green */
            }}
        """)

        loadConfigButton = QPushButton("Load config", self)
        loadConfigButton.clicked.connect(self.get_config_file)  # Connect to load_config function
        main_layout.addWidget(loadConfigButton)
        # Set custom style using setStyleSheet
        loadConfigButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {gatter_color}; /* white */
                color: black;
                border: none;
                padding: 3px 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                margin: 3px;
                cursor: pointer;
                border-radius: 5px;
                height: 20px;
                width: 100px;
            }}
            QPushButton:hover {{
                background-color: #45a049; /* Darker green */
            }}
            QPushButton:pressed {{
                background-color: #3e8e41; /* Even darker green */
            }}
        """)


    # Out of usage because simulation is running all the time
        '''
        runConfigButton = QPushButton("Run simulation", self)
        runConfigButton.clicked.connect(self.runSimulation)  # Connect to load_config function
        main_layout.addWidget(runConfigButton)
        Set custom style using setStyleSheet
        runConfigButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {gatter_color}; /* white */
                color: black;
                border: none;
                padding: 3px 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                margin: 3px;
                cursor: pointer;
                border-radius: 5px;
                height: 20px;
                width: 100px;
            }}
            QPushButton:hover {{
                background-color: #45a049; /* Darker green */
            }}
            QPushButton:pressed {{
                background-color: #3e8e41; /* Even darker green */
            }}
        """)
'''

        runConfigButton = QPushButton("Delete config", self)
        runConfigButton.clicked.connect(self.delete_config)  # Connect to load_config function
        main_layout.addWidget(runConfigButton)
        # Set custom style using setStyleSheet
        runConfigButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {gatter_color}; /* white */
                color: black;
                border: none;
                padding: 3px 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                margin: 3px;
                cursor: pointer;
                border-radius: 5px;
                height: 20px;
                width: 100px;
            }}
            QPushButton:hover {{
                background-color: #45a049; /* Darker green */
            }}
            QPushButton:pressed {{
                background-color: #3e8e41; /* Even darker green */
            }}
        """)

        info_button = QPushButton("i", self)
        info_button.clicked.connect(self.show_info)
    # TODO tooltip doe snot appear on linux
        info_button.setToolTip("Pull gatter from the menu box into the drop area to add them. \n Right click on two an existing gatter to create a wire. If you click on the left half it will be the input gatter-point of the wire. Click on the right half of the other gatter to set it as endpoint. \n Right clikc on a wire to delete it. \n Use middle mouse button to delete a gatter with all its wires.")
        info_button.setFocusPolicy(Qt.NoFocus)  # Allows tooltip on hover even when button is not focused
        info_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {gatter_color}; /* white */
                color: black;
                border: none;
                padding: 3px 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                margin: 3px;
                cursor: pointer;
                border-radius: 5px;
                height: 20px;
                width: 20;
            }}
            QPushButton:hover {{
                background-color: #45a049; /* Darker green */
            }}
            QPushButton:pressed {{
                background-color: #3e8e41; /* Even darker green */
            }}
        """)
        main_layout.addWidget(info_button)

        # Set layout for the widget
        self.setLayout(main_layout)