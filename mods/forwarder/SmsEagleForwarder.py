import requests
from .Forwarder import Forwarder


class SmsEagleForwarder(Forwarder):

    def sendAlert(self, alert):
        # create URL for SMS Eagle
        url = self.config.getValue("SmsEagleForwarder", "url", "http://127.0.0.1/index.php/http_api/send_sms")
        urlParameters = {
            "login" : self.config.getValue("SmsEagleForwarder", "user", "admin"),
            "pass" : self.config.getValue("SmsEagleForwarder", "password", "admin"),
            "to" : self.config.getValue("SmsEagleForwarder", "target", "+49123456789"),
            "message" : alert.getLogmessage()
        }
        requests.get(url, params=urlParameters)
