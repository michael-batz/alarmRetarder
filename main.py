#! /usr/bin/python3

from mods.forwarder.StdoutForwarder import StdoutForwarder
from mods.forwarder.SmsEagleForwarder import SmsEagleForwarder
from mods.receiver.SnmpTrapReceiver import SnmpTrapReceiver
from mods.scheduler.Scheduler import Scheduler
from mods.config.Config import Config


# get configuration
config = Config("./etc/config.ini")
classNameForwarder = config.getValue('general', 'fowarder', 'StdoutForwarder')
classNameReceiver = config.getValue('general', 'fowarder', 'SnmpTrapReceiver')

# create objects
forwarder = eval(classNameForwarder + "(config)")
scheduler = Scheduler(config, forwarder)
receiver = eval(classNameReceiver + "(config, scheduler)")

# start threads
scheduler.start()
receiver.start()

