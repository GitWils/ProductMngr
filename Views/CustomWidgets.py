from typing import Callable

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer, QSize
from enum import Enum, auto
import sys

class DlgMode(Enum):
    Add = auto()
    Sub = auto()
    Edit = auto()
    Del = auto()

class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self) -> None:
        super().__init__()
        splash_pix = QtGui.QPixmap('img/splash.svg')
        self.setPixmap(splash_pix)
        # Додаємо прогрес-бар
        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setGeometry(100,
                                  splash_pix.height() - 160,
                                  splash_pix.width() - 200,
                                  40)
        # Таймер для оновлення прогресу
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0

    def start_progress(self) -> None:
        self.timer.start(3)  # Оновлення кожні 10мс

    def update_progress(self) -> None:
        self.progress_value += 1
        self.progress.setValue(self.progress_value)
        # Оновлюємо текст
        # self.showMessage(f"Завантаження... {self.progress_value}%",
        #                  Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
        #                  Qt.GlobalColor.white)
        if self.progress_value >= 100:
            self.timer.stop()

class Inset(QtWidgets.QWidget):
    def __init__(self, table1, table2) -> None:
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self._buttons = list()

        self.tblLayout = Inset.getTblLayout()
        self.tblLayout.addWidget(table1)
        self.tblLayout.addWidget(table2)
        tblWgt = QtWidgets.QWidget()
        tblWgt.setLayout(self.tblLayout)
        self.layout.addWidget(tblWgt)

        self.btnLayout = Inset.getBtnLayout()
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

class EditBtn(QtWidgets.QPushButton):
    def __init__(self, filename: str, active: bool, tooltip: str = '') -> None:
        self.filename = filename
        if active:
            QtWidgets.QPushButton.__init__(self, QtGui.QIcon('img/act' + self.filename), '')
        else:
            QtWidgets.QPushButton.__init__(self, QtGui.QIcon('img/inact' + self.filename), '')
            self.setDisabled(True)
        self.setIconSize(QSize(40, 40))
        self.setToolTip(tooltip)
        self.setObjectName("mng")
        self.setCursor(QtGui.QCursor(Qt.CursorShape.OpenHandCursor))
        self.setStyleSheet("border: 0px solid red")

    def setActive(self, active: bool):
        if active:
            self.setIcon(QtGui.QIcon('img/act' + self.filename))
            self.setEnabled(True)
        else:
            self.setIcon(QtGui.QIcon('img/inact' + self.filename))
            self.setDisabled(True)

    def fileName(self) -> str:
        return self.filename

class ButtonBox(QtWidgets.QDialogButtonBox):
    def __init__(self,
                 doubleBtnMode: bool,
                 acceptedFunc: Callable[[], None],
                 rejectedFunc: Callable[[], None]
                 ) -> None:
        super().__init__()
        if doubleBtnMode:
            self.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel |
                                QtWidgets.QDialogButtonBox.StandardButton.Ok)
            self.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setObjectName('dlgBtn')
            self.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText('Скасувати')
        else:
            self.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setObjectName('dlgBtn')
        self.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText('Зберегти')
        if acceptedFunc: self.accepted.connect(acceptedFunc)
        if rejectedFunc: self.rejected.connect(rejectedFunc)
        if sys.platform == 'win32' or sys.platform == 'win64':
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

    def setBtnOkText(self, text: str) -> None:
        self.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText(text)

    def setBtnCancelText(self, text: str) -> None:
        self.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText(text)

class EditComboBox(QtWidgets.QComboBox):
    def __init__(self) -> None:
        super().__init__()
        self.setEditable(True)

class Table(QtWidgets.QTableView):
    """ table widget to display data """
    def __init__(self) -> None:
        super().__init__()
        self.initColumnStyles()
        #self.setObjectName("table")

    def initColumnStyles(self) -> None:
        self.setMinimumHeight(470)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setEditTriggers(QtWidgets.QListView.EditTrigger.NoEditTriggers)

class IntSpinBox(QtWidgets.QSpinBox):
    """ spinbox widget for int numbers """
    def __init__(self, readonly=False, changedFunc=None) -> None:
        super().__init__()
        self.setValue(0)
        self.setMaximum(100000)
        self.setReadOnly(readonly)
        # self.setSuffix(' шт.')
        if changedFunc: self.textChanged.connect(changedFunc)

class FloatSpinBox(QtWidgets.QDoubleSpinBox):
    """ spinbox widget for float numbers """
    def __init__(self, readonly=False, changedFunc=None):
        super().__init__()
        self.setValue(1)
        self.setMaximum(100000)
        self.setReadOnly(readonly)
        self.setDecimals(2)
        if changedFunc: self.textChanged.connect(changedFunc)

class LineEdit(QtWidgets.QLineEdit):
    """ LineEdit widget with custom parameters """
    def __init__(self, text='', readonly=False, changedFunc=None) -> None:
        super().__init__()
        self.setReadOnly(readonly)
        self.setText(text)
        if changedFunc: self.textChanged.connect(changedFunc)

class Note(QtWidgets.QTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.setMaximumHeight(100)

class Logger(QtWidgets.QTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.init()
        #self.setMinimumHeight(147)
        self.setMaximumHeight(120)

    def init(self) -> None:
        self.setReadOnly(True)

    def showContent(self, logs: []) -> None:
        self.clear()
        msg = ''
        for log in logs:
            msg += f'<br>{log[1][0:5]} <span style="text-decoration: underline">{log[1][6:]}</span> {log[0]}'
        self.insertHtml(msg[4:])
        self.ensureCursorVisible()

    def addMessage(self, msg: str, date: str) -> None:
        self.insertHtml(f'{date[0:5]}<span style="text-decoration: underline">{date[7:]}</span>{msg}<br>')
        self.ensureCursorVisible()

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