#!/usr/bin/env python

"""
This script sets the IP addresses of the deployed service.
"""

import os
import copy
import yaml

NAME = 'plex'

with open(os.path.expanduser('~/deployment-config.yaml')) as f:
    config = yaml.load(f)
    
ip_address = config[NAME]['ip-address']
external_traffic_policy = config[NAME]['external-traffic-policy']

if os.path.exists('./{}-service.yaml'.format(NAME)):
    os.rename('./{}-service.yaml'.format(NAME), './{}-service.yaml.bak'.format(NAME))

with open('./{}-service.yaml.bak'.format(NAME)) as f:
    raw_data = yaml.load(f)

# Write out a version with TCP services only.
tcp_ports = []
udp_ports = []
for port in raw_data['spec']['ports']:
    if 'protocol' in port and port['protocol'] == 'UDP':
        udp_ports.append(port) 
    else:
        tcp_ports.append(port)

data = copy.deepcopy(raw_data)

data['spec']['ports'] = tcp_ports
data['metadata']['name'] += '-tcp'
data['metadata']['annotations']['metallb.universe.tf/allow-shared-ip'] = NAME
data['spec']['loadBalancerIP'] = ip_address
data['spec']['externalTrafficPolicy'] = external_traffic_policy 
with open('./{}-service-tcp.out.yaml'.format(NAME), 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)

# Write out a version with UDP services only.
data = copy.deepcopy(raw_data)
keep_ports = []
data['spec']['ports'] = udp_ports
data['metadata']['name'] += '-upd'
data['metadata']['annotations']['metallb.universe.tf/allow-shared-ip'] = NAME
data['spec']['loadBalancerIP'] = ip_address
data['spec']['externalTrafficPolicy'] = external_traffic_policy 
with open('./{}-service-udp.out.yaml'.format(NAME), 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)


