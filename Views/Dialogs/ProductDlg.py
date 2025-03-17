from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
import Views.CustomWidgets as CustomWidgets
from pprint import pprint
from abc import ABC, abstractmethod

class ProductDlg(QDialog):
	def __init__(self, departments: [], existingIds: []=[]) -> None:
		super().__init__()
		self.setWindowModality(Qt.WindowModality.ApplicationModal)
		self.setFixedWidth(700)
		self.setMinimumHeight(400)
		self._departments = departments
		self._existingIds = existingIds
		# self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
		self._dlgGrid = CustomWidgets.DialogGrid()
		self._drawProductField('Найменування продукту:')
		self._weight = self._dlgGrid.addFloatBox('Вага (кг):')
		self._wgtNote = self._dlgGrid.addNote('Примітка:')
		self._bbox = self._dlgGrid.addButtonBox(True, acceptedFunc = self.accept, rejectedFunc=self.reject)
		self.setLayout(self._dlgGrid.getGrid())
		self._initValues()

	def accept(self) -> None:
		if len(self.getProduct()) == 0:
			self.setMsg('Введіть назву продукту!')
		# elif len(self.getPost()) == 0:
		# 	self.setMsg('Введіть найменування посади!')
		# elif self.getNomenclatureId() < 1:
		# 	self.setMsg('Номер підрозділу повинен бути більше 0!')
		else:
			super().accept()

	def setMsg(self, msg: str) -> None:
		self._dlgGrid.setMsg(msg)
		self.adjustSize()

	@abstractmethod
	def _drawProductField(self, name) -> None:
		pass

	@abstractmethod
	def _initValues(self) -> None:
		pass

	def reject(self) -> None:
		super().reject()

	@abstractmethod
	def getProduct(self) -> None:
		pass

	def getWeight(self) -> float:
		return self._weight.value()

	def getNote(self) -> str:
		return self._wgtNote.toPlainText()

class NewProductDlg(ProductDlg):
	def __init__(self, departments, existingIds: []=[]) -> None:
		super().__init__(departments, existingIds = existingIds)

	def _initValues(self) -> None:
		self.setWindowTitle("Створення нової посади")

	def _drawProductField(self, name: str) -> None:
		self._productName = self._dlgGrid.addEditBox(name)
		self._productName.addItems(self._departments)

	def getProduct(self) -> str:
		return self._productName.currentText()

class EditProductDlg(ProductDlg):
	def __init__(self, products: [], action: [], existingIds: []=[]) -> None:
		self._action = action
		super().__init__(products, existingIds = existingIds)

	def accept(self) -> None:
		if self.getProduct() == self._action.getName()\
			and self.getWeight() == self._action.getWeight()\
			and self.getNote() == self._action.getNote():
			self.setMsg('Жоден параметр не змінено!\nВведіть значення, або натисніть "Скасувати"')
		else:
			super().accept()

	def _initValues(self) -> None:
		self.setWindowTitle("Редагування посади")
		self._weight.setValue(self._action.getWeight())
		# self._wgtNote.setValue(self._post.getId())

	def _drawProductField(self, name: str) -> None:
		self._productName = self._dlgGrid.addLineEdit(name, self._action.getName())

	def getProduct(self) -> str:
		return self._productName.text()

class DelProductDlg(ProductDlg):
	def __init__(self, products: [], action: [], existingIds: []=[]):
		self._action = action
		super().__init__(products, existingIds = existingIds)

	def _initValues(self) -> None:
		self.setWindowTitle("Видалення запису")
		self._weight.setValue(self._action.getWeight())
		# self._wgtNote.setValue(self._post.getId())
		self._bbox.setBtnOkText('Видалити')
		self._setReadonlyAll()

	def _drawProductField(self, name: str) -> None:
		self._productName = self._dlgGrid.addLineEdit(name, self._action.getName())

	def _setReadonlyAll(self) -> None:
		self._productName.setReadOnly(True)
		self._weight.setReadOnly(True)
		self._wgtNote.setReadOnly(True)

	def getProduct(self) -> str:
		return self._productName.text()