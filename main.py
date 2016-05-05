#! /usr/bin/python3

from mods.forwarder.StdoutForwarder import StdoutForwarder
from mods.receiver.SnmpTrapReceiver import SnmpTrapReceiver
from mods.scheduler.Scheduler import Scheduler

forwarder = StdoutForwarder()
scheduler = Scheduler(forwarder)
receiver = SnmpTrapReceiver(scheduler)

scheduler.start()
receiver.start()

