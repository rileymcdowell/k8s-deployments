#!/usr/bin/env python3
import socket
import struct

#CAST_GRP = '192.168.1.255'
CAST_GRP = '255.255.255.255'
CAST_PORT = 10001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.bind(('', CAST_PORT))
#mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
#sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  data, addr = sock.recvfrom(1024)
  print('FROM ADDRESS: {}'.format(addr))
  print('------ BEGIN DATA ------')
  print(data)
  print('------- END DATA -------')
  print('')
