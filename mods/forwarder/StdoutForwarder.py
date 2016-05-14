from .Forwarder import Forwarder

class StdoutForwarder(Forwarder):

    def sendAlert(self, alert):
        output = "Alert " + alert.getId() + ": "
        output += alert.getLogmessage()

        self.logger.info("Output: %s", output)
        print(output)

    def sendConfigChangedAlert(self, sectionName, key, oldValue, value):
        output = "Config Changed: "
        output += sectionName + "." + key + ": "
        output += oldValue + " -> " + value

        self.logger.info("Output: %s", output)
        print(output)
