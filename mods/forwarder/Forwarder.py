import logging

class Forwarder:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("forwarder")

    def sendAlert(self, alert):
        pass

    def sendConfigChangedAlert(self, sectionName, key, oldValue, value):
        pass
