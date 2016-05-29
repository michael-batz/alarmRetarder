""" entities module.

This module defines the entities for alarmRetarder.
"""

import time

class Alert(object):
    """Entity Alert.

    This is the definition for the entity alert.

    Attributes:
        alert_id: ID of the alert.
        alert_type: integer of alert type. 1 = PROBLEM, 2 = RESOLUTION
        alert_key: alert key.
        alert_severity: alert severity.
        alert_logmessage: alert message.
    """

    def __init__(self, alert_id, alert_type, alert_key, alert_severity, alert_logmessage):
        """Initialisation of an Alert"""
        self.__alert_id = alert_id
        self.__alert_type = alert_type
        self.__alert_key = alert_key
        self.__alert_severity = alert_severity
        self.__alert_logmessage = alert_logmessage

        # get current timestamp
        self.__alert_time = time.localtime()

    def get_id(self):
        """Returns the ID"""
        return self.__alert_id

    def get_type(self):
        """Returns the type"""
        return self.__alert_type

    def get_key(self):
        """Returns the key"""
        return self.__alert_key

    def get_severity(self):
        """Returns the severity"""
        return self.__alert_severity

    def get_logmessage(self):
        """Returns the logmessage"""
        return self.__alert_logmessage

    def get_time(self):
        """Returns the timestamp"""
        return self.__alert_time

