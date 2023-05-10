from datetime import datetime
from calendar import day_name
from json import load
from time import sleep
from window import Window
from threading import Thread, _active
from ctypes import pythonapi, py_object

def time_to_next_alarm():
    next_alarm = ["", "", -1.0] 
    f = open("data/alarms.json")
    content = load(f)
    current = datetime.today().now().time().strftime("%H:%M:%S")
    day = day_name[datetime.today().weekday()].upper()
    for i in content['items']:
        if(day in i['day']):
            d = (datetime.strptime(i['time'], "%H:%M:%S") - datetime.strptime(current, "%H:%M:%S"))
            if(d.days != 0):
                continue
            if(d.total_seconds() < next_alarm[2] or next_alarm[2] == -1.0):
                next_alarm[0] = i['reason']
                next_alarm[1] = i['description']
                next_alarm[2] = d.total_seconds()
    return next_alarm
def time_to_tommorow():
    current = datetime.strptime(datetime.today().now().time().strftime("%H:%M:%S"), "%H:%M:%S")
    tommorow = datetime.strptime("00:00:00", "%H:%M:%S")
    return (tommorow - current).seconds

def alarm():
    s = 5 # Refresh time
    while True:
        t = time_to_next_alarm()
        try:
            print(t[2])
            if(t[2] <= s):
                sleep(t[2])
                win = Thread(target=Window, args=(t[0], t[1]))
                win.setName("Window")
                win.start()
            sleep(s)
        except ValueError:
            if(time_to_tommorow() < s):
                sleep(time_to_tommorow)
            sleep(s)