#! /usr/bin/python3

import threading
import time
import logging
import logging.config
import os
from mods.forwarder import StdoutForwarder
from mods.forwarder import SmsEagleForwarder
from mods.receiver import SnmpTrapReceiver
from mods.scheduler import Scheduler
from mods.config import Config

# get directory name
basedir = os.path.dirname(__file__)

# get configuration
config = Config(basedir + "/etc/config.conf")
class_name_forwarder = config.get_value('general', 'forwarder', 'StdoutForwarder')
class_name_receiver = config.get_value('general', 'receiver', 'SnmpTrapReceiver')

# create logging config
logging.basedir = basedir + "/logs"
logging.config.fileConfig(basedir + "/etc/logging.conf")

# create threading event
run_event = threading.Event()
run_event.set()

# create objects
forwarder = eval(class_name_forwarder + "(config)")
scheduler = Scheduler(config, forwarder, run_event)
receiver = eval(class_name_receiver + "(config, scheduler, run_event)")

# start threads
scheduler.start()
receiver.start()

try:
    while 1:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down alarmRetarder:")
    run_event.clear()
    print("Shutting down scheduler...")
    scheduler.join()
    print("Shutting down receiver...")
    receiver.join()
    print("...exited")
