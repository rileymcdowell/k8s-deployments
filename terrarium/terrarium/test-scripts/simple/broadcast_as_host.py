#!/usr/bin/env python3

import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('1.2.3.4', 9))
        return s.getsockname()[0]
    except socket.error:
        return None
    finally:
        del s

MULTICAST = True 

if MULTICAST:
    CAST_GRP = '239.255.255.250'
    CAST_PORT = 1900
else:
    # Broadcast, not multicast
    CAST_GRP = '192.168.1.255'
    CAST_PORT = 1900

# regarding socket.IP_MULTICAST_TTL
# ---------------------------------
# for all packets sent, after two hops on the network the packet will not
# be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
MULTICAST_TTL = 8

REQUEST = '\r\n'.join([ "M-SEARCH * HTTP/1.1"
                      , "HOST: {host}:{port}"
                      , "ST:upnp:rootdevice"
                      , "MX:8"
                      , 'MAN:"ssdp:discover"'
                      , ""
                      , ""
                      ]).format(host=CAST_GRP, port=CAST_PORT)

print(REQUEST)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
if MULTICAST:
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
else:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(REQUEST.encode(), (CAST_GRP, CAST_PORT))


print("Beginning listener")
print("---------------------")
while True:
    data, addr = sock.recvfrom(65507)
    print("rx addr:", addr)
    print("rx data:", data)
    print("---------------------")

