from .Forwarder import Forwarder

class StdoutForwarder(Forwarder):

    def sendAlert(self, alert):
        output = "Alert: "
        output += alert.getId()
        output += "\n"
        output += alert.getLogmessage()
        output += "\n"

        self.logger.info("Output: %s", output)
        print(output)

    def sendConfigChangedAlert(self, sectionName, key, oldValue, value):
        output = "Config Changed: "
        output += sectionName + "." + key + ": "
        output += oldValue + " -> " + value

        self.logger.info("Output: %s", output)
        print(output)
