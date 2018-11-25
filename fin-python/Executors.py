import Queue
import threading
from quota.StkQuoteCollector import StkQuote
from db.Dao import *
import datetime
import time
from quota.StkList import StockList
import random

class GetQuoteWorker:

    session_factory = None
    logger = None
    startYear = None
    startMonth = None
    stkNo = None
    wait_min = 30
    wain_max = 40
    
    def __init__(self, start_year, startMonth, stkNo):
        self.session_factory = SessionFactory()
        self.logger = LoggerFactory.getLogger(self)
        self.startYear = start_year
        self.startMonth =  startMonth
        self.stkNo = stkNo

    def doWork(self):
        nowYear = datetime.datetime.now().year        
        endYM = int(datetime.datetime.today().strftime('%Y%m'))
        years = list(range(nowYear - self.startYear + 1))
        sMonth = self.startMonth

        end_flag = False
        isFirstYear = True
        for y in years:
            rMth = 1
            if(isFirstYear is True):
                isFirstYear = False
                rMth = self.startMonth

            for m in range(rMth, 13):
                if int(str(y) + str(m)) > endYM:
                    self.logger.info('******* END MONTH: BREAK !!! *******')
                    end_flag = True
                    break
                
                sMonth = m
                d = datetime.date(y + self.startYear, sMonth, 1)
                ymd = d.strftime('%Y%m%d')
                sq = StkQuote(ymd, self.stkNo, self.session_factory)
                try:
                    sq.doWork()       
                    time.sleep(random.randint(self.wait_min, self.wain_max))                                 
                except Exception as e:
                    self.logger.error(e)                                 
                            
            if(end_flag is True):
                break     
    

class GetQuoteExecutor(threading.Thread):
    
    queue = None

    def __init__(self, queue):        
        self.queue = queue
    
    def run(self):
        stk = self.queue.get()
        startYear = stk["marketDate"].year
        startYear = 2008 if startYear < 2008 else startYear
        startMonth = stk["marketDate"].month
        worker = GetQuoteWorker(stk["stkNo"], startYear, startMonth)
        worker.doWork()

