import Adafruit_DHT as adht 
import time 
from datetime import datetime
import logging 
import threading 
from threading import Timer
import mysql.connector
import os

#uncomment timer class to activate timer
'''class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue: # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")'''

def getMac():
    #get eth0 mac
    try:
        macEth = open('/sys/class/net/eth0/address').read()
    except:
        macEth = "00:00:00:00:00:00"
    macEth = macEth[9:17]
    #get wlan0 mac
    try:
        macWlan = open('/sys/class/net/wlan0/address').read()
    except:
        macWlan = "00:00:00:00:00:00"
    macWlan = macWlan[9:17]
    streamEth = os.popen("cat /sys/class/net/eth0/carrier")
    outEth = streamEth.read()
    if(outEth == "1"):
        return macEth
    return macWlan

#def tick():
db = mysql.connector.connect(
    host = "devilberry.local",
    port = "3306",
    user = "grafana",
    password = "DB_R4CkG",
    database = "temperatura"
)

humidity, temperature = adht.read_retry(adht.DHT22, 12)
timestamp = str(time.time())[0:10]
cursor = db.cursor()
if humidity is not None and temperature is not None:
    sqlQuery = "select id_sen from sensore where mac=%s;"
    mac = getMac()
    print(mac)
    val = [mac]
    cursor.execute(sqlQuery, val)
    id = cursor.fetchall()[0][0]
    print(id)
    val = [id, temperature, humidity, timestamp]
    sql = "insert into lettura values (null, %s, %s, %s, %s);"
    cursor.execute(sql, val)
    db.commit()
else:
    print("Failed to retrieve data from humidity sensor")

#uncomment to set the interval (es 300ms)for infinite timer
'''t = InfiniteTimer(300, tick)
t.start()'''

