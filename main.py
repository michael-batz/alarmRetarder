#! /usr/bin/python3

from mods.forwarder.StdoutForwarder import StdoutForwarder
from mods.forwarder.SmsEagleForwarder import SmsEagleForwarder
from mods.receiver.SnmpTrapReceiver import SnmpTrapReceiver
from mods.scheduler.Scheduler import Scheduler

forwarder = SmsEagleForwarder()
#forwarder = StdoutForwarder()
scheduler = Scheduler(forwarder)
receiver = SnmpTrapReceiver(scheduler)

scheduler.start()
receiver.start()

