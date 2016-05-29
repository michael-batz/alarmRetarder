"""Scheduler module.

This module defines the scheduler part of alarmRetarder.
"""
import sched
import time
import threading
import logging

class Scheduler(threading.Thread):
    """Scheduler class.

    This is the class definition of the alarmRetarder Scheduler, which
    is the main part of the software.

    Attributes:
        config: an object for accessing the configuration.
        forwarder: a forwarder object to forward messages.
        runEvent: a threading.Event for checking the shutdown state of
            the application.
    """

    def __init__(self, config, forwarder, runEvent):
        """inits the Scheduler class."""
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

    def addAlert(self, alert):
        """Adds an alert to Scheduling queue.

        If an alarm was received by a receiver, it will be scheduled
        with this function. This function checks, if the alert is a
        problem or resolution or dupplicate of an existing alarm and
        handles the received alarm in the correct way.

        Args:
            alert: alert object.

        Returns:
            None.
        """
        # get delay from config (in seconds)
        delay = int(self.config.get_value('general', 'alertdelay', '60'))

        # lock on events var
        self.lockEvents.acquire()
        # if alert is a problem
        if alert.get_type() == "1":
            # check if alert with that key is already defined
            try:
                self.events[alert.get_key()]
                self.logger.debug("alert with type problem and key %s is already scheduled",
                                  alert.get_key())
            except KeyError:
                # if no alert exists, schedule alert and save the event in dictionary
                schedulerEvent = self.alertScheduler.enter(delay, 1, self.forwardAlert,
                                                           argument=(alert,))
                self.events[alert.get_key()] = schedulerEvent
                self.logger.debug("schedule problem alert with key %s in %s seconds",
                                  alert.get_key(), delay)
        # if alert is a solution
        if alert.get_type() == "2":
            # check if alert with that key exists
            try:
                self.events[alert.get_key()]
            # if not: ignore
            except KeyError:
                self.logger.debug("problem alert for resolution with key %s not found",
                                  alert.get_key())
            else:
                # if event is None, alert is already sent
                if self.events[alert.get_key()] is None:
                    # send resolved alert
                    self.forwardResolvedAlert(alert)
                    self.logger.debug("resolution for problem alert with key %s found, "
                                      "sending resolved message", alert.get_key())
                else:
                    # cancel scheduling
                    self.alertScheduler.cancel(self.events[alert.get_key()])
                    self.logger.debug("resolution for problem alert with key %s found, "
                                      "alert not sent, removing alert from list", alert.get_key())
                # remove event from dictionary
                del self.events[alert.get_key()]
        # release lock on events var
        self.lockEvents.release()

    def addConfigChangedAlert(self, sectionName, key, oldValue, value):
        """Sends a config changed alert.

        This function will be executed to send an alert to the
        forwarder object if the configuration was changed.

        Args:
            sectionName: name of the changed config section.
            key: key of the changed config option.
            oldValue: old value of the changed config option.
            value: new value of the changed config option.

        Returns:
            None.
        """
        self.logger.debug("forward config changed alert")
        self.forwarder.sendConfigChangedAlert(sectionName, key, oldValue, value)


    def forwardAlert(self, alert):
        """Sends out a problem alert.

        This function sends a problem alert to the forwarder object.

        Args:
            alert: an alert object.

        Returns:
            None.
        """
        self.logger.debug("forward alert with key %s", alert.get_key())
        self.forwarder.sendAlert(alert)
        self.lockEvents.acquire()
        self.events[alert.getKey()] = None
        self.lockEvents.release()

    def forwardResolvedAlert(self, alert):
        """Sends out a resolution alert.

        This function sends a resolution alert to the forwarder object.

        Args:
            alert: an alert object.

        Returns:
            None.
        """
        self.logger.debug("forward resolved alert with key %s", alert.get_key())
        self.forwarder.sendAlert(alert)

    def run(self):
        """Start the Scheduler.

        This is the run function of the Scheduler which starts the
        Scheduler in a new thread.
        """
        while self.runEvent.is_set():
            self.alertScheduler.run()
            time.sleep(1)
