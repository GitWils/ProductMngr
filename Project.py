from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QPoint

import Views.Dialogs.ProductDlg as Dialogs
import Views.ProductView as ProductView
import Views.ActionView as ActionView
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
        self._productTable = None
        self._employeesTable = None
        self._logArea = CustomWidgets.Logger()

        self.initMenu()

    def initMenu(self):
        centralLayout = QtWidgets.QVBoxLayout()
        self.setLayout(centralLayout)
        lblLog = QtWidgets.QLabel("Журнал подій:")
        centralLayout.addWidget(self._initTabs())
        centralLayout.addWidget(lblLog)
        centralLayout.addWidget(self._logArea, Qt.AlignmentFlag.AlignBottom)
        self._logArea.showContent(self._productMngr.getLogs())

    def _initTabs(self):
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self.createProductsTab(), "Продукти")
        tabs.addTab(QtWidgets.QLabel("Тут могла бути ваша реклама"), "Звіт")
        tabs.setCurrentIndex(0)
        return tabs

    @Timing
    def createProductsTab(self):
        """ nomenclature tab contents creation """
        self._productTable = ProductView.ProductTable(self._productMngr.getProducts())
        self._actionTable = ActionView.ActionTable(self._productMngr.getActionsList())
        tab = CustomWidgets.Inset(self._productTable, self._actionTable)
        tab.addButton(self.addActionBtn, CustomWidgets.DlgMode.Add, True, 'Добавити продукт')
        subBtn = tab.addButton(self.subtractActionBtn, CustomWidgets.DlgMode.Sub, True, 'Забрати продукт')
        editBtn = tab.addButton(self.editActionBtn, CustomWidgets.DlgMode.Edit, False, 'Редагувати переміщення')
        delBtn = tab.addButton(self.DelActionBtn, CustomWidgets.DlgMode.Del, False, 'Видалити переміщення')
        self._productTable.clicked.connect(self.showActions)
        self._actionTable.doubleClicked.connect(self.editActionBtn)
        return tab

    def showActions(self):
        self._productMngr.setFilterID(self._productTable.getSelectedRowId())
        self.ReloadTables()

    def _getInitPos(self) -> QPoint:
        """ calculation the starting position point of dialog"""
        dlgPos = self.mapToGlobal(self.pos())
        dlgPos.setX(dlgPos.x() + 170)
        dlgPos.setY(dlgPos.y() + 80)
        return dlgPos

    def addActionBtn(self):
        """ if the add action button was clicked """
        dialog = Dialogs.AddProductDlg(departments = self._productMngr.getProductsList(),
                                        existingIds = self._productMngr.getActionsIdList())
        dialog.move(self._getInitPos())
        result = dialog.exec()
        if result:
            self._productMngr.addAction(dialog.getProduct(), dialog.getWeight(), dialog.getNote())
            self._logArea.showContent(self._productMngr.getLogs())
            self.ReloadTables()

    def subtractActionBtn(self):
        """ if subtract action button was clicked """
        dialog = Dialogs.SubtractProductDlg(departments = self._productMngr.getProductsList(),
                                            existingIds = self._productMngr.getActionsIdList())
        dialog.move(self._getInitPos())
        result = dialog.exec()
        if result:
            self._productMngr.addAction(dialog.getProduct(), -dialog.getWeight(), dialog.getNote())
            self._logArea.showContent(self._productMngr.getLogs())
            self.ReloadTables()

    def editActionBtn(self):
        """ if edit action button was clicked """
        currentAction = self._productMngr.getActionById(self._actionTable.getSelectedRowId())
        dialog = Dialogs.EditProductDlg(self._productMngr.getProductsList(),
                            self._productMngr.getActionById(self._actionTable.getSelectedRowId()),
                            [])
        dialog.move(self._getInitPos())
        result = dialog.exec()
        if result:
            self._productMngr.editAction(currentAction,
                                         dialog.getProduct(),
                                         dialog.getWeight(),
                                         dialog.getNote()
                                       )
            self._logArea.showContent(self._productMngr.getLogs())
            self.ReloadTables()

    def DelActionBtn(self):
        """ if delete action button was clicked """
        currentPost = self._productMngr.getActionById(self._actionTable.getSelectedRowId())
        dialog = Dialogs.DelProductDlg(self._productMngr.getProductsList(), currentPost)
        dialog.move(self._getInitPos())
        result = dialog.exec()
        if result:
            self._productMngr.delAction(currentPost)
            self._logArea.showContent(self._productMngr.getLogs())
            self.ReloadTables()

    def ReloadTables(self) -> None:
        self._actionTable.loadData(self._productMngr.getActionsList())
        self._productTable.loadData(self._productMngr.getProducts())

    # def topLeft(self):
    #     qr = self.frameGeometry()
    #     cp = self.screen().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     return qr.topLeft()