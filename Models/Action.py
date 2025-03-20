from datetime import datetime

class Filter:
	def __init__(self, product_id=0):
		self._productId = product_id

	def setProductId(self, product_id: int) -> None:
		self._productId = product_id

	def getProductId(self):
		return self._productId

class Action:
	def __init__(self, name: str, name_id: int, action_id: int, weight: float, note: str, date: datetime) -> None:
		""" nomenclature unit
		name - job title
		id - number by nomenclature
		weight - ..."""
		self._name =    name
		self._name_id = name_id
		self._id =      action_id
		self._weight =  weight
		self._note =    note
		self._date =    date

	def __str__(self) -> str:
		return f"{self._name}:{self._name_id}, вага - {self._weight}кг примітка - \"{self._note}\" створено - {self._date}"

	def getName(self) -> str:
		return self._name

	def getProductId(self) -> int:
		return self._name_id

	def getId(self) -> int:
		return self._id

	def getWeight(self) -> float:
		return self._weight

	def getNote(self) -> str:
		return self._note

	def getDate(self) -> datetime:
		return self._date