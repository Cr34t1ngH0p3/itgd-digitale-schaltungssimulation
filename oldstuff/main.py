# This code was written with the help of:
# https://pyqtgraph.readthedocs.io/en/latest/api_reference/flowchart/index.html


import sys

import pyqtgraph.flowchart.Terminal
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsLineItem
from PyQt5.uic import loadUi
import pyqtgraph as pg
from pyqtgraph.flowchart.Terminal import ConnectionItem
from pyqtgraph.flowchart.Terminal import TerminalGraphicsItem
from pyqtgraph.flowchart import Terminal
from pyqtgraph.flowchart import Flowchart, Node
import pyqtgraph.flowchart.library as fclib

from pyqtgraph import GraphicsObject


# import AND gate logic from module
from module import AND
# import NAND gate logic from module
from module import NAND
# import OR gate logic from module
from module import OR


connection = []

class Main(QMainWindow):

    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        loadUi('interface.ui', self)
        self.setWindowTitle('Circuit Simulator')

        # To begin, you must decide what the input and output variables will be for your flowchart.
        # Create a flowchart with one terminal defined for each variable:
        self.fc = Flowchart(terminals={
            'INPUT_TRUE': {'io': 'in'},
            'INPUT_FALSE': {'io': 'in'},
            'OUTPUT1': {'io': 'out'},
            'OUTPUT2': {'io': 'out'}
        })


        ##############################################################################
        # After implementing a new Node subclass, you want to register the class
        # so that it appears in the menu of Nodes the user can select from:
        # import pyqtgraph.flowchart.library as fclib
        # fclib.registerNodeType(SpecialFunctionNode, [('Category', 'Sub-Category')])
        # The second argument to registerNodeType is a list of tuples, with each
        # tuple describing a menu location in which SpecialFunctionNode should appear.
        ##############################################################################

        # adding custom flowchart node class 'ANDPort' (defined below) to the Flowchart Library (fclib) so we can use it
        fclib.registerNodeType(ANDPort, [('Gates',)])
        # adding custom flowchart node class 'NANDPort' (defined below) to the Flowchart Library (fclib) so we can use it
        fclib.registerNodeType(NANDPort, [('Gates',)])
        # adding custom flowchart node class 'ORPort' (defined below) to the Flowchart Library (fclib) so we can use it
        fclib.registerNodeType(ORPort, [('Gates',)])


        ##############################################################################
        # Once the flowchart is created, add its control widget to your application.
        # The control widget provides several features:
        # - displays a list of all nodes in the flowchart containing the control widget for each node
        # - provides access to the flowchart design window via the 'flowchart' button
        # - interface for saving/restoring flowcharts to disk
        ##############################################################################

        # The flowchart returns a widget controller (with flowchart save buttons), which are added to self.canvas
        diagram_controller = self.fc.widget()
        # self.canvas is a QVBoxLayout that was prev added in Qt Designer and named 'canvas' (see .ui file in Qt Designer)
        self.canvas.addWidget(diagram_controller)

        # setting some static inputs in flowchart for later use to set Logic Ports
        self.fc.setInput(INPUT_TRUE=True)
        self.fc.setInput(INPUT_FALSE=False)



##############################################################################################################################
# A node subclass implements:
# 1. list of input/output terminals and their properties
# 2. process() function which takes the names of the input terminals as keyword arguments and
#    returns a dict with the names of output terminals as keys
##############################################################################################################################

class CustomTerminal(Terminal):
    def __init__(self, node, name, **opts):
        super().__init__(node, name, **opts)

class ANDPort(pg.flowchart.Node):

    # this is a custom class for our logic gates, 
    # it subclasses pg.flowchart.Node and 
    # overrides the process method, 
    # because there we need to map how the values are calculated and applied to our library module
    nodeName = 'AND'

    # all nodes are provided a unique name when they are created
    def __init__(self, name, **kwags):
        super().__init__(name, **kwags)
        # instantiation of the AND gate from our library
        self.port_object = AND(name)
        # returns a dictionary with a definition of inputs/outputs
        self.port_metadata = self.port_object.getDefinition()

        # self.terminals object to pass to Node.__init__ later using the port_metadata to pass necessary data
        self.terminals = {}
        for input_port in self.port_metadata['inputs']:
            self.terminals[input_port] = {'io': 'in'}

        for output_port in self.port_metadata['outputs']:
            self.terminals[output_port] = {'io': 'out'}

        # self.terminals will just be:
        # {
        #   'A' : {'io': 'in'},
        #   'B' : {'io': 'in'},
        #   'X' : {'io': 'out'}
        # }        

        # initialize with a dict describing the I/O terminals on this node
        Node.__init__(self, name, terminals = self.terminals)

    def addTerminal(self, name, **opts):
        """Add a new terminal to this Node with the given name. Extra
        keyword arguments are passed to Terminal.__init__.

        Causes sigTerminalAdded to be emitted."""
        name = self.nextTerminalName(name)
        term = CustomTerminal(self, name, **opts)
        self.terminals[name] = term
        if term.isInput():
            self._inputs[name] = term
        elif term.isOutput():
            self._outputs[name] = term
        self.graphicsItem().updateTerminals()
        self.sigTerminalAdded.emit(self, term)
        return term




    ###############################################################################
    # Process data through this node. This method is called any time the flowchart
    # wants the node to process data. It will be called with one keyword argument
    # corresponding to each input terminal, and must return a dict mapping the name
    # for each output terminal to its new value.
    ###############################################################################

    # whenever something on the flowchart is changed, the process() method is called for all nodes
    # used to recalculate the port values
    def process(self, **kwds):
        # Get current input values applied to the Node
        # inputValues() returns a dict of all input values currently assigned to this node
        input_dict = self.inputValues()
        # input_dict will return something like: {'A' : True, 'B' : False} (or None values if not connected yet)

        # conversion of input_dict to a list of booleans, because that is what library requires in setInputs()
        input_vector = [value for key, value in input_dict.items()] # creates [True, False] from above dictionary

        # Now apply the inputs to the port_object (which is the AND Gate) from library (setInputs) which takes the boolean list
        self.port_object.setInputs(input_vector)

        # return value is a dict with one key per output terminal
        # So: return a dictionary which as key has the name of the output port ('X') 
        # and as value the return value of the port_object function evaluateOutputs()
        return {self.port_metadata['outputs'][0]: self.port_object.evaluateOutputs()}

    # def graphicsItem(self):
    #     """Return the GraphicsItem for this node. Subclasses may re-implement
    #     this method to customize their appearance in the flowchart."""
    #     if self._graphicsItem is None:
    #         self._graphicsItem = NodeGraphicsItem(self)
    #     return self._graphicsItem

    def connected(self, localTerm, remoteTerm):
        print('connected')



