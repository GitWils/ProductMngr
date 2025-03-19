from Models.DBManager import DBManager
from Models.Action import Action
from pprint import pprint


class ProductMngr:
	def __init__(self) -> None:
		self._db = DBManager()
		self._products = []
		self._actions = dict()
		self.reloadAll()
		#temp debug shows
		print("Products (ProductMngr.py __init__()):")
		pprint(self._products)
		print("Actions (ProductMngr.py __init__()):")
		for key, item in self._actions.items():
			print(f"   {item}")

	def getProductsList(self) -> []:
		res = []
		for product in self._products:
			res.append(product['name'])
		return res

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

	def getLogs(self) -> str:
		return self._db.getLogs()

	def addProduct(self, name: str) -> int:
		productId = self._db.newProduct(name)
		self.reloadProducts()
		return productId

	def reloadAll(self) -> None:
		self.reloadProducts()
		self.reloadActions()

	def reloadProducts(self) -> None:
		# self._products.clear()
		self._products = self._db.getProducts()

	def reloadActions(self) -> None:
		self._actions.clear()
		self._actions = self._db.getActions()

	def addAction(self, product: str, weight: float, note: str) -> None:
		productId = self.addProduct(product)
		self._db.newAction(productId, weight, note)
		if weight > 0:
			msg = f'отримано <span style="text-decoration: underline">{product}</span> '\
				f'вагою <span style="text-decoration: underline">{weight}</span>, кг'
		else:
			msg = f'передано в роботу <span style="text-decoration: underline">{product}</span> ' \
			      f'вагою <span style="text-decoration: underline">{-weight}</span>, кг'
		self._db.newLogMsg(msg)
		self.reloadAll()

	def delAction(self, action: Action) -> None:
		self._db.delActionById(action.getId(), action.getProductId())
		msg = f'видалено дію <span style="text-decoration: underline">{action.getName()}</span> '\
				f'вагою <span style="text-decoration: underline">{action.getWeight()}</span>, '
		self._db.newLogMsg(msg)
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
		self.reloadAll()