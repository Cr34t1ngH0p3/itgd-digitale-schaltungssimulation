from PyQt5.QtCore import QPoint

from .parent_gatter import GatterButton
from ...helper.global_variables import wireList

class OrButton(GatterButton):
    def __init__(self, name, inList=[], outList=[], parent=None, start_pos=QPoint(0,0), is_in_drop_area=False, gatter_id=None):
        super().__init__(parent, name, inList, outList, start_pos, is_in_drop_area, gatter_id)
        self.update()
     #   self.inputButton.text('OR')

    def updateState(self):
        sum = 0
        for wireId in self.inputWireList:
            try:
                sum = sum + wireList[wireId].getState()
            except Exception as e: # catch exception and dont throw error because this happens if old configs are load. there gatter with lists of all future wires are created, but the wire does not exist yet...TODO fix this problem in a pretty way
                print('Error while updating gatter state: ', e)
        if sum > 0:
            self.outputValue = 1
        else:
            self.outputValue = 0

        self.informWireAboutStateThread()


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
