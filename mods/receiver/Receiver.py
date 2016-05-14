import threading
from ..entities.Alert import Alert
from ..scheduler.Scheduler import Scheduler

class Receiver(threading.Thread):

    def __init__(self, config, scheduler, runEvent):
        threading.Thread.__init__(self)
        self.scheduler = scheduler
        self.config = config
        self.runEvent = runEvent

    def scheduleAlert(self, id, type, key, severity, logmessage):
        alert = Alert(id, type, key, severity, logmessage)
        self.scheduler.addAlert(alert)

    def setConfigOption(self, sectionName, key, value):
        oldValue = self.config.getValue(sectionName, key, "")
        self.config.setValue(sectionName, key, value)
        self.scheduler.addConfigChangedAlert(sectionName, key, oldValue, value)

    def run(self):
        raise ImplementationError()

