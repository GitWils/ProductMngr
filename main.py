#! /usr/bin/python3

from PyQt6 import QtWidgets 
from PyQt6.QtCore import Qt, QEvent, QTranslator
from PyQt6.QtGui import QIcon, QAction

from Views.Widgets.CustomWidgets import SplashScreen
from Views.Widgets.Translator import UkrainianTranslator
from Project import Project
import sys

class MainWindow(QtWidgets.QMainWindow):
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
        file_menu = QtWidgets.QMenu("&Файл", self)
        excellAct = QAction("&Експорт в Excel", self)
        #excellAct.triggered.connect(self.pr.openSaveDlg)
        file_menu.addAction(excellAct)
        print_action = QAction("&Друкувати журнал", self)
        print_action.triggered.connect(self.pr.printActions)
        file_menu.addAction(print_action)
        view_menu = QtWidgets.QMenu("&Вигляд", self)
        view_menu.addAction(QAction("&Налаштування", self))
        menuBar.addMenu(file_menu)
        menuBar.addMenu(view_menu)
        return menuBar

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
    with open("style.css", "r") as file:
        app.setStyleSheet(file.read())
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