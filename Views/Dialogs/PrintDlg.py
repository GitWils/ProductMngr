from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
from Views.Widgets.DialogGrid import DialogGrid
from pprint import pprint

class PrintDlg(QDialog):
	def __init__(self) -> None:
		super().__init__()
		self.setWindowModality(Qt.WindowModality.ApplicationModal)
		self.setFixedWidth(530)
		self.setFixedHeight(300)
		self.setWindowTitle("Друкувати журнал подій")
		self._dlgGrid = DialogGrid()
		self._periodBox = self._dlgGrid.addPeriodBox('з', 'по')
		self._countWgt = self._dlgGrid.addSpinBox("максимальна кількість звітів:")
		self._countWgt.setValue(50)
		self._bbox = self._dlgGrid.addButtonBox(True, acceptedFunc=self.accept, rejectedFunc=self.reject)
		self._bbox.setBtnOkText('Друкувати')
		self._dlgGrid.setMsg("Виберіть період")
		self.setLayout(self._dlgGrid.getGrid())

	def accept(self) -> None:
		# if len(self.getProduct()) == 0:
		# 	self.setMsg('Введіть назву продукту!')
		# elif self.getWeight() == 0.00:
		# 	self.setMsg('Вага не може мати нульове значення!')
		# else:
		# 	super().accept()
		super().accept()

	def reject(self) -> None:
		super().reject()

