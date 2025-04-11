#! /usr/bin/python3

from PyQt6 import QtWidgets 
from PyQt6.QtCore import Qt, QEvent, QTranslator
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QStyleFactory

from Views.Widgets.CustomWidgets import SplashScreen
from Views.Widgets.Translator import UkrainianTranslator
from Project import Project, Settings
from ProjectTypes import Theme
import sys

class MainWindow(QtWidgets.QMainWindow, Settings):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Облік продукту ")
        self.setMinimumSize(1004, 750)
        self.centerWindow()
        self._initUI()

    def _initUI(self):
        """ user interface initializing"""
        ico = QIcon("img/logo.png")
        self.setWindowIcon(ico)
        self.pr = Project()
        self.setMenuBar(self._createMenuBar())
        self.setCentralWidget(self.pr)

    def _createMenuBar(self):
        menuBar = QtWidgets.QMenuBar(self)
        fileMenu = QtWidgets.QMenu("&Файл", self)
        excellAct = QAction("&Експорт в Excel", self)
        #excellAct.triggered.connect(self.pr.openSaveDlg)
        fileMenu.addAction(excellAct)
        printAct = QAction("&Друкувати журнал", self)
        printAct.triggered.connect(self.pr.printActions)
        fileMenu.addAction(printAct)

        viewMenu = QtWidgets.QMenu("&Вигляд", self)
        styleMenu = QtWidgets.QMenu("&Тема", self)
        viewMenu.addMenu(styleMenu)
        darkThemeAct = QAction("Темна", self)
        darkThemeAct.triggered.connect(self._setDarkTheme)
        osThemeAct = QAction("Звичайна", self)
        osThemeAct.triggered.connect(self._setOSTheme)
        styleMenu.addAction(osThemeAct)
        styleMenu.addAction(darkThemeAct)

        menuBar.addMenu(fileMenu)
        menuBar.addMenu(viewMenu)
        return menuBar

    def _setDarkTheme(self):
        with open("style.css", "r") as file:
            self.setStyleSheet(file.read())
        self.setTheme(Theme.Dark)
        self.pr.setTheme(Theme.Dark)

    def _setOSTheme(self):
        self.setStyleSheet("")
        self.setStyle(QStyleFactory.create("Windows"))
        self.setTheme(Theme.OS)
        self.pr.setTheme(Theme.OS)

    def event(self, e) -> QtWidgets.QWidget.event:
        """ hotkey handling """
        if e.type() == QEvent.Type.WindowDeactivate:
            self.setWindowOpacity(0.85)
        elif e.type() == QEvent.Type.WindowActivate:
            self.setWindowOpacity(1)
        elif e.type() == QEvent.Type.KeyPress and e.key() == Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)

    def centerWindow(self):
        """ centering the main window at the center of the screen """
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    """ start program function """
    app = QtWidgets.QApplication(sys.argv)
    # with open("style.css", "r") as file:
    #     app.setStyleSheet(file.read())
    translator = UkrainianTranslator()
    app.installTranslator(translator)
    # Створюємо і показуємо заставку
    splash = SplashScreen()
    splash.show()
    splash.start_progress()
    while splash.progress_value < 100:
        app.processEvents()
    # Створюємо головне вікно
    # ico = QIcon("img/logo.png")
    # app.setWindowIcon(ico)
    window = MainWindow()
    window.show()
    splash.finish(window)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()