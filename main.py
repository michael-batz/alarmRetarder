#! /usr/bin/python3

from alarm import Alarm
from SnmpTrapReceiver import SnmpTrapReceiver
import time

alarmStore = {}
trapReceiver = SnmpTrapReceiver(alarmStore)
trapReceiver.start()
time.sleep(10)
print("test1")
print(alarmStore)
time.sleep(10)
print("test2")
print(alarmStore)
time.sleep(10)
print("test4")
print(alarmStore)
time.sleep(100)
alarm1 = Alarm(1, '04-05-2016', 'Dies ist ein Testalarm')
