from datetime import datetime

def getDtNow():
    now = datetime.now()
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    return dtString