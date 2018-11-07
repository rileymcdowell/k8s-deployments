#!/usr/bin/env python

"""
The purpose of this script is to separate udp and tcp services apart
because while metallb supports this, kubernetes does not allow 
one load balancer to balance both udp and tcp traffic.

https://github.com/kubernetes/kubernetes/pull/64471

"""

import os
import copy
import yaml
import codecs

with open('../../deployment-config.yaml') as f:
    config = yaml.load(f)

ip_address = config['unifi']['ip-address']
external_traffic_policy = config['unifi']['external-traffic-policy']

if os.path.exists('./unifi-web-service.yaml'):
    os.rename('./unifi-web-service.yaml', './unifi-web-service.yaml.bak')

with open('./unifi-web-service.yaml.bak') as f:
    data = yaml.load(f)

# Write out a version with TCP services only.
tcp_data = copy.deepcopy(data)
keep_ports = []
for port in tcp_data['spec']['ports']:
    if 'protocol' in port and port['protocol'] == 'UDP':
        continue
    else:
        keep_ports.append(port)
tcp_data['spec']['ports'] = keep_ports
tcp_data['metadata']['name'] += '-tcp'
tcp_data['metadata']['annotations']['metallb.universe.tf/allow-shared-ip'] = 'unifi'
tcp_data['spec']['loadBalancerIP'] = ip_address
tcp_data['spec']['externalTrafficPolicy'] = external_traffic_policy
with open('./unifi-web-service-tcp.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(tcp_data, f)

# Write out a version with UDP services only.
udp_data = copy.deepcopy(data)
keep_ports = []
for port in udp_data['spec']['ports']:
    if 'protocol' in port and port['protocol'] == 'UDP':
        keep_ports.append(port)
    else:
        continue
udp_data['spec']['ports'] = keep_ports
udp_data['metadata']['name'] += '-udp'
udp_data['metadata']['annotations']['metallb.universe.tf/allow-shared-ip'] = 'unifi'
udp_data['spec']['loadBalancerIP'] = ip_address
udp_data['spec']['externalTrafficPolicy'] = external_traffic_policy
with open('./unifi-web-service-udp.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(udp_data, f)



