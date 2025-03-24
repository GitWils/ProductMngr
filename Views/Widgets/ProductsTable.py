from typing import Callable
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt

from Views.Widgets.CustomWidgets import DlgMode, EditBtn

class ProductsTable(QtWidgets.QWidget):
    def __init__(self, table1, table2) -> None:
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self._buttons = list()

        self.tblLayout = ProductsTable.getTblLayout()
        self.tblLayout.addWidget(table1)
        self.tblLayout.addWidget(table2)
        tblWgt = QtWidgets.QWidget()
        tblWgt.setLayout(self.tblLayout)
        self.layout.addWidget(tblWgt)

        self.btnLayout = ProductsTable.getBtnLayout()
        btnsWgt = QtWidgets.QWidget()
        btnsWgt.setLayout(self.btnLayout)
        self.layout.addWidget(btnsWgt)

        table2.clicked.connect(self.setActiveBtns)

    @staticmethod
    def getTblLayout() -> QtWidgets.QHBoxLayout:
        tblLayout = QtWidgets.QHBoxLayout()
        # tblLayout.setContentsMargins(0, 0, 0, 10)
        tblLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        return tblLayout

    @staticmethod
    def getBtnLayout() -> QtWidgets.QHBoxLayout:
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(0, 0, 0, 10)
        btnLayout.setSpacing(40)
        btnLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        # btnLayout.addStretch(40)
        return btnLayout

    def addButton(self,
                  func: Callable[[], None],
                  mode_type: DlgMode,
                  active: bool,
                  tooltip: str
                  ) -> QtWidgets.QPushButton:
        match mode_type:
            case DlgMode.Add:
                filename = 'new.png'
            case DlgMode.Sub:
                filename = 'minus.png'
            case DlgMode.Edit:
                filename = 'edit.png'
            case DlgMode.Del:
                filename = 'del.png'
            case _:
                raise ValueError("Unknown button type")
        btn = EditBtn(filename, active, tooltip)
        self.btnLayout.addWidget(btn)
        btn.clicked.connect(func)
        self._buttons.append(btn)
        return btn

    def setActiveBtns(self, status: bool) -> None:
        for btn in self._buttons:
            btn.setActive(status)