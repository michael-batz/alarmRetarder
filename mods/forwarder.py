"""forwarder.

This module defines the forwarding part of alarm forwarder.

"""
import logging
import requests

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
        self._config = config
        self._logger = logging.getLogger("forwarder")

    def send_alert(self, alert):
        """Sends out an alert.

        This is the function that needs to be implemented. It will be
        executed to send an alert to the user.

        Args:
            alert: alert object to send.

        Returns:
            None
        """
        pass

    def send_config_changed_alert(self, section_name, key, old_value, value):
        """Sends out a config changed alert.

        This function needs to be implemented to send an alert to the
        user to signal a change of a configuration.

        Args:
            section_name: string with name of the changed
                configuration value.
            key: the changed configuration key.
            old_value: old value of the configuration option.
            value: new value if the configuration option.

        Returns:
            None.
        """
        pass

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

    def send_alert(self, alert):
        """Sends an alert.

        Sends out an alert using the SMS Eagle HTTP API.

        Args:
            alert: an alert object to send.

        Returns:
            None.
        """
        self.send_message(alert.get_logmessage())

    def send_config_changed_alert(self, section_name, key, old_value, value):
        """Sends out a config changed alert.

        Sends out a config changed alert using the SMS Eagle HTTP API.

        Args:
            section_name: string with name of the changed
                configuration value.
            key: the changed configuration key.
            old_value: old value of the configuration option.
            value: new value if the configuration option.

        Returns:
            None.
        """
        # check, if target phone number was changed
        if section_name == "SmsEagleForwarder" and key == "target":
            message = "Agent logged out (new agent is " + value + ")"
            self.send_message(message, old_value)
            message = "Agent logged in (old agent was " + old_value + ")"
            self.send_message(message)
        # if not, send config changed message
        else:
            message = "Config Changed: "
            message += section_name + "." + key + ": "
            message += old_value + " -> " + value
            self.send_message(message)

    def send_message(self, message, target=None):
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
        url = self._config.get_value("SmsEagleForwarder", "url",
                                     "http://127.0.0.1/index.php/http_api/send_sms")

        # check if a value for target is set
        if target is None:
            target = self._config.get_value("SmsEagleForwarder", "target", "+49123456789")

        # setup URL parameters
        url_parameters = {
            "login" : self._config.get_value("SmsEagleForwarder", "user", "admin"),
            "pass" : self._config.get_value("SmsEagleForwarder", "password", "admin"),
            "to" : target,
            "message" : message
        }

        # log message
        self._logger.info("Send SMS to %s: %s", target, message)

        # send HTTP GET request
        try:
            requests.get(url, params=url_parameters)
        except:
            self._logger.error("Error sending SMS. Problem in communication with SMS Eagle")

class StdoutForwarder(Forwarder):
    """Forwards alerts using standard output.

    This class is an implementation of the abstract Forwarder class
    and sends out alerts using standard output.
    """

    def send_alert(self, alert):
        """Sends an alert.

        Prints out an alert on standard output.

        Args:
            alert: an alert object to print.

        Returns:
            None.
        """
        output = "Alert " + alert.get_id() + ": "
        output += alert.get_logmessage()

        self._logger.info("Output: %s", output)
        print(output)

    def send_config_changed_alert(self, section_name, key, old_value, value):
        """Sends out a config changed alert.

        Prints out a config changed alert on standard output.

        Args:
            section_name: string with name of the changed
                configuration value.
            key: the changed configuration key.
            old_value: old value of the configuration option.
            value: new value if the configuration option.

        Returns:
            None.
        """
        output = "Config Changed: "
        output += section_name + "." + key + ": "
        output += old_value + " -> " + value

        self._logger.info("Output: %s", output)
        print(output)
