FROM ubuntu:latest
MAINTAINER Michael Batz <mail@michael-batz.de>

# copy repository to /opt
COPY ./ /opt/alarmRetarder/

# install required software
RUN apt-get update -y \
    && apt-get install -y python3 python3-pysnmp4 python3-requests

# start alarmRetarder
CMD /opt/alarmRetarder/main.py