###################################################################################################################################################


class NANDPort(pg.flowchart.Node):

    nodeName = 'NAND'

    def __init__(self, name):

        self.port_object = NAND(name)
        self.port_metadata = self.port_object.getDefinition()

        self.terminals = {}
        for input_port in self.port_metadata['inputs']:
            self.terminals[input_port] = {'io': 'in'}

        for output_port in self.port_metadata['outputs']:
            self.terminals[output_port] = {'io': 'out'}

        # self.terminals will just be:
        # {
        #   'A' : {'io': 'in'},
        #   'B' : {'io': 'in'},
        #   'X' : {'io': 'out'}
        # }        

        # initialize with a dict describing the I/O terminals on this node
        Node.__init__(self, name, terminals = self.terminals)


    ###############################################################################
    # Process data through this node. This method is called any time the flowchart
    # wants the node to process data. It will be called with one keyword argument
    # corresponding to each input terminal, and must return a dict mapping the name
    # for each output terminal to its new value.
    ###############################################################################

    # whenever something on the flowchart is changed, the process() method is called for all nodes
    # used to recalculate the port values
    def process(self, **kwds):
        # Get current input values applied to the Node
        # inputValues() returns a dict of all input values currently assigned to this node
        input_dict = self.inputValues()
        # input_dict will return something like: {'A' : True, 'B' : False} (or None values if not connected yet)

        # conversion of input_dict to a list of booleans, because that is what library requires in setInputs()
        input_vector = [value for key, value in input_dict.items()] # creates [True, False] from above dictionary

        # Now apply the inputs to the port_object (which is the NAND Gate) from library (setInputs) which takes the boolean list
        self.port_object.setInputs(input_vector)

        # return value is a dict with one key per output terminal
        # So: return a dictionary which as key has the name of the output port ('X') 
        # and as value the return value of the port_object function evaluateOutputs()
        return {self.port_metadata['outputs'][0]: self.port_object.evaluateOutputs()}

    # def graphicsItem(self):
    #     """Return the GraphicsItem for this node. Subclasses may re-implement
    #     this method to customize their appearance in the flowchart."""
    #     if self._graphicsItem is None:
    #         self._graphicsItem = NodeGraphicsItem(self)
    #     return self._graphicsItem


#############################################################################################################################################


class ORPort(pg.flowchart.Node):

    nodeName = 'OR'

    def __init__(self, name):

        self.port_object = OR(name)
        self.port_metadata = self.port_object.getDefinition()

        self.terminals = {}
        for input_port in self.port_metadata['inputs']:
            self.terminals[input_port] = {'io': 'in'}

        for output_port in self.port_metadata['outputs']:
            self.terminals[output_port] = {'io': 'out'}

        # self.terminals will just be:
        # {
        #   'A' : {'io': 'in'},
        #   'B' : {'io': 'in'},
        #   'X' : {'io': 'out'}
        # }        

        # initialize with a dict describing the I/O terminals on this node
        Node.__init__(self, name, terminals = self.terminals)


    ###############################################################################
    # Process data through this node. This method is called any time the flowchart
    # wants the node to process data. It will be called with one keyword argument
    # corresponding to each input terminal, and must return a dict mapping the name
    # for each output terminal to its new value.
    ###############################################################################

    # whenever something on the flowchart is changed, the process() method is called for all nodes
    # used to recalculate the port values
    def process(self, **kwds):
        # Get current input values applied to the Node
        # inputValues() returns a dict of all input values currently assigned to this node
        input_dict = self.inputValues()
        # input_dict will return something like: {'A' : True, 'B' : False} (or None values if not connected yet)

        # conversion of input_dict to a list of booleans, because that is what library requires in setInputs()
        input_vector = [value for key, value in input_dict.items()] # creates [True, False] from above dictionary

        # Now apply the inputs to the port_object (which is the OR Gate) from library (setInputs) which takes the boolean list
        self.port_object.setInputs(input_vector)

        # return value is a dict with one key per output terminal
        # So: return a dictionary which as key has the name of the output port ('X') 
        # and as value the return value of the port_object function evaluateOutputs()
        return {self.port_metadata['outputs'][0]: self.port_object.evaluateOutputs()}

    # def graphicsItem(self):
    #     """Return the GraphicsItem for this node. Subclasses may re-implement
    #     this method to customize their appearance in the flowchart."""
    #     if self._graphicsItem is None:
    #         self._graphicsItem = NodeGraphicsItem(self)
    #     return self._graphicsItem




app = QApplication(sys.argv)
window = Main()
window.show()
app.exec()
