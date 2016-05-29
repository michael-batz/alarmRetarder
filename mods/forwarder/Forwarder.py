"""Forwarder.

This module defines an abstract class for the alarm forwarder.

"""
import logging

class Forwarder(object):
    """ An Alarm Forwarder.

    This is an abstract class for the alarm forwarder. Each
    implememtation needs to implement the two functions sendAlert(...)
    and sendConfigChangedAlert(...).

    Attributes:
        config: an object for getting or setting configuration values
    """

    def __init__(self, config):
        """inits the Forwarder class"""
        self.config = config
        self.logger = logging.getLogger("forwarder")

    def sendAlert(self, alert):
        """Sends out an alert.

        This is the function that needs to be implemented. It will be
        executed to send an alert to the user.

        Args:
            alert: alert object to send.

        Returns:
            None
        """
        pass

    def sendConfigChangedAlert(self, sectionName, key, oldValue, value):
        """Sends out a config changed alert.

        This function needs to be implemented to send an alert to the
        user to signal a change of a configuration.

        Args:
            sectionName: string with name of the changed
                configuration value.
            key: the changed configuration key.
            oldValue: old value of the configuration option.
            value: new value if the configuration option.

        Returns:
            None.
        """
        pass
