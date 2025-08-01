from typing import Callable
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QDateTime

from Views.Widgets.CustomWidgets import EditComboBox, LineEdit, IntSpinBox, FloatSpinBox, Note, ButtonBox

class PeriodBox:
    def __init__(self, begin: str, to: str) -> None:
        self._beginLbl = QtWidgets.QLabel(begin)
        self._beginLbl.setContentsMargins(50, 0, 0, 0)
        self._endLbl = QtWidgets.QLabel(to)
        self._beginDate = QtWidgets.QDateTimeEdit()
        self._beginDate.setCalendarPopup(True)
        self._toDate = QtWidgets.QDateTimeEdit()
        self._toDate.setCalendarPopup(True)
        self._toDate.setDateTime(QDateTime.currentDateTime())
        self._beginDate.setDateTime(self._toDate.dateTime().addDays(-7))

    def getBeginLbl(self):
        return self._beginLbl

    def getEndLbl(self):
        return self._endLbl

    def getBeginDate(self):
        return self._beginDate

    def getEndDate(self):
        return self._toDate

class DialogGrid:
    def __init__(self) -> None:
        self.lblWarning = None
        self.__grid = QtWidgets.QGridLayout()
        self.initSettings()
        self.initWarning()

    def initSettings(self) -> None:
        self.__grid.setContentsMargins(40, 40, 40, 40)
        self.__grid.setSpacing(30)

        # self.__grid.setColumnStretch(0, 1)
        # self.__grid.setColumnStretch(1, 2)
        # self.__grid.setColumnStretch(2, 1)
        # self.__grid.setColumnStretch(3, 2)

    def setMargins(self, val: int) -> None:
        self.__grid.setContentsMargins(val, val, val, val)

    def initWarning(self) -> None:
        self.lblWarning = QtWidgets.QLabel('')
        self.lblWarning.setObjectName('orange')
        self.__addWidget(self.lblWarning)
        self.lblWarning.hide()

    def setMsg(self, txt: str) -> None:
        self.lblWarning.setText(txt)
        self.lblWarning.show()

    def addEditBox(self, txt: str) -> EditComboBox:
        lbl = QtWidgets.QLabel(txt)
        box = EditComboBox()
        self.__addWidgets(lbl, box)
        return box

    def addLineEdit(self, txt, val = '', readonly : bool=False, changedFunc = None) -> LineEdit:
        lbl = QtWidgets.QLabel(txt)
        edit = LineEdit(val, readonly, changedFunc)
        self.__addWidgets(lbl, edit)
        return edit

    def addSpinBox(self, txt: str, changedFunc=None) -> IntSpinBox:
        lbl = QtWidgets.QLabel(txt)
        spin = IntSpinBox(changedFunc = changedFunc)
        self.__addWidgets(lbl, spin)
        return spin

    def addFloatBox(self, txt: str, changedFunc=None) -> FloatSpinBox:
        lbl = QtWidgets.QLabel(txt)
        spin = FloatSpinBox(changedFunc = changedFunc)
        self.__addWidgets(lbl, spin)
        return spin

    def addFromDateBox(self, txt: str, changedFunc=None) -> QtWidgets.QDateTimeEdit:
        lbl = QtWidgets.QLabel(txt)
        date = QtWidgets.QDateTimeEdit()
        self.__addWidgets(lbl, date)
        return date

    def addPeriodBox(self, begin: str, to: str) -> PeriodBox:
        periodBox = PeriodBox(begin, to)
        self.__addQuadrupleWidgets(periodBox.getBeginLbl(), periodBox.getBeginDate(),
                                   periodBox.getEndLbl(),    periodBox.getEndDate())
        return periodBox

    def addNote(self, txt: str) -> Note:
        lbl = QtWidgets.QLabel(txt)
        note = Note()
        self.__addWidgets(lbl, note)
        return note

    def addButtonBox(self,
                     doubleBtnMode: bool,
                     acceptedFunc: Callable[[], None],
                     rejectedFunc: Callable[[], None]
                     ) -> ButtonBox:
        bbox = ButtonBox(doubleBtnMode, acceptedFunc, rejectedFunc)
        self.__addWidget(bbox)
        self.__grid.setAlignment(bbox, Qt.AlignmentFlag.AlignCenter)
        return bbox

    def __addWidget(self, wgt) -> None:
        self.__grid.addWidget(wgt, self.__grid.rowCount(), 0, 1, 4)

    def __addWidgets(self, lblWgt, editWgt) -> None:
        self.__grid.addWidget(lblWgt, self.__grid.rowCount(), 0, 1, 2)
        self.__grid.addWidget(editWgt, self.__grid.rowCount() - 1, 2, 1, 2)
        # self.__grid.addWidget(lblWgt, self.__grid.rowCount(),       0, 1, 1)
        # self.__grid.addWidget(editWgt, self.__grid.rowCount() - 1,  1, 1, 3)

    def __addQuadrupleWidgets(self, lblWgt1, editWgt1, lblWgt2, editWgt2):
        self.__grid.addWidget(lblWgt1,  self.__grid.rowCount(),     0, 1, 1)
        self.__grid.addWidget(editWgt1, self.__grid.rowCount() - 1, 1, 1, 1)
        self.__grid.addWidget(lblWgt2,  self.__grid.rowCount() - 1, 2, 1, 1)
        self.__grid.addWidget(editWgt2, self.__grid.rowCount() - 1, 3, 1, 1)

    def getGrid(self) -> QtWidgets.QGridLayout:
        return self.__grid