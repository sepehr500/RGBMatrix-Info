import threading
import time
import Queue
import datetime
from StandbyScreen import StandbyScreen
from NewsBrief import NewsBrief
from WeatherBrief import WeatherBrief




def TimeConditionMinuteInter(interval):
    result = datetime.datetime.now().minute % interval
    return True if result == 0 else False

def Every15Min():
    return TimeConditionMinuteInter(15)
def EveryHour():
    return True if  datetime.datetime.now().minute   == 0 else False
def Every15Seconds():
    print(datetime.datetime.now().second)
    return True if datetime.datetime.now().second % 120 == 0 else False




def addToQueue(e, screenFunction , condition):
    
    global q
    now = datetime.datetime.now()
    while True:
        time.sleep(1)
        if (condition()):
            print("screen added to queue")
            q.put(screenFunction)
            e.set()
            time.sleep(120)
            


q = Queue.Queue()
e = threading.Event()
#configure screens
#threading.Thread(target=addToQueue,args=(e,NewsBrief.playScreen,Every15Seconds ,)).start()
threading.Thread(target=addToQueue,args=(e,WeatherBrief.playScreen,Every15Min ,)).start()


while True:
    if (q.empty()):
        e.clear()
        StandbyScreen.standby(e)
    else:
         print("broke out")
         method = q.get()
         method()
    






