""" Alert module.

This module defines the class for the entity Alert.
"""

import time

class Alert(object):
    """Entity Alert.

    This is the definition for the entity alert.

    Attributes:
        id: ID of the alert.
        type: integer of alert type. 1 = PROBLEM, 2 = RESOLUTION
        key: alert key.
        severity: alert severity.
        logmessage: alert message.
    """

    def __init__(self, id, type, key, severity, logmessage):
        """Initialisation of an Alert"""
        self.id = id
        self.type = type
        self.key = key
        self.severity = severity
        self.logmessage = logmessage

        # get current timestamp
        self.time = time.localtime()

    def getId(self):
        """Returns the ID"""
        return self.id

    def getType(self):
        """Returns the type"""
        return self.type

    def getKey(self):
        """Returns the key"""
        return self.key

    def getSeverity(self):
        """Returns the severity"""
        return self.severity

    def getLogmessage(self):
        """Returns the logmessage"""
        return self.logmessage

    def getTime(self):
        """Returns the timestamp"""
        return self.time

