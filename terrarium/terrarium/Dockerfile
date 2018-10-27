FROM alpine:3.8

RUN apk add --no-cache \
    python3 \
    py3-flask \
    py3-redis \
    py3-gevent

RUN  python3 -m pip install \
     flask \
     apscheduler \
     redis \
     ouimeaux \
     six \
     gevent~=1.2.0 # ouimeaux needs this

# Patch ouimeaux to have a packet TTL of 2
RUN sed -i 's/import gevent/import gevent\nimport socket as _socket/' /usr/lib/python3.6/site-packages/ouimeaux/environment.py && \
    sed -i 's/self.upnp.server.start()/self.upnp.server.start();self.upnp.server.socket.setsockopt(_socket.IPPROTO_IP, _socket.IP_MULTICAST_TTL, 2)/' /usr/lib/python3.6/site-packages/ouimeaux/environment.py

# Make sure times are reported in local time
RUN apk add --no-cache tzdata && \
    echo "America/Chicago" > /etc/timezone && \
    echo "America/Chicago" > /etc/TZ && \
    cp /usr/share/zoneinfo/America/Chicago /etc/localtime


RUN mkdir /app

WORKDIR  /app

COPY ./ ./

ENV FLASK_APP "app.py"
ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

STOPSIGNAL SIGINT

EXPOSE 80
EXPOSE 54321

CMD flask run --host=0.0.0.0 --port=80
