"""Receiver.

This module defines the abstract class for an alarm receiver. An
alarm receives alarms and schedules them as alert in the scheduler.
"""

import threading
import logging
from ..entities.Alert import Alert
from ..scheduler.Scheduler import Scheduler

class Receiver(threading.Thread):
    """ An alarm receiver.

    This is an abstract class for an alarm receiver.
    A concrete implementation receives an alarm an schedules an alert
    using the scheduler.

    Attributes:
        config: an object for getting or setting configuration values
        scheduler: an object for scheduling alerts
        runEvent: a threading.Event for checking the shutdown state
            of the application.
    """

    def __init__(self, config, scheduler, runEvent):
        """inits the Receiver class."""
        threading.Thread.__init__(self)
        self.scheduler = scheduler
        self.config = config
        self.runEvent = runEvent
        self.logger = logging.getLogger("receiver")

    def scheduleAlert(self, id, type, key, severity, logmessage):
        """Schedules an alert after receiving an alarm.

        Creates an Alert object with the given arguments and sending
        it to the Scheduler.

        Args:
            id: alarm ID
            type: an integer. 1 = PROBLEM, 2 = RESOLUTION
            key: alarm key
            severity: alarm severity
            logmessage: alarm message

        Returns:
            None
        """
        alert = Alert(id, type, key, severity, logmessage)
        self.scheduler.addAlert(alert)

    def setConfigOption(self, sectionName, key, value):
        """Sets a configuration option.

        This function sets an option in the configuration or changes
        an exisiting configuration entry.

        Args:
            sectionName: name of the config section
            key: key of the configuration option
            value: new value of the configuration option

        Returns:
            None
        """
        # get old value and change config
        oldValue = self.config.getValue(sectionName, key, "")
        if oldValue != value:
            self.config.setValue(sectionName, key, value)
            # send ConfigChangedAlert
            self.scheduler.addConfigChangedAlert(sectionName, key, oldValue, value)

    def run(self):
        """Receive function.

        This is the function which has to implement the receiving of
        new alarms. It will be executed as own thread. The
        implementation should look for the runEvent, which will be set
        to FALSE if the application shuts down. If an alarm was
        received the functions scheduleAlert(...) or
        setConfigOption(...) should be executed.

        Args:

        Returns:
            None
        """
        raise ImplementationError()
