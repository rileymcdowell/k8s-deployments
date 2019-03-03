#!/usr/bin/env python

"""
This script sets the IP addresses of the deployed service.
"""

import os
import yaml

NAME = 'smtp'

with open('../../deployment-config.yaml') as f:
    config = yaml.load(f)
    
ip_address = config[NAME]['ip-address']
external_traffic_policy = config[NAME]['external-traffic-policy']

if os.path.exists('./{}-service.yaml'.format(NAME)):
    os.rename('./{}-service.yaml'.format(NAME), './{}-service.yaml.bak'.format(NAME))

with open('./{}-service.yaml.bak'.format(NAME)) as f:
    data = yaml.load(f)

data['metadata']['name'] += '-tcp'
data['metadata']['annotations']['metallb.universe.tf/allow-shared-ip'] = NAME
data['spec']['loadBalancerIP'] = ip_address
data['spec']['externalTrafficPolicy'] = external_traffic_policy 
with open('./{}-service.out.yaml'.format(NAME), 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)


