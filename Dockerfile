FROM ubuntu:latest
MAINTAINER Michael Batz <mail@michael-batz.de>

# copy repository to /opt
COPY * /opt/alarmRetarder/

# install required software
RUN apt-get update -y \
    && apt-get install -y python3 python3-pysnmp4

# start alarmRetarder
RUN /opt/alarmRetarder/main.py
