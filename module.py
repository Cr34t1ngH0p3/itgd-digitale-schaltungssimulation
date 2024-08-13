
import numpy as np
import string


class OR(object):

    def __init__(self, name, nr_inputs=2):
        self.name = name
        self.nr_inputs = 2
        self.input_vector = [None for i in range(self.nr_inputs)]
        self.output_vector = [None]
        
    def setInputs(self, input_vector):
        self.input_vector = input_vector
        print("{} Set OR Port inputs to: {}".format(self.name, input_vector))
        return True
        
    def evaluateOutputs(self):
        self.output_vector[0] = np.logical_or(*self.input_vector)
        print("{} Output evaluates to: {}".format(self.name, self.output_vector[0]))
        return self.output_vector[0]
        
    def getDefinition(self):
        # returns   {
        #                'name' : 'NAND',
        #                'inputs' : ['A', 'B'],
        #                'outputs' : ['X']
        #            }
        return {'name': self.name, 'inputs': [string.ascii_uppercase[idx] for idx in range(self.nr_inputs)], 'outputs': ['X']}


class NAND(object):

    def __init__(self, name, nr_inputs=2):
        self.name = name
        self.nr_inputs = 2
        self.input_vector = [None for i in range(self.nr_inputs)]
        self.output_vector = [None]
        
    def setInputs(self, input_vector):
        self.input_vector = input_vector
        print("{} Set NAND Port inputs to: {}".format(self.name, input_vector))
        return True
        
    def evaluateOutputs(self):
        self.output_vector[0] = np.logical_not(np.logical_and(*self.input_vector))
        print("{} Output evaluates to: {}".format(self.name, self.output_vector[0]))
        return self.output_vector[0]
        
    def getDefinition(self):
        # returns   {
        #                'name' : 'NAND',
        #                'inputs' : ['A', 'B'],
        #                'outputs' : ['X']
        #            }
        return {'name': self.name, 'inputs': [string.ascii_uppercase[idx] for idx in range(self.nr_inputs)], 'outputs': ['X']}


class AND(object):

    def __init__(self, name, nr_inputs=2):
        self.name = name
        self.nr_inputs = 2
        self.input_vector = [None for i in range(self.nr_inputs)]
        self.output_vector = [None]

    def setInputs(self, input_vector):
        self.input_vector = input_vector
        print("{} Set AND Port inputs to: {}".format(self.name, input_vector))
        return True

    def evaluateOutputs(self):
        self.output_vector[0] = np.logical_and(*self.input_vector)
        print("{} Output evaluates to: {}".format(self.name, self.output_vector[0]))
        return self.output_vector[0]

    def getDefinition(self):
        # returns   {
        #                'name' : 'AND',
        #                'inputs' : ['A', 'B'],
        #                'outputs' : ['X']
        #            }
        return {'name' : self.name, 'inputs' : [string.ascii_uppercase[idx] for idx in range(self.nr_inputs)], 'outputs' : ['X']}
        
        
        
        
