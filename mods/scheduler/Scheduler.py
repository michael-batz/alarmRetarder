import sched
import time
import threading

class Scheduler(threading.Thread):

    def __init__(self, forwarder):
        threading.Thread.__init__(self)
        self.alertScheduler = sched.scheduler(time.time, time.sleep)
        self.forwarder = forwarder
        # dictionary with mapping alertKey -> scheduling event
        self.events = {}

    # add alert to queue
    def addAlert(self, alert, delay):
        # if alert is a problem
        if alert.getType() == "1":
            # check if alert with that key is already defined
            try:
                self.events[alert.getKey()]
            except KeyError:
                # if no alert exists, schedule alert and save the event in dictionary
                schedulerEvent = self.alertScheduler.enter(delay, 1, self.forwardAlert, argument=(alert,))
                self.events[alert.getKey()] = schedulerEvent
        # if alert is a solution
        if alert.getType() == "2":
            # check if alert with that key exists
            try:
                self.events[alert.getKey()]
            # if not: ignore
            except KeyError:
                pass
            else:
                # if event is None, alert is already sent
                if self.events[alert.getKey()] is None:
                    # send resolved alert
                    self.forwardResolvedAlert(alert)
                else:
                    # cancel scheduling
                    self.alertScheduler.cancel(self.events[alert.getKey()])
                # remove event from dictionary
                del self.events[alert.getKey()]


    # forward alert using the configured forwarder
    def forwardAlert(self, alert):
        self.forwarder.sendAlert(alert)
        self.events[alert.getKey()] = None

    def forwardResolvedAlert(self, alert):
        self.forwarder.sendAlert(alert)

    # run the scheduler
    def run(self):
        while 1:
            self.alertScheduler.run()
            time.sleep(10)
