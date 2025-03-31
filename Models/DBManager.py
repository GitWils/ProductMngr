import datetime
from PyQt6 import QtSql
from Decorators import Singleton, Timing
from Models.Action import Action, Filter

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
                            counter integer default 0)""")
            self.query.clear()
        if 'actions' not in self.con.tables():
            self.query.exec("""create table actions (id integer primary key autoincrement, 
                            product_id integer secondary key,                            
                            weight float,
                            note text,        
                            blocked bool default false,                    
                            str_date text, dt datetime default current_timestamp)""")
            self.query.clear()
        if 'logs' not in self.con.tables():
            self.query.exec("""create table logs (id integer primary key autoincrement, 
                            message text, 
                            str_date text, 
                            dt datetime default current_timestamp, 
                            enable bool default true)""")
            self.query.clear()

    def newProduct(self, name: str) -> int:
        product_id = 0
        self.query.prepare("select id from products where name = ?")
        self.query.addBindValue(name)
        if self.query.exec() and self.query.next():
            product_id = self.query.value(0)
        else:
            self.query.clear()
            self.query.prepare("insert into products(name) values(?)")
            self.query.addBindValue(name)
            if self.query.exec():
                product_id = self.query.lastInsertId()
        self.query.clear()
        return product_id

    def updateProduct(self, name: str, product_id) -> None:
        self.query.exec(f"""update products set name = '{name}' where id = '{product_id}'""")
        self.query.clear()

    def newAction(self, product_id: int, weight: float=0.00, note: str="") -> None:
        date = self.getDateTime()
        self.query.prepare(f"""insert into actions (product_id, weight, note, str_date, dt)
                    values(:product_id, :weight, :note, :str_date, :dt)""")
        self.query.bindValue(':product_id', product_id)
        self.query.bindValue(':weight',     weight)
        self.query.bindValue(':note',       note)
        self.query.bindValue(':str_date',   date['s_date'])
        self.query.bindValue(':dt',         date['datetime'])
        self.query.exec()
        self.query.clear()
        self.query.prepare("""update products set counter=counter+1 where id = :product_id""")
        self.query.bindValue(':product_id', product_id)
        self.query.exec()
        self.query.clear()

    def updateAction(self, action_id: int, product_id: int, weight: float=0.00, note: str="") -> None:
        date = self.getDateTime()
        self.query.prepare("""update actions set  
            product_id = :product_id, weight = :weight, note = :note, str_date = :str_date, dt = :dt
            where id = :id""")
        self.query.bindValue(':product_id', product_id)
        self.query.bindValue(':weight', weight)
        self.query.bindValue(':note', note)
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.bindValue(':id', action_id)
        self.query.exec()
        self.query.clear()

    def getProducts(self) -> []:
        self.query.exec("""select 
                            products.id, products.name, products.counter, sum(actions.weight) as total_amount                        
                            from products 
                            join actions on(products.id = actions.product_id)                            
                            group by actions.product_id""")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = dict({
                    'id':       self.query.value('products.id'),
                    'name':     self.query.value('products.name'),
                    'counter':  self.query.value('products.counter'),
                    'sum':      self.query.value('total_amount')
                })
                lst.append(arr)
                self.query.next()
        self.query.clear()
        return lst

    def getActions(self, fltr: Filter) -> dict[int, Action]:
        self.query.prepare(
            """select * from actions left join products on (products.id=actions.product_id) 
            where actions.product_id=:product_id order by id""")
        self.query.bindValue(':product_id', fltr.getProductId())
        self.query.exec()
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
        self.query.prepare("select id from products where name = :name order by id")
        self.query.bindValue(':name', name)
        self.query.exec()
        res = 0
        if self.query.isActive():
            self.query.first()
            if self.query.isValid():
                res = self.query.value('id')
        self.query.clear()
        return res

    def delActionById(self, action_id: int, product_id: int) -> None:
        self.query.prepare("delete from actions where id = :id")
        self.query.bindValue(':id', action_id)
        self.query.exec()
        self.query.clear()
        self.query.prepare("update products set counter=counter-1 WHERE id = :id")
        self.query.bindValue(':id', product_id)
        self.query.exec()
        self.query.clear()
        self.query.exec("delete from products where counter < 1")
        self.query.clear()

    def getLogs(self, fltr: Filter) -> []:
        """ returns array of logs """
        if fltr.getBeginDate():
            self.query.prepare('select * from logs where dt > :begin and dt < :end order by id desc limit :limit')
            self.query.bindValue(":begin", fltr.getBeginDate())
            self.query.bindValue(":end", fltr.getEndDate())
        else:
            self.query.prepare('select * from logs order by id desc limit :limit')
        self.query.bindValue(':limit', fltr.getLimit())
        self.query.exec()
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = [self.query.value('message'), self.query.value('str_date')]
                lst.append(arr)
                self.query.next()
        self.query.clear()
        return lst

    def newLogMsg(self, msg: str):
        """ new log massage creating """
        date = self.getDateTime()
        self.query.prepare("insert into logs values(null, :message, :str_date, :dt, True)")
        self.query.bindValue(':message', msg)
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        self.query.clear()

    def getWhereFromFilter(self, fltr: Filter, prefix: str) -> str:
        where = ''
        # if filter.get('contracts'):
        #     where = ' and ('
        #     for id in filter['contracts']:
        #         where += f' {prefix}.contract_id = {id} or '
        #     where = where[:-4] + ')'
        # if filter.get('from'):
        #     where += f' and({prefix}.dt > "{filter['from']}") '
        # if filter.get('to'):
        #     where += f' and({prefix}.dt < "{filter['to']}")'
        # if where == '': #if need to find nothing
        #     where = f' and ({prefix}.contract_id = 0)'
        if fltr.getBeginDate():
            where += f" where {prefix}.dt > '{fltr.getBeginDate()}'"
            where += f" and {prefix}.dt < '{fltr.getEndDate()}' "
        return where

    @staticmethod
    def getDateTime() -> {}:
        date = datetime.datetime.now()
        res = dict({'s_date': date.strftime("%H:%M %d.%m.%Y"), 'datetime': str(date)})
        return res

    def __del__(self) -> None:
        self.con.close()