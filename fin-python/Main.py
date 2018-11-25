import sys
from Logger import *
from PyQt5.QtWidgets import *



class Main(QWidget):

    logger = None
    AP_NAME = 'Risk Control'

    label_FIMTX = None
    label_FIMTX_Price = None        
    label_on_date = None
    label_on_date_value = None        
    label_left_days = None
    label_left_days_value = None    
    label_risk_exposure = None
    label_risk_exposure_value = None    
    label_rent = None
    label_rent_value = None

    label_iv = None
    input_iv = None


    def __init__(self, apName):
        self.logger = LoggerFactory.getLogger(self)
        super(self.__class__, self).__init__()
        if apName != None and apName != '':
            self.AP_NAME = apName
        self.startWindow()
        self.show()

    
    def startWindow(self):
        self.setWindowTitle(self.AP_NAME)

    
    def setLayout(self):
        self.createTable()
        



    def Base_Info(self):
        self.label_FIMTX = QLabel()
        self.label_FIMTX_Price = QLabel()
        self.label_FIMTX.setText('小台市價')
        
        self.label_on_date = QLabel()
        self.label_on_date_value = QLabel()
        self.label_on_date.setText('到期日')

        self.label_left_days = QLabel()
        self.label_left_days_value = QLabel()
        self.label_left_days.setText('剩餘天數')

        self.label_risk_exposure = QLabel()
        self.label_risk_exposure_value = QLabel()
        self.label_risk_exposure.setText('曝險部位金額')

        self.label_rent = QLabel()
        self.label_rent_value = QLable()
        self.label_rent.setText('每日可收金額')        

        self.label_iv = QLabel()
        self.label_iv.setText('IV')
        self.input_iv = QLineEdit()
    





if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main = Main('風險控制')
    sys.exit(app.exec_())