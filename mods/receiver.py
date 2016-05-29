"""receiver.

This module defines the abstract class for an alarm receiver. An
alarm receives alarms and schedules them as alert in the scheduler.
"""

import threading
import logging
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from .entities import Alert

class Receiver(threading.Thread):
    """ An alarm receiver.

    This is an abstract class for an alarm receiver.
    A concrete implementation receives an alarm an schedules an alert
    using the scheduler.

    Attributes:
        config: an object for getting or setting configuration values
        scheduler: an object for scheduling alerts
        run_event: a threading.Event for checking the shutdown state
            of the application.
    """

    def __init__(self, config, scheduler, run_event):
        """inits the Receiver class."""
        threading.Thread.__init__(self)
        self._scheduler = scheduler
        self._config = config
        self._run_event = run_event
        self._logger = logging.getLogger("receiver")

    def schedule_alert(self, alert_id, alert_type, alert_key, alert_severity, alert_logmessage):
        """Schedules an alert after receiving an alarm.

        Creates an Alert object with the given arguments and sending
        it to the Scheduler.

        Args:
            alert_id: alarm ID
            alert_type: an integer. 1 = PROBLEM, 2 = RESOLUTION
            alert_key: alarm key
            alert_severity: alarm severity
            alert_logmessage: alarm message

        Returns:
            None
        """
        alert = Alert(alert_id, alert_type, alert_key, alert_severity, alert_logmessage)
        self._scheduler.add_alert(alert)

    def set_config_option(self, section_name, key, value):
        """Sets a configuration option.

        This function sets an option in the configuration or changes
        an exisiting configuration entry.

        Args:
            section_name: name of the config section
            key: key of the configuration option
            value: new value of the configuration option

        Returns:
            None
        """
        # get old value and change config
        old_value = self.__config.get_value(section_name, key, "")
        if old_value != value:
            self.__config.set_value(section_name, key, value)
            # send ConfigChangedAlert
            self._scheduler.add_config_changed_alert(section_name, key, old_value, value)

    def run(self):
        """Receive function.

        This is the function which has to implement the receiving of
        new alarms. It will be executed as own thread. The
        implementation should look for the runEvent, which will be set
        to FALSE if the application shuts down. If an alarm was
        received the functions schedule_alert(...) or
        set_config_option(...) should be executed.

        Args:

        Returns:
            None
        """
        raise ImplementationError()

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
        def check_shutdown(time_now):
            """Callback function: shutdown handler.

            This function will be used by pySNMP as callback function
            to check, if the application is on the way to shutdown.

            Args:
                timeNow: the actual time (not used in this case.

            Returns:
                None.
            """
            if self._run_event.is_set() is False:
                snmp_engine.transportDispatcher.jobFinished(1)

        def trap_received(snmp_engine, state_reference, context_engine_id,
                          context_name, var_binds, cb_ctx):
            """Callback function: receiving a trap.

            This is a callback function used by pySNMP and executed
            each time, if a SNMP trap was received. It checks the type
            of the trap and schedules an alert or sets a configuration
            option.

            Args:
                snmp_engine: pySNMP snmpEngine.
                state_reference: pySNMP stateReference.
                context_engine_id: pySNMP contextEngineId.
                context_name: pySNMP contextName.
                var_binds: pySNMP varBinds.
                cb_Ctx: pySNMP cbCtx.
            """
            alert_id = ""
            alert_type = ""
            alert_key = ""
            alert_severity = ""
            alert_logmessage = ""
            config_section = ""
            config_key = ""
            config_value = ""
            trap_oid = ""
            for var_bind in var_binds:
                var_bind_name = str(var_bind[0])
                var_bind_value = str(var_bind[1])
                if var_bind_name == "1.3.6.1.6.3.1.1.4.1.0":
                    trap_oid = var_bind_value
                elif var_bind_name == "1.3.6.1.4.1.99999.3.1":
                    alert_id = var_bind_value
                elif var_bind_name == "1.3.6.1.4.1.99999.3.2":
                    alert_type = var_bind_value
                elif var_bind_name == "1.3.6.1.4.1.99999.3.3":
                    alert_key = var_bind_value
                elif var_bind_name == "1.3.6.1.4.1.99999.3.4":
                    alert_severity = var_bind_value
                elif var_bind_name == "1.3.6.1.4.1.99999.3.5":
                    alert_logmessage = var_bind_value
                elif var_bind_name == "1.3.6.1.4.1.99999.3.10":
                    config_section = var_bind_value
                elif var_bind_name == "1.3.6.1.4.1.99999.3.11":
                    config_key = var_bind_value
                elif var_bind_name == "1.3.6.1.4.1.99999.3.12":
                    config_value = var_bind_value
            if trap_oid == "1.3.6.1.4.1.99999.3.0.1":
                self._logger.info("alert trap received: id=%s, type=%s, key=%s, "
                                  "severity=%s, logmsg=%s", alert_id, alert_type, alert_key,
                                  alert_severity, alert_logmessage)
                self.schedule_alert(alert_id, alert_type, alert_key,
                                    alert_severity, alert_logmessage)
            elif trap_oid == "1.3.6.1.4.1.99999.3.0.2":
                self.__logger.info("config trap received: section=%s, key=%s, value=%s",
                                   config_section, config_key, config_value)
                self.set_config_option(config_section, config_key, config_value)
            else:
                self._logger.warn("trap with no matching configuration received")

        # get configuration
        config_listen_address = self._config.get_value("SnmpTrapReceiver", "listenaddress",
                                                       "127.0.0.1")
        config_listen_port = int(self._config.get_value("SnmpTrapReceiver", "listenport", "162"))
        config_community = self._config.get_value("SnmpTrapReceiver", "community", "public")

        # create and configure SNMP engine
        snmp_engine = engine.SnmpEngine()
        config.addTransport(snmp_engine,
	                           udp.domainName + (1,),
		                          udp.UdpTransport().openServerMode((config_listen_address,
                                                               config_listen_port)))
        config.addV1System(snmp_engine, 'my-area', config_community)

        # register callback function
        ntfrcv.NotificationReceiver(snmp_engine, trap_received)

        # register timer callback function
        snmp_engine.transportDispatcher.registerTimerCbFun(check_shutdown)

        # start dispatcher
        snmp_engine.transportDispatcher.jobStarted(1)
        try:
            snmp_engine.transportDispatcher.runDispatcher()
        except:
            snmp_engine.transportDispatcher.closeDispatcher()
            raise
