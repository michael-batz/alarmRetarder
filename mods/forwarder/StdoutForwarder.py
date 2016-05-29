""" StdoutForwarder.

This module defines the class StdoutForwarder, which sends alerts out
using standard output.
"""
from .Forwarder import Forwarder

class StdoutForwarder(Forwarder):
    """Forwards alerts using standard output.

    This class is an implementation of the abstract Forwarder class
    and sends out alerts using standard output.
    """

    def sendAlert(self, alert):
        """Sends an alert.

        Prints out an alert on standard output.

        Args:
            alert: an alert object to print.

        Returns:
            None.
        """
        output = "Alert " + alert.getId() + ": "
        output += alert.getLogmessage()

        self.logger.info("Output: %s", output)
        print(output)

    def sendConfigChangedAlert(self, sectionName, key, oldValue, value):
        """Sends out a config changed alert.

        Prints out a config changed alert on standard output.

        Args:
            sectionName: string with name of the changed
                configuration value.
            key: the changed configuration key.
            oldValue: old value of the configuration option.
            value: new value if the configuration option.

        Returns:
            None.
        """
        output = "Config Changed: "
        output += sectionName + "." + key + ": "
        output += oldValue + " -> " + value

        self.logger.info("Output: %s", output)
        print(output)
