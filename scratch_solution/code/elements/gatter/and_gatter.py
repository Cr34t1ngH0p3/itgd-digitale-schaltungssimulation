from PyQt5.QtCore import QPoint

from .parent_gatter import GatterButton
from ...helper.global_variables import wireList


class AndButton(GatterButton):
    def __init__(self, name, inList=[], outList=[], parent=None, start_pos=QPoint(0,0), is_in_drop_area=False, gatter_id=None):
        super().__init__(parent, name, inList, outList, start_pos, is_in_drop_area, gatter_id)
        self.update()
        #self.inputButton.text('AND')

    def updateState(self):
        for wireId in self.inputWireList:
            try:
                if (wireList[wireId].getState() == 0):
                    self.outputValue = 0
                    self.informWireAboutStateThread()

                  #  self.update()
                    return
            except Exception as e: # catch exception and dont throw error because this happens if old configs are load. there gatter with lists of all future wires are created, but the wire does not exist yet...TODO fix this problem in a pretty way
                print('Error while updating gatter state: ', e)

        self.outputValue = 1
        self.informWireAboutStateThread()

    #    self.update()