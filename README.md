# alarmRetarder

alarmRetarder is a small tool, that receives alarm messages using a specified receiver (e.g. via SNMP traps), reduces identical messages and schedules them for forwarding. The forwarding of messages will be delayed using a configured value (e.g. 60 seconds). A configured forwarder (e.g. sending SMS) will be used to send alarm messges to the target.

Each alarm message containes the following fields:
* ID
* type (1 = problem, 2 = resolution)
* severity
* timestamp
* key
* logmessage

Each alarm message has a type, which could be "problem" (1) or "resolution" (2). A problem means, that there is something, which needs attention. All alarm messages of type problem with the same key will be reduced to one. A resolution alarm message resolves a problem alarm message with the same key.

If a problem alarm message occurs, it will be delayed using the configured interval. If the problem is resolved (with a resolution alarm message) within that interval, the message will not be forwarded to the user.

The tool was designed for the network management plattform OpenNMS and the SNMP trap northbounder (OpenNMS version 17.1.0 or higher), but may be useful for other use cases, too.

## Usage

### Start a Docker Container
There is a Docker Image on Docker Hub. alarmRetarder is installed in /opt/alarmRetarder with its default configuration. If you want to use your own configuration, map your own configuration file in the container with volumes.

Please hava a look at the following docker-compose.yml example:
```
version: "2"
services:
  alarmretarder:
     image: michaelbatz/alarmretarder
     volumes:
      - ./data/alarmretarder/etc/config.conf:/opt/alarmRetarder/etc/config.conf
      - ./data/alarmretarder/logs:/opt/alarmRetarder/logs
```


### Manually setup your environment
alarmRetarder is written in Python3 and all you need, are the following libraries:
* pysnmp4
* requests

If all the libraries are installed, simply execute main.py and alarmRetarder is running:
```
./main.py
```


## Documentation
The documentation is provided with the tool and can also seen on [GitHub](https://github.com/michael-batz/alarmRetarder/blob/master/docs/src/documentation.adoc)

## Support
Please use the issues on the [GitHub project](https://github.com/michael-batz/alarmRetarder "alarmRetarder on GitHub") for bugs, enhancement requests and support questions.
