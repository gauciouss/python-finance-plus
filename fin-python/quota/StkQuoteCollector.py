from bs4 import BeautifulSoup
from Logger import *
import requests
import json
from db.Dao import *

class StkQuote:

    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={}&stockNo={}'
    logger = None
    json = None    
    _stock_no = None
    _db = None


    def __init__(self, date, stkNo, db):
        self.logger = LoggerFactory.getLogger(self)        
        self.url = self.url.format(date, stkNo)
        self.logger.info('url: {}', self.url)        
        self._stock_no = stkNo
        self._db = db
    

    def doGetData(self):
        res = requests.get(self.url).text
        self.json = json.loads(res)

    def doSave(self):
        data = self.json['data']
        #["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]
        insert_sql = "INSERT INTO STOCK_QUOTE(STK_ID, QUOTE_DATE, TOTAL_VOLUMN, TURNOVER, OPEN, CLOSE, HIGHEST, LOWEST, DEAL_COUNT) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
        dao = DaoTemplate(self._db.getSession())
        for d in data: 
            dt = d[0].replace('/', '')
            dt = int(dt) + 19110000
            vol = d[1].replace(',', '')
            turnover = d[2].replace(',', '')
            open = d[3]
            high = d[4]
            low = d[5]
            close = d[6]
            #distance = d[7]
            dc = d[8].replace(',', '')
            sql = insert_sql.format(self._stock_no, dt, vol, turnover, open, high, low, close, dc)
            self.logger.info('insert quote sql: {}', sql)
            dao.doSave(sql)
        
    def doWork(self):
        self.doGetData()
        self.doSave()        