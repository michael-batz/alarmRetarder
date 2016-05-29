"""SmsEagleForwarder module.

This module defines the class SmsEagleForwarder which forwards alerts
using the SMSEagle SMS Gateway.
"""
import requests
from .Forwarder import Forwarder

class SmsEagleForwarder(Forwarder):
    """Forwards alerts using the SMSEagle SMS Gateway.

    This class is an implementation of the abstract Forwarder class.
    It sends out alerts using the SMSEagle SMS Gateway. It reads the
    following parameters from the configuration section
    "SmsEagleForwarder"

    Configuration:
        url: URL of the SMS Eagle HTTP API
        user: username of the SMS Eagle HTTP API
        password: password of the SMS Eagle HTTP API
        target: target phone number
    """

    def sendAlert(self, alert):
        """Sends an alert.

        Sends out an alert using the SMS Eagle HTTP API.

        Args:
            alert: an alert object to send.

        Returns:
            None.
        """
        self.sendMessage(alert.getLogmessage())

    def sendConfigChangedAlert(self, sectionName, key, oldValue, value):
        """Sends out a config changed alert.

        Sends out a config changed alert using the SMS Eagle HTTP API.

        Args:
            sectionName: string with name of the changed
                configuration value.
            key: the changed configuration key.
            oldValue: old value of the configuration option.
            value: new value if the configuration option.

        Returns:
            None.
        """
        # check, if target phone number was changed
        if sectionName == "SmsEagleForwarder" and key == "target":
            message = "Agent logged out (new agent is " + value + ")"
            self.sendMessage(message, oldValue)
            message = "Agent logged in (old agent was " + oldValue + ")"
            self.sendMessage(message)
        # if not, send config changed message
        else:
            message = "Config Changed: "
            message += sectionName + "." + key + ": "
            message += oldValue + " -> " + value
            self.sendMessage(message)

    def sendMessage(self, message, target=None):
        """Sends out a message to the SMSEagle HTTP API.

        This function sends out a message to the SMSEagle HTTP API.
        It gets the needed parameters from the configuration. There
        is the possibility to overwrite the target option.

        Args:
            message: string with the alert message.
            target: string with a target phone number or None, if the
                configuration value should be used.
        """
        # create URL for SMS Eagle
        url = self.config.get_value("SmsEagleForwarder", "url",
                                   "http://127.0.0.1/index.php/http_api/send_sms")

        # check if a value for target is set
        if target is None:
            target = self.config.get_value("SmsEagleForwarder", "target", "+49123456789")

        # setup URL parameters
        urlParameters = {
            "login" : self.config.get_value("SmsEagleForwarder", "user", "admin"),
            "pass" : self.config.get_value("SmsEagleForwarder", "password", "admin"),
            "to" : target,
            "message" : message
        }

        # log message
        self.logger.info("Send SMS to %s: %s", target, message)

        # send HTTP GET request
        try:
            requests.get(url, params=urlParameters)
        except:
            self.logger.error("Error sending SMS. Problem in communication with SMS Eagle")
