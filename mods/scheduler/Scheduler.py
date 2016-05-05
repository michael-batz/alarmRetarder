import sched
import time
import threading

class Scheduler(threading.Thread):

    def __init__(self, forwarder):
        threading.Thread.__init__(self)
        self.alertScheduler = sched.scheduler(time.time, time.sleep)
        self.forwarder = forwarder

    # add alert to queue
    def addAlert(self, alert, delay):
        self.alertScheduler.enter(delay, 1, self.forwardAlert, argument=(alert,))


    # forward alert using the configured forwarder
    def forwardAlert(self, alert):
        self.forwarder.sendAlert(alert)

    # run the scheduler
    def run(self):
        while 1:
            self.alertScheduler.run()
            time.sleep(10)
