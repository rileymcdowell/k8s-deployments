#!/usr/bin/env python

"""
The purpose of this script is to configure separate udp and tcp services 
because while metallb supports this, kubernetes does not allow 
one load balancer to balance both udp and tcp traffic.

This service also sets the IP addresses of various deployed services.

https://github.com/kubernetes/kubernetes/pull/64471

"""

import os
import copy
import yaml
import codecs

with open('../../deployment-config.yaml') as f:
    config = yaml.load(f)
    
ip_address = config['docker-registry']['ip-address']
external_traffic_policy = config['docker-registry']['external-traffic-policy']

if os.path.exists('./docker-registry-service.yaml'):
    os.rename('./docker-registry-service.yaml', './docker-registry-service.yaml.bak')

with open('./docker-registry-service.yaml.bak') as f:
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
tcp_data['metadata']['annotations']['metallb.universe.tf/allow-shared-ip'] = 'docker-registry'
tcp_data['spec']['loadBalancerIP'] = ip_address
tcp_data['spec']['externalTrafficPolicy'] = external_traffic_policy 
with open('./docker-registry-service-tcp.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(tcp_data, f)


