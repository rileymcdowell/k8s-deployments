#!/usr/bin/env python3
import gevent
from gevent import socket
from gevent.server import DatagramServer

MCAST_IP = "239.255.255.250"
MCAST_PORT = 1900
MCAST_TTL = 2

import socket as _socket

def get_ip_address():
    s = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
    try:
        s.connect(('1.2.3.4', 9))
        return s.getsockname()[0]
    except _socket.error:
        return None
    finally:
        del s

CLIENTS = {}

def _response_received(message, address):
        print("Received a response from {0}:{1}".format(*address))
        lines = [x.decode() for x in message.splitlines()]
        lines.pop(0) # HTTP status
        headers = {}
        for line in lines:
            try:
                header, value = line.split(":", 1)
                headers[header.lower()] = value.strip()
            except ValueError:
                continue
        if (headers.get('x-user-agent', None) == 'redsonic'):
            location=headers.get('location',None)
            if location is not None and location not in CLIENTS:
                print("Found WeMo at {0}".format(location))
                CLIENTS[location] = headers
                #gevent.spawn(discovered.send, self, address=address,
                #        headers=headers)

server = DatagramServer(get_ip_address() + ':54321', _response_received)

request = '\r\n'.join(("M-SEARCH * HTTP/1.1",
                       "HOST:{}:{}",
                       "ST:upnp:rootdevice",
                       "MX:2",
                       'MAN:"ssdp:discover"',
                        "", "")).format(MCAST_IP, MCAST_PORT)

with gevent.Timeout(2, KeyboardInterrupt):
    while True:
        try:
            server.set_spawn(1)
            server.init_socket()
            server.socket.setsockopt(_socket.IPPROTO_IP, _socket.IP_MULTICAST_TTL, MCAST_TTL)
            server.start()
            server.sendto(request.encode(), (MCAST_IP, MCAST_PORT))
            gevent.sleep(2)
        except KeyboardInterrupt:
            print('Scan Complete')
            break


