#! /usr/bin/python3

from mods.forwarder.StdoutForwarder import StdoutForwarder
from mods.forwarder.SmsEagleForwarder import SmsEagleForwarder
from mods.receiver.SnmpTrapReceiver import SnmpTrapReceiver
from mods.scheduler.Scheduler import Scheduler
from mods.config.config import Config
import threading
import time
import logging
import logging.config
import os

# get directory name
basedir = os.path.dirname(__file__)

# get configuration
config = Config(basedir + "/etc/config.conf")
classNameForwarder = config.get_value('general', 'forwarder', 'StdoutForwarder')
classNameReceiver = config.get_value('general', 'receiver', 'SnmpTrapReceiver')

# create logging config
logging.basedir = basedir + "/logs"
logging.config.fileConfig(basedir + "/etc/logging.conf")

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
