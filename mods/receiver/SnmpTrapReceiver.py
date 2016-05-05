from .Receiver import Receiver
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

class SnmpTrapReceiver(Receiver):

    def run(self):
        # callback function for receiving traps
        def trapReceived(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
            print("Trap Received")
            for varBind in varBinds:
                varBindName = varBind[0]
                varBindValue = varBind[1]
                print("    " + varBindName.prettyPrint() + ": " + varBindValue.prettyPrint())
            alertType = "alert type"
            alertKey = "alert key"
            alertId = "12"
            alertSeverity = 5
            alertLogmessage = "This is a test alert"
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
