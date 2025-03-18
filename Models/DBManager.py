import datetime
from PyQt6 import QtSql
from Decorators import Singleton, Timing
from Models.Action import Action

from pprint import pprint

class CustomQuery(QtSql.QSqlQuery):
    """ class used for catching sql errors """
    def __init__(self) -> None:
        super().__init__()

    def clear(self) -> None:
        error = self.lastError()
        if error.isValid():
            print(f"Помилка БД: {error.text()}")
        super().clear()

@Singleton
class DBManager:
    def __init__(self) -> None:
        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.con.setDatabaseName('data.s')
        self.con.open()
        self.query = CustomQuery()
        if 'products' not in self.con.tables():
            self.query.exec("""create table products (id integer primary key autoincrement, 
                            name text unique,
                            counter integer default 0, 
                            enable bool default true)""")
        if 'actions' not in self.con.tables():
            self.query.exec("""create table actions (id integer primary key autoincrement, 
                            product_id integer secondary key,                            
                            weight float,
                            note text,                            
                            str_date text, dt datetime default current_timestamp, 
                            enable bool default true)""")
        if 'logs' not in self.con.tables():
            self.query.exec("""create table logs (id integer primary key autoincrement, 
                            message text, 
                            str_date text, 
                            dt datetime default current_timestamp, 
                            enable bool default true)""")
        self.query.clear()

    def newProduct(self, name: str) -> int:
        self.query.exec(f"""insert or ignore into products(name) values('{name}')""")
        productId = self.query.lastInsertId()
        self.query.clear()
        return productId

    def updateProduct(self, name: str, product_id) -> None:
        self.query.exec(f"""update products set name = '{name}' where id = '{product_id}'""")
        self.query.clear()

    def saveAction(self, product_id: int, weight: float=0.00, note: str="") -> None:
        date = self.getDateTime()
        self.query.exec(f"""insert into actions (product_id, weight, note, str_date, dt)
            values('{product_id}', '{weight}', '{note}', '{date['s_date']}', '{date['datetime']}')""")
        self.query.clear()
        self.query.exec(f"""update products set counter=counter+1 where id = '{product_id}'""")
        self.query.clear()

    def updateAction(self, action_id: int, product_id: int, weight: float=0.00, note: str="") -> None:
        date = self.getDateTime()
        self.query.exec(f"""update actions set  
            product_id='{product_id}', 
            weight='{weight}', 
            note = '{note}', 
            str_date = '{date['s_date']}',
            dt = '{date['datetime']}'
            where id = '{action_id}'""")
        self.query.clear()

    def getProducts(self) -> []:
        self.query.exec("select * from products where enable=True order by id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = dict({
                    'id':       self.query.value('id'),
                    'name':     self.query.value('name'),
                    'counter':  self.query.value('counter')
                })
                lst.append(arr)
                self.query.next()
        self.query.clear()
        return lst

    def getActions(self) -> dict[int, Action]:
        self.query.exec(
            "select * from actions left join products on (products.id=actions.product_id) where actions.enable=True order by id")
        lst = {}
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                lst.update({self.query.value('actions.id'):
                                Action(name =  self.query.value('products.name'),
                	                        name_id =   self.query.value('actions.product_id'),
                                            action_id = self.query.value('actions.id'),
                							weight =    self.query.value('weight'),
                                            note =      self.query.value('actions.note'),
                                            date=       self.query.value('str_date')
                                )
                            })
                self.query.next()
        self.query.clear()
        return lst

    def getProductIdByName(self, name: str) -> int:
        self.query.exec(f"select id from products where name='{name}' order by id")
        res = 0
        if self.query.isActive():
            self.query.first()
            if self.query.isValid():
                res = self.query.value('id')
        self.query.clear()
        return res

    def getLogs(self):
        #self.query.exec("select * from logs order by id limit 20")
        self.query.exec("select * from logs order by id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = [self.query.value('message'), self.query.value('str_date')]
                lst.append(arr)
                self.query.next()
        return lst

    def delActionById(self, action_id, product_id) -> None:
        print(f'product_id = {product_id}, action_id = {action_id}')
        self.query.exec(f"delete from actions where id='{action_id}'")
        self.query.clear()
        self.query.exec(f"""update products set counter=counter-1 WHERE id = '{product_id}'""")
        self.query.clear()
        self.query.exec(f"""delete from products where counter < 1""")
        self.query.clear()

    # def delDepartmentById(self, department_id) -> None:
    #     self.query.exec(f"delete from products where id='{department_id}'")
    #     self.query.clear()

    def saveLogMsg(self, msg):
        date = self.getDateTime()
        self.query.prepare("insert into logs values(null, :message, :str_date, :dt, True)")
        self.query.bindValue(':message', msg)
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        self.query.clear()

    @staticmethod
    def getDateTime() -> {}:
        date = datetime.datetime.now()
        res = dict({'s_date': date.strftime("%H:%M %d.%m.%Y"), 'datetime': str(date)})
        return res

    def __del__(self) -> None:
        self.con.close()