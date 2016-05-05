from .Forwarder import Forwarder

class StdoutForwarder(Forwarder):

    def sendAlert(self, alert):
        output = "Alert "
        output += alert.getId()
        output += "\n"
        output += alert.getLogmessage()
        output += "\n"
        print(output)
