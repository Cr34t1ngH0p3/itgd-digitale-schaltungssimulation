###########################################
#                                         #
# MENU area to manage config              #
# start and stop the circlecalculation    #
#                                         #
###########################################

import json

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout, QMessageBox, QFileDialog

from .drag_and_drop import DropArea
from ..elements.startElement import startElement
from ..helper.functions import globalSimulationRun
from ..helper.global_variables import wireList, gateList, background_color, button_color, startPoints
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
        config_data = {'gatter': config_gatter, 'wire': config_wire, 'wire_id': Wire.get_counter(), 'gatter_id': GatterButton.get_counter()} # store id counter to prevent id errors when loading config
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
            GatterButton.set_counter(config_data['gatter_id'])
            Wire.set_counter(config_data['wire_id'])

            for entry in config_data['gatter']:
                gatter_data = entry['gatter']
                self.dropArea.addGatterButton(gatter_data)

            for entry in config_data['wire']:
                wire_data = entry['wire']
                self.dropArea.addWire(wire_data)

            globalSimulationRun()

            QMessageBox.information(self, "Load Config", f"Config loaded successfully from {file_path}!")


    # run simulation by "updating" every wire that is connected to one of the startpoints, this should trigger the update function of all connected gatter and so on
    # TODO 1.check for circle, 2.run again if something changes, 3.maybe do continues updates (like a ticke rate)
    def runSimulation(self):
        for id, startPoint in startPoints.items():
            for wireId in startPoint.outWire:
                wireList[wireId].setState(id)


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
                background-color: {button_color}; /* white */
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
                background-color: {button_color}; /* white */
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

        runConfigButton = QPushButton("Run simulation", self)
        runConfigButton.clicked.connect(self.runSimulation)  # Connect to load_config function
        main_layout.addWidget(runConfigButton)
        # Set custom style using setStyleSheet
        runConfigButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_color}; /* white */
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

        # Set layout for the widget
        self.setLayout(main_layout)