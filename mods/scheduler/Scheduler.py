import sched
import time
import threading
import logging

class Scheduler(threading.Thread):

    def __init__(self, config, forwarder, runEvent):
        threading.Thread.__init__(self)
        self.lockEvents = threading.RLock()
        self.alertScheduler = sched.scheduler(time.time, time.sleep)
        self.config = config
        self.forwarder = forwarder
        self.runEvent = runEvent
        self.logger = logging.getLogger("scheduler")

        # dictionary with mapping alertKey -> scheduling event
        self.lockEvents.acquire()
        self.events = {}
        self.lockEvents.release()

    # add alert to queue
    def addAlert(self, alert):
        # get delay from config (in seconds)
        delay = int(self.config.getValue('general', 'alertdelay', '60'))

        # lock on events var
        self.lockEvents.acquire()
        # if alert is a problem
        if alert.getType() == "1":
            # check if alert with that key is already defined
            try:
                self.events[alert.getKey()]
                self.logger.debug("alert with type problem and key %s is already scheduled", 
                                  alert.getKey())
            except KeyError:
                # if no alert exists, schedule alert and save the event in dictionary
                schedulerEvent = self.alertScheduler.enter(delay, 1, self.forwardAlert, 
                                                           argument=(alert,))
                self.events[alert.getKey()] = schedulerEvent
                self.logger.debug("schedule problem alert with key %s in %s seconds", 
                                  alert.getKey(), delay)
        # if alert is a solution
        if alert.getType() == "2":
            # check if alert with that key exists
            try:
                self.events[alert.getKey()]
            # if not: ignore
            except KeyError:
                self.logger.debug("problem alert for resolution with key %s not found", 
                                  alert.getKey())
            else:
                # if event is None, alert is already sent
                if self.events[alert.getKey()] is None:
                    # send resolved alert
                    self.forwardResolvedAlert(alert)
                    self.logger.debug("resolution for problem alert with key %s found, "
                                      "sending resolved message", alert.getKey())
                else:
                    # cancel scheduling
                    self.alertScheduler.cancel(self.events[alert.getKey()])
                    self.logger.debug("resolution for problem alert with key %s found, "
                                      "alert not sent, removing alert from list", alert.getKey())
                # remove event from dictionary
                del self.events[alert.getKey()]
        # release lock on events var
        self.lockEvents.release()

    # send ConfigChangedAlert directly to forwarder object
    def addConfigChangedAlert(self, sectionName, key, oldValue, value):
        self.logger.debug("forward config changed alert")
        self.forwarder.sendConfigChangedAlert(sectionName, key, oldValue, value)


    # forward alert using the configured forwarder
    def forwardAlert(self, alert):
        self.logger.debug("forward alert with key %s", alert.getKey())
        self.forwarder.sendAlert(alert)
        self.lockEvents.acquire()
        self.events[alert.getKey()] = None
        self.lockEvents.release()

    def forwardResolvedAlert(self, alert):
        self.logger.debug("forward resolved alert with key %s", alert.getKey())
        self.forwarder.sendAlert(alert)

    # run the scheduler
    def run(self):
        while self.runEvent.is_set():
            self.alertScheduler.run()
            time.sleep(1)
