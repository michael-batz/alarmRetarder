import time

class Alert:

    def __init__(self, id, type, key, severity, logmessage):
        # store fields
        self.id = id
        self.type = type
        self.key = key
        self.severity = severity
        self.logmessage = logmessage

        # get current timestamp
        self.time = time.localtime()

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def getKey(self):
        return self.key

    def getSeverity(self):
        return self.severity

    def getLogmessage(self):
        return self.logmessage

    def getTime(self):
        return self.time

