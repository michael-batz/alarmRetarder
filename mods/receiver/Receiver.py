import threading
from ..entities.Alert import Alert
from ..scheduler.Scheduler import Scheduler

class Receiver(threading.Thread):

    def __init__(self, scheduler):
        threading.Thread.__init__(self)
        self.scheduler = scheduler

    def scheduleAlert(self, id, type, key, severity, logmessage):
        alert = Alert(id, type, key, severity, logmessage)
        self.scheduler.addAlert(alert, 10)

    def run(self):
        raise ImplementationError()
