#!/usr/bin/env python3
import socket
import struct

MCAST_GRP = '239.255.255.250'
MCAST_PORT = 1900

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  data, addr = sock.recvfrom(10240)
  print('FROM ADDRESS: {}'.format(addr))
  print('------ BEGIN DATA ------')
  print(data)
  print('------- END DATA -------')
  print('')
