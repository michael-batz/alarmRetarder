#! /usr/bin/python3

from mods.forwarder.StdoutForwarder import StdoutForwarder
from mods.forwarder.SmsEagleForwarder import SmsEagleForwarder
from mods.receiver.SnmpTrapReceiver import SnmpTrapReceiver
from mods.scheduler.Scheduler import Scheduler
from mods.config.Config import Config
import threading
import time

# get configuration
config = Config("./etc/config.ini")
classNameForwarder = config.getValue('general', 'fowarder', 'StdoutForwarder')
classNameReceiver = config.getValue('general', 'fowarder', 'SnmpTrapReceiver')

# create threading event
runEvent = threading.Event()
runEvent.set()

# create objects
forwarder = eval(classNameForwarder + "(config)")
scheduler = Scheduler(config, forwarder, runEvent)
receiver = eval(classNameReceiver + "(config, scheduler, runEvent)")

# start threads
scheduler.start()
receiver.start()

try:
    while 1:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down alarmRetarder:")
    runEvent.clear()
    print("Shutting down scheduler...")
    scheduler.join()
    print("Shutting down receiver...")
    receiver.join()
    print("...exited")
