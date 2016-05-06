from .Receiver import Receiver
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

class SnmpTrapReceiver(Receiver):

    def run(self):
        # callback function for receiving traps
        def trapReceived(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
            print("Trap Received")
            alertId = ""
            alertType = "" 
            alertKey = ""
            alertSeverity = ""
            alertLogmessage = ""
            for varBind in varBinds:
                varBindName = str(varBind[0])
                varBindValue = str(varBind[1])
                if varBindName == "1.3.6.1.4.1.99999.3.1":
                    alertId = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.2":
                    alertType = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.3":
                    alertKey = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.4":
                    alertSeverity = varBindValue
                elif varBindName == "1.3.6.1.4.1.99999.3.5":
                    alertLogmessage = varBindValue
                print("    " + varBindName  + ": " + varBindValue)
            self.scheduleAlert(alertId, alertType, alertKey, alertSeverity, alertLogmessage)

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
	
        # start dispatcher
        snmpEngine.transportDispatcher.jobStarted(1)
        try:
            snmpEngine.transportDispatcher.runDispatcher()
        except:
            snmpEngine.transportDispatcher.closeDispatcher()
            raise
