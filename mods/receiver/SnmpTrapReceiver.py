"""SnmpTrapReceiver.

This module defines the class SnmpTrapReceiver, which receives alarms
by SNMP trap.
"""

from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from .Receiver import Receiver

class SnmpTrapReceiver(Receiver):
    """Receives alarms by SNMP trap.

    This class is an implementation of the abstract Receiver class and
    receives alarms by SNMP traps. It reads the following parameter
    from the configuration section "SnmpTrapReceiver".

    Configuration:
        listenaddress: interface to listen for SNMP traps.
        listenport: port to listen for SNMP traps.
        community: SNMP community for the trap receiver.
    """

    def run(self):
        """Receives SNMP traps.

        Start the receiving of SNMP traps in a new thread. If a
        received trap is a alertTrap, the alert will be scheduled. If
        the received trap is a configTrap, the configuration option
        will be changed. All other traps will be ignored.
        """
        # callback function: shutdown handler
        def checkShutdown(timeNow):
            """Callback function: shutdown handler.

            This function will be used by pySNMP as callback function
            to check, if the application is on the way to shutdown.

            Args:
                timeNow: the actual time (not used in this case.

            Returns:
                None.
            """
            if self.runEvent.is_set() is False:
                snmpEngine.transportDispatcher.jobFinished(1)

        def trapReceived(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
            """Callback function: receiving a trap.

            This is a callback function used by pySNMP and executed
            each time, if a SNMP trap was received. It checks the type
            of the trap and schedules an alert or sets a configuration
            option.

            Args:
                snmpEngine: pySNMP snmpEngine.
                stateReference: pySNMP stateReference.
                contextEngineId: pySNMP contextEngineId.
                contextName: pySNMP contextName.
                varBinds: pySNMP varBinds.
                cbCtx: pySNMP cbCtx.
            """
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
            if trapOid == "1.3.6.1.4.1.99999.3.0.1":
                self.logger.info("alert trap received: id=%s, type=%s, key=%s, "
                                 "severity=%s, logmsg=%s", alertId, alertType, alertKey,
                                 alertSeverity, alertLogmessage)
                self.scheduleAlert(alertId, alertType, alertKey, alertSeverity, alertLogmessage)
            elif trapOid == "1.3.6.1.4.1.99999.3.0.2":
                self.logger.info("config trap received: section=%s, key=%s, value=%s",
                                 configSection, configKey, configValue)
                self.setConfigOption(configSection, configKey, configValue)
            else:
                self.logger.warn("trap with no matching configuration received")

        # get configuration
        configListenAddress = self.config.get_value("SnmpTrapReceiver", "listenaddress", "127.0.0.1")
        configListenPort = int(self.config.get_value("SnmpTrapReceiver", "listenport", "162"))
        configCommunity = self.config.get_value("SnmpTrapReceiver", "community", "public")

        # create and configure SNMP engine
        snmpEngine = engine.SnmpEngine()
        config.addTransport(snmpEngine,
	                        udp.domainName + (1,),
		                    udp.UdpTransport().openServerMode((configListenAddress, configListenPort)))
        config.addV1System(snmpEngine, 'my-area', configCommunity)

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
