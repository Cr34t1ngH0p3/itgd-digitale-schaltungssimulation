from .parent_gatter import GatterButton
from ...helper.global_variables import wireList

class OrButton(GatterButton):
    def __init__(self, name, inList=[], outList=[], parent=None, position_x=0, position_y=0, is_in_drop_area=False):
        super().__init__(parent, name, inList, outList, position_x, position_y, is_in_drop_area)
        self.update()
     #   self.inputButton.text('OR')

    def updateState(self):
        sum = 0
        for wireId in self.inputWireList:
            sum = sum + wireList[wireId].getState()
        if sum > 0:
            self.outputValue = 1
        else:
            self.outputValue = 0
        for wireId in self.outWire:
            wireList[wireId].setState(self.outputValue)


#        for wireId in self.inputWireList:
#            if (wireList[wireId].getState() == 1):
#                self.outputValue = 1
#                for wireId in self.outWire:
#                    wireList[wireId].setState(1)
#            self.update()
#            return
#        self.outputValue = 0
#        for wireId in self.outWire:
#            wireList[wireId].setState(0)

        self.update()
