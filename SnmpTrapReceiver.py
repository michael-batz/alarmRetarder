#! /usr/bin/python3
import  threading
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

class SnmpTrapReceiver(threading.Thread):

    def __init__(self, alarmStore):
        threading.Thread.__init__(self)
        self.alarmStore = alarmStore
        self.alarmCounter = 0

    def run(self):
        # callback function for receiving traps
        def trapReceived(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
            print("Trap Received")
            for varBind in varBinds:
                varBindName = varBind[0]
                varBindValue = varBind[1]
                print("    " + varBindName.prettyPrint() + ": " + varBindValue.prettyPrint())
            
            alarmId = self.alarmCounter
            alarmObject = 'Dies ist eine Testmessage'
            self.alarmCounter = self.alarmCounter + 1
            self.alarmStore[alarmId] = alarmObject

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
