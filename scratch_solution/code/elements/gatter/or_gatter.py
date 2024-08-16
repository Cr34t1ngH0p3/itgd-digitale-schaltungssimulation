from .parent_gatter import GatterButton

class OrButton(GatterButton):
    def __init__(self, name, inList=[], outList=[], parent=None, position_x=0, position_y=0, is_in_drop_area=False):
        super().__init__(parent, name, inList, outList, position_x, position_y, is_in_drop_area)
        self.update()
     #   self.inputButton.text('OR')

    def update(self):
        for wire in self.inputWireList:
            if (wire.getState() == 1):
                self.outWire.setState(1)
                return
        if (self.outWire):
            self.outWire.setState(0)
