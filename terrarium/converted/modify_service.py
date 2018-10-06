#!/usr/bin/env python

"""
The purpose of this script is to separate udp and tcp services apart
because while metallb supports this, kubernetes does not allow 
one load balancer to balance both udp and tcp traffic.

It also assigns a traffic policy and ip address.

https://github.com/kubernetes/kubernetes/pull/64471

"""

import os
import copy
import yaml
import codecs

with open('../../deployment-config.yaml') as f:
    config = yaml.load(f)

ip_address = config['terrarium']['ip-address']
external_traffic_policy = config['terrarium']['external-traffic-policy']

if os.path.exists('./terrarium-app-service.yaml'):
    os.rename('./terrarium-app-service.yaml', './terrarium-app-service.yaml.bak')

with open('./terrarium-app-service.yaml.bak') as f:
    raw_data = yaml.load(f)

# Write out a version with TCP services only.
data = copy.deepcopy(raw_data)
keep_ports = []
for port in data['spec']['ports']:
    if 'protocol' in port and port['protocol'] == 'UDP':
        continue
    else:
        keep_ports.append(port)
data['spec']['ports'] = keep_ports
data['metadata']['name'] += '-tcp'
data['metadata']['annotations']['metallb.universe.tf/allow-shared-ip'] = 'terrarium'
data['spec']['loadBalancerIP'] = ip_address
data['spec']['externalTrafficPolicy'] = external_traffic_policy
with open('./terrarium-app-service-tcp.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)


