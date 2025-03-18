from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QPoint

import Views.Dialogs.ProductDlg as Dialogs
import Views.ProductView as ProductView
import Views.CustomWidgets as CustomWidgets
from Models.ProductManager import ProductMngr
from Decorators import Timing

from pprint import pprint

class Project(QtWidgets.QWidget):
    """ widget fills main window"""
    def __init__(self):
        super().__init__()
        self._productMngr = ProductMngr()
        self._actionTable = None
        self._employeesTable = None
        self._logArea = CustomWidgets.Logger()

        self.initMenu()

    def initMenu(self):
        centralLayout = QtWidgets.QVBoxLayout()
        self.setLayout(centralLayout)
        lblLog = QtWidgets.QLabel("Журнал подій:")
        # self._logArea.addMessage("log message", "12.01.2005 8:18")
        centralLayout.addWidget(self._initTabs())
        centralLayout.addWidget(lblLog)
        centralLayout.addWidget(self._logArea, Qt.AlignmentFlag.AlignBottom)
        self._logArea.showContent(self._productMngr.getLogs())

    def _initTabs(self):
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self.createNomenclatureTab(), "Продукт")
        tabs.addTab(QtWidgets.QLabel("Тут могла бути ваша реклама"), "Звіт")
        tabs.setCurrentIndex(0)
        return tabs

    @Timing
    def createNomenclatureTab(self):
        """ nomenclature tab contents creation """
        self._actionTable = ProductView.Product(self._productMngr.getActionsList())
        tab = CustomWidgets.Inset(self._actionTable)
        tab.addButton(self.NewNomenclatureBtn, CustomWidgets.DlgMode.New, True, 'Оформити переміщення')
        editBtn = tab.addButton(self.EditNomenclatureBtn, CustomWidgets.DlgMode.Edit, False, 'Редагувати переміщення')
        delBtn = tab.addButton(self.DelNomenclatureBtn, CustomWidgets.DlgMode.Del, False, 'Видалити переміщення')
        return tab

    def _getInitPos(self) -> QPoint:
        """ calculation the starting position point of dialog"""
        dlgPos = self.mapToGlobal(self.pos())
        dlgPos.setY(dlgPos.y() - 30)
        dlgPos.setX(dlgPos.x() + 50)
        return dlgPos

    def NewNomenclatureBtn(self):
        """ if the new button was clicked """
        dialog = Dialogs.NewProductDlg(departments = self._productMngr.getProductsList(),
                                            existingIds = self._productMngr.getActionsIdList())
        dialog.move(self._getInitPos())
        result = dialog.exec()
        if result:
            self._productMngr.addAction(dialog.getProduct(), dialog.getWeight(), dialog.getNote())
            self._logArea.showContent(self._productMngr.getLogs())
            self._actionTable.loadData(self._productMngr.getActionsList())

    def EditNomenclatureBtn(self):
        print(f"{self._actionTable.getSelectedRowId()} was clicked")
        currentAction = self._productMngr.getActionById(self._actionTable.getSelectedRowId())
        dialog = Dialogs.EditProductDlg(self._productMngr.getProductsList(),
                            self._productMngr.getActionById(self._actionTable.getSelectedRowId()))
        dialog.move(self._getInitPos())
        result = dialog.exec()
        if result:
            self._productMngr.editAction(currentAction,
                                         dialog.getProduct(),
                                         dialog.getWeight(),
                                         dialog.getNote()
                                       )
            self._logArea.showContent(self._productMngr.getLogs())
            self._actionTable.loadData(self._productMngr.getActionsList())

    def DelNomenclatureBtn(self):
        currentPost = self._productMngr.getActionById(self._actionTable.getSelectedRowId())
        dialog = Dialogs.DelProductDlg(self._productMngr.getProductsList(), currentPost)
        dialog.move(self._getInitPos())
        result = dialog.exec()
        if result:
            self._productMngr.delAction(currentPost)
            self._logArea.showContent(self._productMngr.getLogs())
            self._actionTable.loadData(self._productMngr.getActionsList())

    def NewEmployeeBtn(self):
        print("new employee button was clicked")

    def EditEmployeeBtn(self):
        print("edit employee button was clicked")

    def DelEmployeeBtn(self):
        print("del employee button was clicked")

    # def topLeft(self):
    #     qr = self.frameGeometry()
    #     cp = self.screen().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     return qr.topLeft()