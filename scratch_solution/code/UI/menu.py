###########################################
#                                         #
# MENU area to manage config              #
# start and stop the circlecalculation    #
#                                         #
###########################################

import json

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout, QMessageBox, QFileDialog
from ..helper.global_variables import wireList, gateList
from ..elements.gatter.parent_gatter import GatterButton
from .drag_and_drop import DropArea


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
        config_data = {'gatter': config_gatter, 'wire': config_wire}
        try:
            with open(file_path, 'w') as config_file:
                json.dump(config_data, config_file, indent=4)
            QMessageBox.information(self, "Store Config", "Config stored successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to store config: {e}")


    def load_config(self):
        # Your logic for loading the config
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Config File", "", "JSON Files (*.json);;All Files (*)", options=options)

        if file_path:
            with open(file_path, 'r') as config_file:
                config_data = json.load(config_file)

            # Clear the existing gateList
            gateList.clear()
            wireList.clear()
            print(config_data)
            for entry in config_data['gatter']:
                gatter_data = entry['gatter']
                print(gatter_data)
                self.dropArea.addGatterButton(gatter_data)

            QMessageBox.information(self, "Load Config", f"Config loaded successfully from {file_path}!")





    def __init__(self, parent, drop_area):
        super().__init__(parent)
        self.dropArea = drop_area
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: lightgray;")
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
        storeConfigButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 3px 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                margin: 3px;
                cursor: pointer;
                border-radius: 5px;
                height: 20px;
                width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker green */
            }
            QPushButton:pressed {
                background-color: #3e8e41; /* Even darker green */
            }
        """)

        loadConfigButton = QPushButton("Load config", self)
        loadConfigButton.clicked.connect(self.load_config)  # Connect to load_config function
        main_layout.addWidget(loadConfigButton)
        # Set custom style using setStyleSheet
        loadConfigButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 3px 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                margin: 3px;
                cursor: pointer;
                border-radius: 5px;
                height: 20px;
                width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker green */
            }
            QPushButton:pressed {
                background-color: #3e8e41; /* Even darker green */
            }
        """)

        # Set layout for the widget
        self.setLayout(main_layout)
