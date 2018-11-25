from Logger import *
from db.Dao import *

class StockList:

    _db = None
    logger = None

    def __init__(self, db):
        self.logger = LoggerFactory.getLogger(self)  
        self._db = db


    
    def findAllStock(self):
        result = list()
        sql = 'select * from STOCK_LIST'
        session = self._db.getSession()
        cur = session.cursor()
        cur.execute(sql)
        qrs = cur.fetchall()
        for row in qrs:
            stkNo = row[0]
            stkName = row[1]
            isin_code = row[2]
            market_date = row[3]
            market_type = row[4]
            industry = row[5]
            entity = {
                "stkNo": stkNo,
                "stkName": stkName,
                "isinCode": isin_code,
                "marketDate": market_date,
                "marketType": market_type,
                "industry": industry
            }
            self.logger.debug("entity: {}", entity)
            result.append(entity)        
        return result


    def findStkById(self, stkNo):
        self.logger.trace('findStkById() exec start, stkNo: {}', stkNo)
        result = None
        sql = 'select * from STOCK_QUOTE where STK_ID = %s order by QUOTE_DATE DESC LIMIT 1' %(stkNo)
        session = self._db.getSession()
        cur = session.cursor()
        cur.execute(sql)
        qrs = cur.fetchall()
        result = qrs if len(qrs) == 1 else None
        return result
