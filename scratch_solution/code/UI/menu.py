###########################################
#                                         #
# MENU area to manage config              #
# start and stop the circlecalculation    #
#                                         #
###########################################

from PyQt5.QtWidgets import QFrame, QPushButton, QVBoxLayout


class Menu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: lightgray;")
        self.setFixedSize(300, 50)
        self.source_label = None  # Track the first selected label (source)
        self.source_side = None  # Track whether the source is input or output
        main_layout = QVBoxLayout()

        storeConfigButton = QPushButton("Store config", self)
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
                margin: 10px 10px;
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

        loadConfigButton= QPushButton("Load config", self)
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
                margin: 10px 10px;
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