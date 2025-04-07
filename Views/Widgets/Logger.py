from PyQt6 import QtGui, QtWidgets

class Logger(QtWidgets.QTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.init()
        #self.setMinimumHeight(147)
        self.setMaximumHeight(140)

    def init(self) -> None:
        self.setReadOnly(True)

    def showContent(self, logs: []) -> None:
        self.clear()
        msg = ''
        for log in logs:
            msg += f'<br>{log[1][0:5]} <span style="text-decoration: underline">{log[1][6:]}</span> {log[0]}'
        self.insertHtml(msg[4:])
        self.ensureCursorVisible()
        # self.moveCursor(QtGui.QTextCursor.MoveOperation.Start)

    def addMessage(self, msg: str, date: str) -> None:
        self.insertHtml(f'{date[0:5]}<span style="text-decoration: underline">{date[7:]}</span>{msg}<br>')
        self.ensureCursorVisible()
        self.moveCursor(QtGui.QTextCursor.MoveOperation.End)