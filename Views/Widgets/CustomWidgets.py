from typing import Callable

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer, QSize
from enum import Enum, auto
import sys

from Views.Localization import _

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
            self.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText(_("btn.cancel"))
        else:
            self.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setObjectName('dlgBtn')
        self.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText(_("btn.save"))
        self.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setDefault(True)
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

