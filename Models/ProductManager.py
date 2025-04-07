from Models.DBManager import DBManager
from Models.Action import Action, Filter
from pprint import pprint
import html
import re

class ProductMngr:
	def __init__(self) -> None:
		self._db = DBManager()
		self._products = []
		self._actions = dict()
		self._filter = Filter(0)
		self.reloadAll()
		#temp debug shows
		print("Products (ProductMngr.py __init__()):")
		pprint(self._products)
		print("Actions (ProductMngr.py __init__()):")
		for key, item in self._actions.items():
			print(f"   {item}")

	def getProducts(self) -> []:
		return self._products

	def getActionsList(self) -> []:
		res = []
		for key, val in self._actions.items():
			res.append(val)
		return res

	def getActionsIdList(self) -> []:
		res = []
		for key, val in self._actions.items():
			res.append(key)
		return res

	def getActions(self):
		return self._actions

	def getActionById(self, action_id: int) -> Action:
		return self._actions[action_id]

	def getLogs(self) -> []:
		return self._db.getLogs(self._filter)

	def getLogsStr(self) -> str:
		list = self._db.getLogs(self._filter)
		result = '\n'.join([f"{index + 1}. [{item[1]}] -> {item[0]} [баланс: {100}кг]" for index, item in enumerate(reversed(list))])
		result = re.sub('<.*?>', '', result)
		return  result

	def addProduct(self, name: str) -> int:
		productId = self._db.newProduct(name)
		self.reloadProducts()
		return productId

	def getBalanceByProductId(self, product_id) -> float:
		res = None
		for product in self._products:
			if product['id'] == product_id:
				res = product['sum']
		return res

	def reloadAll(self) -> None:
		self.reloadProducts()
		self.reloadActions()

	def reloadProducts(self) -> None:
		# self._products.clear()
		self._products = self._db.getProducts()

	def reloadActions(self) -> None:
		self._actions.clear()
		self._actions = self._db.getActions(self._filter)

	def addAction(self, product: str, weight: float, note: str) -> None:
		productId = self.addProduct(product)
		balance = self.getBalanceByProductId(productId) + weight
		self._db.newAction(productId, weight, note)
		if weight > 0:
			msg = f'отримано <span style="text-decoration: underline">{product}</span> '\
				f'вагою <span style="text-decoration: underline">{weight:.2f}</span> кг'
		else:
			msg = f'передано в роботу <span style="text-decoration: underline">{product}</span> ' \
			      f'вагою <span style="text-decoration: underline">{-weight:.2f}</span> кг'
		msg += f' -> залишок: <span style="text-decoration: underline">{balance}</span> кг'
		self._db.newLogMsg(productId, msg)
		self.reloadAll()

	def delAction(self, action: Action) -> None:
		self._db.delActionById(action.getId(), action.getProductId())
		balance = self.getBalanceByProductId(action.getProductId()) - action.getWeight()
		msg = f'видалено переміщення <span style="text-decoration: underline">{action.getName()}</span> '\
				f'вагою <span style="text-decoration: underline">{abs(action.getWeight()):.2f}</span> кг '\
				f'-> залишок: <span style="text-decoration: underline">{balance}</span> кг'
		self._db.newLogMsg(action.getProductId(), msg)
		self.reloadAll()

	def editAction(self,
	             original_action: Action,
	             product: str,
	             weight: float,
	             note: str
	             ) -> None:
		if product != original_action.getName():
			self._db.updateProduct(product, original_action.getProductId())
		if weight != original_action.getWeight() or note != original_action.getNote():
			self._db.updateAction(original_action.getId(), original_action.getProductId(), weight, note)
		balance = self.getBalanceByProductId(original_action.getProductId()) + (weight - original_action.getWeight())
		msg = f'відредаговано переміщення <span style="text-decoration: underline">{original_action.getName()}</span> '\
				f'-> залишок: <span style="text-decoration: underline">{balance}</span> кг'
		#f'вагою <span style="text-decoration: underline">{abs(action.getWeight()):.2f}</span>, кг'
		self._db.newLogMsg(original_action.getProductId(), msg)
		self.reloadAll()

	def setFilterID(self, product_id: int) -> None:
		self._filter.setProductId(product_id)
		self.reloadActions()

	def setFilterPeriod(self, begin: str, end: str) -> None:
		self._filter.setBeginDate(begin)
		self._filter.setEndDate(end)

	def setFilterLimit(self, limit: int) -> None:
		self._filter.setLimit(limit)

	def filterClear(self) -> None:
		self._filter.clear()