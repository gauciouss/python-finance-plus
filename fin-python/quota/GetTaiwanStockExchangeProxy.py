import requests
from bs4 import BeautifulSoup
from Logger import Logger, LoggerFactory


class GetTaiwanStockExchangeProxy:

    logger = None
    domain = 'http://bsr.twse.com.tw/bshtm/'    
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
        
    stk_no = ''
    content = ''
    

    def __init__(self, stk_no):
        self.logger = LoggerFactory.getLogger(self)
        self.stk_no = stk_no
        

    def createHeaderPayload(self, text):                
        payload = {}
        soup = BeautifulSoup(text, 'lxml')      
        for item in soup.select('input[type=hidden]'):
            if item.get('value'):
                payload[item.get('name')] = item.get('value')
        
        payload['TextBox_Stkno'] = self.stk_no
        payload['__EVENTTARGET'] =''
        payload['__EVENTARGUMENT'] =''
        payload['__LASTFOCUS'] =''
        payload['RadioButton_Normal'] ='RadioButton_Normal'
        payload['btnOK'] = '查詢'    
        return payload



    def getData(self):   
        rs = requests.session()
        res = rs.get(self.domain + 'bsMenu.aspx', headers = self.headers)
        res.encoding = 'utf-8'        
        payload = self.createHeaderPayload(res.text)
        print(payload)
        res = rs.post(self.domain + '/bsMenu.aspx', data = payload, headers = self.headers)     
        res = rs.get(self.domain + '/bsContent.aspx', headers = self.headers)
        self.content = res.text
        return res.text

    def save2DB(self):
        ctn = self.content
        

        



proxy = GetTaiwanStockExchangeProxy('2317')
print(proxy.getData())    