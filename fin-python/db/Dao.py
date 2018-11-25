import pymysql
from Logger import *
from Util import *


class SessionFactory:

    _size = 20
    _connections = None        
    _instance = None
    _config = {
        'host': '192.168.191.128',
        'port': 3306,
        'user': 'root',
        'pwd': '12345678',
        'db': 'finance_info'
    }


    logger = None

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)
        db = pymysql.connect(host = self._config['host'], port = self._config['port'], user = self._config['user'], passwd = self._config['pwd'], db = self._config['db'])         
        self._connections = [db] * 20        

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger("******* EXIT PROCESS, CLOSE ALL DB CONNECTIONS *******")
        for i, db in enumerate(self._connections):
            if(db.open is True):
                db.close()



    def getSession(self):
        rdb = None
        for i, db in enumerate(self._connections):            
            if(db.open is True):
                rdb = db
                break
        return rdb

class DaoTemplate:

    _db = None
    logger = None

    def __init__(self, db):
        self.logger = LoggerFactory.getLogger(self)
        self._db = db
    
    def doSave(self, sql):
        self.logger.trace('start exec doSave(), sql: {}', sql)
        cur = self._db.cursor()
        cur.execute(sql)
        self._db.commit()        

    
    



