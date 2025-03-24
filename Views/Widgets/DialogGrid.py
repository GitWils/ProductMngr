from typing import Callable
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from Views.Widgets.CustomWidgets import EditComboBox, LineEdit, IntSpinBox, FloatSpinBox, Note, ButtonBox

class DialogGrid:
    def __init__(self) -> None:
        self.lblWarning = None
        self.__grid = QtWidgets.QGridLayout()
        self.initSettings()
        self.initWarning()

    def initSettings(self) -> None:
        self.__grid.setContentsMargins(40, 40, 40, 40)
        self.__grid.setSpacing(30)

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

    def addNote(self, txt: str) -> Note:
        lbl = QtWidgets.QLabel(txt)
        note = Note()
        self.__addWidgets(lbl, note)
        return note

    def addComboBox(self, txt: str) -> QtWidgets.QComboBox:
        lbl = QtWidgets.QLabel(txt)
        comboBox = QtWidgets.QComboBox()
        comboBox.addItem('Форма 1', 1)
        comboBox.addItem('Форма 2', 2)
        comboBox.addItem('Форма 3', 3)
        self.__addWidgets(lbl, comboBox)
        return comboBox

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
        self.__grid.addWidget(lblWgt, self.__grid.rowCount(), 0, 1, 1)
        self.__grid.addWidget(editWgt, self.__grid.rowCount() - 1, 1, 1, 3)

    def getGrid(self) -> QtWidgets.QGridLayout:
        return self.__grid