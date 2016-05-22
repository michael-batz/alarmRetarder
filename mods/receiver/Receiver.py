import threading
import logging
from ..entities.Alert import Alert
from ..scheduler.Scheduler import Scheduler

class Receiver(threading.Thread):

    def __init__(self, config, scheduler, runEvent):
        threading.Thread.__init__(self)
        self.scheduler = scheduler
        self.config = config
        self.runEvent = runEvent
        self.logger = logging.getLogger("receiver")

    def scheduleAlert(self, id, type, key, severity, logmessage):
        # create and schedule alert
        alert = Alert(id, type, key, severity, logmessage)
        self.scheduler.addAlert(alert)

    def setConfigOption(self, sectionName, key, value):
        # get old value and change config
        oldValue = self.config.getValue(sectionName, key, "")
        if oldValue != value:
            self.config.setValue(sectionName, key, value)
            # send ConfigChangedAlert
            self.scheduler.addConfigChangedAlert(sectionName, key, oldValue, value)

    def run(self):
        raise ImplementationError()
