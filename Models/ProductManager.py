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
		print("Products:")
		pprint(self._products)
		print("Actions (ProductMngr.py __init__()):")
		for key, item in self._actions.items():
			print(f"   {item}")

	def getProductsList(self) -> []:
		res = []
		for product in self._products:
			res.append(product['name'])
		return res

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
		productId = self._db.saveProduct(name)
		if productId is None:
			productId = self._db.getProductIdByName(name)
		self.reloadProducts()
		return productId

	def reloadAll(self) -> None:
		self.reloadProducts()
		self.reloadActions()

	def reloadProducts(self) -> None:
		self._products = self._db.getProducts()

	def reloadActions(self) -> None:
		self._actions.clear()
		self._actions = self._db.getActions()
	def addAction(self, product: str, weight: float, note: str) -> None:
	# def addPost(self, post: Post) -> None:
		productId = self.addProduct(product)
		self._db.saveAction(product, productId, weight, note)
		msg = f'передано <span style="text-decoration: underline">{product}</span> '\
			f'вагою <span style="text-decoration: underline">{product}</span>, кг'
		self._db.saveLogMsg(msg)
		self.reloadActions()

	def delPost(self, action: Action) -> None:
		self._db.delActionById(action.getId(), action.getProductId())
		msg = f'видалено посаду <span style="text-decoration: underline">{action.getName()}</span> '\
				f'у відділі <span style="text-decoration: underline">{action.getName()}</span>, '
		self._db.saveLogMsg(msg)
		self.reloadActions()

	def editPost(self,
	             original_post: Action,
	             department: str,
	             post: str,
	             cnt: int
	             ) -> None:

		self.reloadActions()