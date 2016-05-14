import requests
from .Forwarder import Forwarder


class SmsEagleForwarder(Forwarder):

    def sendAlert(self, alert):
        self.sendMessage(alert.getLogmessage())
       
    def sendConfigChangedAlert(self, sectionName, key, oldValue, value):
        # check, if target phone number was changed
        if sectionName == "SmsEagleForwarder" & key == "target":
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
        # create URL for SMS Eagle
        url = self.config.getValue("SmsEagleForwarder", "url", "http://127.0.0.1/index.php/http_api/send_sms")

        # check if a value for target is set
        if target is None:
            target = self.config.getValue("SmsEagleForwarder", "target", "+49123456789")

        # setup URL parameters
        urlParameters = {
            "login" : self.config.getValue("SmsEagleForwarder", "user", "admin"),
            "pass" : self.config.getValue("SmsEagleForwarder", "password", "admin"),
            "to" : target,
            "message" : message
        }

        # log message
        self.logger.info("Send SMS to %s: %s", target, message)

        # send HTTP GET request
        requests.get(url, params=urlParameters)
 
