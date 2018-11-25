#產生資料連結
#讀取資料
#parse資料
#物件化
#存入資料庫

from quota.StkQuoteCollector import StkQuote
from db.Dao import *
import datetime
import time
from quota.StkList import StockList
import random

class Worker: 

    session_factory = None
    logger = None
    #STAY_TIME = 10

    def __init__(self):
        self.session_factory = SessionFactory()
        self.logger = LoggerFactory.getLogger(self)

    def getAllStk(self):
        s = StockList(self.session_factory)
        rs = s.findAllStock()
        return rs

    def isStockExist(self, stkNo):
        s = StockList(self.session_factory)
        stk = s.findStkById(stkNo)
        return True if stk is not None else False

    def start(self, startYear, startMonth, stkNo):
        nowYear = datetime.datetime.now().year
        #nowMonth = datetime.datetime.now().month
        endYM = int(datetime.datetime.today().strftime('%Y%m'))
        years = list(range(nowYear - startYear + 1))
        sMonth = startMonth

        end_flag = False
        isFirstYear = True
        for y in years:
            rMth = 1
            if(isFirstYear is True):
                isFirstYear = False
                rMth = startMonth

            for m in range(rMth, 13):
                if int(str(y) + str(m)) > endYM:
                    self.logger.info('******* END MONTH: BREAK !!! *******')
                    end_flag = True
                    break
                
                sMonth = m
                d = datetime.date(y + startYear, sMonth, 1)
                ymd = d.strftime('%Y%m%d')
                sq = StkQuote(ymd, stkNo, self.session_factory)
                try:
                    sq.doWork()       
                    time.sleep(random.randint(10, 20))                                 
                except Exception as e:
                    self.logger.error(e)                                 
                            
            if(end_flag is True):
                break            

###################################################################################################

w = Worker()
#print(main.isStockExist(1234))
#main.start(2008, 1, '2317')

stks = w.getAllStk()
for stk in stks:
    stkNo = stk["stkNo"]
    si = int(stkNo)
    if si < 2883:
        continue
    startYear = stk["marketDate"].year
    startYear = 2008 if startYear < 2008 else startYear
    startMonth = stk["marketDate"].month
    if w.isStockExist(stkNo) is False:
        w.start(startYear, startMonth, stkNo)        
#http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20130401&stockNo=1805


