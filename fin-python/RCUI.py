import sys
from Logger import *
from PyQt5.QtWidgets import *

class RiskControlUI(QWidget):

    logger = None
    AP_NAME = 'Risk Control'

    def __init__(self, apName):
        self.logger = LoggerFactory.getLogger(self)
        super(self.__class__, self).__init__()
        if apName != None and apName != '':
            self.AP_NAME = apName
        self.setWindowTitle(self.AP_NAME)
        self.doLayout()
        self.show()
    
    def doLayout(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('call'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('call'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('call'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('call'))
        self.tableWidget.setItem(0, 4, QTableWidgetItem('call'))        
        self.tableWidget.setItem(0, 5, QTableWidgetItem(''))
        self.tableWidget.setItem(0, 6, QTableWidgetItem('put'))
        self.tableWidget.setItem(0, 7, QTableWidgetItem('put'))
        self.tableWidget.setItem(0, 8, QTableWidgetItem('put'))
        self.tableWidget.setItem(0, 9, QTableWidgetItem('put'))
        self.tableWidget.setItem(0, 10, QTableWidgetItem('put'))

        self.tableWidget.setItem(1, 0, QTableWidgetItem('理論價'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem('hedgeV'))
        self.tableWidget.setItem(1, 2, QTableWidgetItem('IV'))
        self.tableWidget.setItem(1, 3, QTableWidgetItem('市價 '))
        self.tableWidget.setItem(1, 4, QTableWidgetItem('庫存 '))        
        self.tableWidget.setItem(1, 5, QTableWidgetItem('履約價'))
        self.tableWidget.setItem(1, 6, QTableWidgetItem('庫存 '))        
        self.tableWidget.setItem(1, 7, QTableWidgetItem('市價'))
        self.tableWidget.setItem(1, 8, QTableWidgetItem('IV'))
        self.tableWidget.setItem(1, 9, QTableWidgetItem('hedgeV'))
        self.tableWidget.setItem(1, 10, QTableWidgetItem('理論價'))


        self.setStrikePrice()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
        
    #設定履約價
    def setStrikePrice(self):
        stkP_range = range(10000, 12000, 100)
        y = 2        
        for p in stkP_range:
            self.tableWidget.setItem(y, 5, QTableWidgetItem(str(p)))
            y = y + 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RiskControlUI('aa')
    sys.exit(app.exec_())