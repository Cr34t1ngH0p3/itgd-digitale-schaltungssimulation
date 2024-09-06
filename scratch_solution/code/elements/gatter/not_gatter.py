from .parent_gatter import GatterButton
from ...helper.global_variables import wireList


class NotButton(GatterButton):
    def __init__(self, name, inList=[], outList=[],  position_x=0, position_y=0, is_in_drop_area=False, parent=None, gatter_id=None):
        super().__init__(parent, name, inList, outList, position_x, position_y, is_in_drop_area, gatter_id)
        self.update()
        #self.inputButton.text('AND')

    def updateState(self):

        #Yeah, I understand, that there is only one input value here and it is possible to make it easier, but anyway :)
        sum = 0
        for wireId in self.inputWireList:
            try:
                sum = sum + wireList[wireId].getState()
            except Exception as e: # catch exception and dont throw error because this happens if old configs are load. there gatter with lists of all future wires are created, but the wire does not exist yet...TODO fix this problem in a pretty way
                print('Error while updating gatter state: ', e)
        if sum > 0:
            self.outputValue = 0
        else:
            self.outputValue = 1

        self.informWireAboutState()


        self.update()