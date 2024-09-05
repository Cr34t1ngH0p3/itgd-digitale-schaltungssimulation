from .parent_gatter import GatterButton
from ...helper.global_variables import wireList


class AndButton(GatterButton):
    def __init__(self, name, inList=[], outList=[],  position_x=0, position_y=0, is_in_drop_area=False, parent=None, gatter_id=None):
        super().__init__(parent, name, inList, outList, position_x, position_y, is_in_drop_area, gatter_id)
        self.update()
        #self.inputButton.text('AND')

    def updateState(self):
        for wireId in self.inputWireList:
            if (wireList[wireId].getState() == 0):
                self.outputValue = 0
                self.informWireAboutState()

                self.update()
                return

        self.outputValue = 1
        self.informWireAboutState()

        self.update()