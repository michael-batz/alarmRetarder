from .Receiver import Receiver
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

class SnmpTrapReceiver(Receiver):

    def run(self):
        # callback function: shutdown handler
        def checkShutdown(timeNow):
            if self.runEvent.is_set() == False:
                snmpEngine.transportDispatcher.jobFinished(1)

        # callback function: receiving a trap
        def trapReceived(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
            print("Trap Received")
            alertId = ""
            alertType = "" 
            alertKey = ""
            alertSeverity = ""
            alertLogmessage = ""
            configSection = ""
            configKey = ""
            configValue = ""
            trapOid = ""
            for varBind in varBinds:
                varBindName = str(varBind[0])
                varBindValue = str(varBind[1])
                if varBindName == "1.3.6.1.6.3.1.1.4.1.0":
                    trapOid = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.1":
                    alertId = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.2":
                    alertType = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.3":
                    alertKey = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.4":
                    alertSeverity = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.5":
                    alertLogmessage = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.10":
                    configSection = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.11":
                    configKey = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.12":
                    configValue = varBindValue
                print("    " + varBindName  + ": " + varBindValue)
            if trapOid == "1.3.6.1.4.1.99999.3.0.1":
                self.scheduleAlert(alertId, alertType, alertKey, alertSeverity, alertLogmessage)
            elif trapOid == "1.3.6.1.4.1.99999.3.0.2":
                self.setConfigOption(configSection, configKey, configValue)

        # create and configure SNMP engine
        snmpEngine = engine.SnmpEngine()
        config.addTransport(
            snmpEngine,
	        udp.domainName + (1,),
		    udp.UdpTransport().openServerMode(('127.0.0.1', 162))
        )
        config.addV1System(snmpEngine, 'my-area', 'public')
	
        # register callback function
        ntfrcv.NotificationReceiver(snmpEngine, trapReceived)

        # register timer callback function
        snmpEngine.transportDispatcher.registerTimerCbFun(checkShutdown)
	
        # start dispatcher
        snmpEngine.transportDispatcher.jobStarted(1)
        try:
            snmpEngine.transportDispatcher.runDispatcher()
        except:
            snmpEngine.transportDispatcher.closeDispatcher()
            raise
