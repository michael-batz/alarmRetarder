#!/bin/bash
/usr/bin/snmptrap -v1  -c public 127.0.0.1 \
    .1.3.6.1.4.1.99999.3 \
    127.0.0.1 6 2 55 \
    .1.3.6.1.4.1.99999.3.10 s "SmsEagleForwarder" \
    .1.3.6.1.4.1.99999.3.11 s "target" \
    .1.3.6.1.4.1.99999.3.12 s "+49987654321" \
