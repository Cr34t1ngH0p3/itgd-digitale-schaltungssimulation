from .parent_gatter import GatterButton

class AndButton(GatterButton):
    def __init__(self, name, _out=None, _inList={}):
        super().__init__(name)
        self.out = _out
        self.inputWireList = _inList
        self.update()
        #self.inputButton.text('AND')

    def update(self):
        for wire in self.inputWireList:
            if (wire.getState() == 0):
                self.outWire.setState(0)
                return
        if (self.outWire):
            self.outWire.setState(1)