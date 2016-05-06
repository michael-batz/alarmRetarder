#! /usr/bin/python3

from mods.forwarder.StdoutForwarder import StdoutForwarder
from mods.forwarder.SmsEagleForwarder import SmsEagleForwarder
from mods.receiver.SnmpTrapReceiver import SnmpTrapReceiver
from mods.scheduler.Scheduler import Scheduler
from mods.config.Config import Config

config = Config("./etc/config.ini")
forwarder = SmsEagleForwarder(config)
#forwarder = StdoutForwarder(config)
scheduler = Scheduler(config, forwarder)
receiver = SnmpTrapReceiver(config, scheduler)

scheduler.start()
receiver.start()

