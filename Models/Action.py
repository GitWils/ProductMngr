from datetime import datetime

class Filter:
	def __init__(self, product_id=0, limit: int=50, begin_date: str=None, end_date: str=None) -> None:
		self._productId = product_id
		self._beginDate = begin_date
		self._endDate = end_date
		self._limit = limit

	def __str__(self) -> str:
		return f"{self._productId} від {self._beginDate} до {self._endDate}, ліміт - {self._limit}"

	def setProductId(self, product_id: int) -> None:
		self._productId = product_id

	def getProductId(self) -> int:
		return self._productId

	def setBeginDate(self, begin_date: str):
		self._beginDate = begin_date

	def getBeginDate(self):
		return self._beginDate

	def setEndDate(self, to_date: str):
		self._endDate = to_date

	def getEndDate(self):
		return self._endDate

	def setLimit(self, limit: int):
		self._limit = limit

	def getLimit(self):
		return self._limit

	def clear(self):
		self._beginDate = None
		self._endDate = None
		self._limit = 50

class Action:
	def __init__(self, name: str, name_id: int, action_id: int, weight: float, note: str, blocked: bool, date: datetime) -> None:
		""" action unit
		name - job title
		name_id - id number in product table
		action_id - id number in action table
		weight - weigh of product in kg
		note - possible notes
		blocked - can't edit or remove if True
		date - creation date"""
		self._name =    name
		self._name_id = name_id
		self._id =      action_id
		self._weight =  weight
		self._note =    note
		self._blocked = blocked
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

	def isBlocked(self) -> bool:
		return self._blocked

	def getDate(self) -> datetime:
		return self._date