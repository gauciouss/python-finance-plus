import os
import platform
import datetime


logPath = 'C:/Users/admin/Desktop/mypython.log'
if platform.system() == 'Windows':
    if os.path.exists(logPath) is True:
        file_create_time = os.path.getctime(logPath) if platform.system() == 'Windows' else os.stat(logPath).st_birthtime 
        print(file_create_time)
        print(datetime.date)
