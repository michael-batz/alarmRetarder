import requests

class SmsEagleForwarder:

    smsUrl = "http://127.0.0.1/index.php/http_api/send_sms"
    smsUser = "admin"
    smsPassword = "admin"
    smsTarget = "+49151123456789"

    def sendAlert(self, alert):
        # create URL for SMS Eagle
        url = SmsEagleForwarder.smsUrl + "?"
        urlParameters = {
            "login" : SmsEagleForwarder.smsUser,
            "pass" : SmsEagleForwarder.smsPassword,
            "to" : SmsEagleForwarder.smsTarget,
            "message" : alert.getLogmessage()
        }
        requests.get(url, params=urlParameters)
