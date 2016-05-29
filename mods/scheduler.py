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
        run_Event: a threading.Event for checking the shutdown state of
            the application.
    """

    def __init__(self, config, forwarder, run_event):
        """inits the Scheduler class."""
        threading.Thread.__init__(self)
        self.__lock_events = threading.RLock()
        self.__alert_scheduler = sched.scheduler(time.time, time.sleep)
        self.__config = config
        self.__forwarder = forwarder
        self.__run_event = run_event
        self.__logger = logging.getLogger("scheduler")

        # dictionary with mapping alert_key -> scheduling event
        self.__lock_events.acquire()
        self.__events = {}
        self.__lock_events.release()

    def add_alert(self, alert):
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
        delay = int(self.__config.get_value('general', 'alertdelay', '60'))

        # lock on events var
        self.__lock_events.acquire()
        # if alert is a problem
        if alert.get_type() == "1":
            # check if alert with that key is already defined
            try:
                self.__events[alert.get_key()]
                self.__logger.debug("alert with type problem and key %s is already scheduled",
                                    alert.get_key())
            except KeyError:
                # if no alert exists, schedule alert and save the event in dictionary
                scheduler_event = self.__alert_scheduler.enter(delay, 1, self.forward_alert,
                                                               argument=(alert,))
                self.__events[alert.get_key()] = scheduler_event
                self.__logger.debug("schedule problem alert with key %s in %s seconds",
                                    alert.get_key(), delay)
        # if alert is a solution
        if alert.get_type() == "2":
            # check if alert with that key exists
            try:
                self.__events[alert.get_key()]
            # if not: ignore
            except KeyError:
                self.__logger.debug("problem alert for resolution with key %s not found",
                                    alert.get_key())
            else:
                # if event is None, alert is already sent
                if self.__events[alert.get_key()] is None:
                    # send resolved alert
                    self.forward_resolved_alert(alert)
                    self.__logger.debug("resolution for problem alert with key %s found, "
                                        "sending resolved message", alert.get_key())
                else:
                    # cancel scheduling
                    self.__alert_scheduler.cancel(self.__events[alert.get_key()])
                    self.__logger.debug("resolution for problem alert with key %s found, "
                                        "alert not sent, removing alert from list", alert.get_key())
                # remove event from dictionary
                del self.__events[alert.get_key()]
        # release lock on events var
        self.__lock_events.release()

    def add_config_changed_alert(self, section_name, key, old_value, value):
        """Sends a config changed alert.

        This function will be executed to send an alert to the
        forwarder object if the configuration was changed.

        Args:
            section_name: name of the changed config section.
            key: key of the changed config option.
            old_value: old value of the changed config option.
            value: new value of the changed config option.

        Returns:
            None.
        """
        self.__logger.debug("forward config changed alert")
        self.__forwarder.send_config_changed_alert(section_name, key, old_value, value)


    def forward_alert(self, alert):
        """Sends out a problem alert.

        This function sends a problem alert to the forwarder object.

        Args:
            alert: an alert object.

        Returns:
            None.
        """
        self.__logger.debug("forward alert with key %s", alert.get_key())
        self.__forwarder.send_alert(alert)
        self.__lock_events.acquire()
        self.__events[alert.getKey()] = None
        self.__lock_events.release()

    def forward_resolved_alert(self, alert):
        """Sends out a resolution alert.

        This function sends a resolution alert to the forwarder object.

        Args:
            alert: an alert object.

        Returns:
            None.
        """
        self.__logger.debug("forward resolved alert with key %s", alert.get_key())
        self.__forwarder.send_alert(alert)

    def run(self):
        """Start the Scheduler.

        This is the run function of the Scheduler which starts the
        Scheduler in a new thread.
        """
        while self.__run_event.is_set():
            self.__alert_scheduler.run()
            time.sleep(1)
