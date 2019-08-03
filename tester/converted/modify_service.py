#!/usr/bin/env python

"""
The purpose of this script is to set up the LoadBalancer's
traffic policies and IP address.

"""

import os
import copy
import yaml
import codecs

with open(os.path.expanduser('~/deployment-config.yaml')) as f:
    config = yaml.load(f)

ip_address = config['tester']['ip-address']
external_traffic_policy = config['tester']['external-traffic-policy']

if os.path.exists('./tester-service.yaml'):
    os.rename('./tester-service.yaml', './tester-service.yaml.bak')

with open('./tester-service.yaml.bak') as f:
    data = yaml.load(f)

# Write out a version with TCP services only.
data = copy.deepcopy(data)
data['metadata']['annotations']['metallb.universe.tf/allow-shared-ip'] = 'tester'
data['spec']['loadBalancerIP'] = ip_address
data['spec']['externalTrafficPolicy'] = external_traffic_policy

# Write out the modified version
with open('./tester-service.out.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)

