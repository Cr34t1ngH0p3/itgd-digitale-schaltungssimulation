from .parent_gatter import GatterButton

class OrButton(GatterButton):
    def __init__(self, _out, _inList, name):
        super().__init__(name)
        self.out = _out
        self.inputWireList = _inList
        self.update()
        self.inputButton.text('OR')

    def update(self):
        for wire in self.inputWireList:
            if (wire.getState() == 1):
                self.outWire.setState(1)
                return
        self.outWire.setState(0)
