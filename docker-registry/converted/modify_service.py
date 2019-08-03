#!/usr/bin/env python

"""
This script sets the IP addresses of various deployed services.

"""

import os
import copy
import yaml
import codecs

with open(os.path.expanduser('~/deployment-config.yaml')) as f:
    config = yaml.load(f)
    
for service_name in ('docker-registry', 'docker-registry-ui'):
    ip_address = config[service_name]['ip-address']
    external_traffic_policy = config[service_name]['external-traffic-policy']

    if os.path.exists('./{}-service.yaml'.format(service_name)):
        os.rename('./{}-service.yaml'.format(service_name), './{}-service.yaml.bak'.format(service_name))

    with open('./{}-service.yaml.bak'.format(service_name)) as f:
        data = yaml.load(f)

    # Write out a version with TCP services only.
    tcp_data = copy.deepcopy(data)
    tcp_data['metadata']['annotations']['metallb.universe.tf/allow-shared-ip'] = service_name
    tcp_data['spec']['loadBalancerIP'] = ip_address
    tcp_data['spec']['externalTrafficPolicy'] = external_traffic_policy
    with open('./{}-service.yaml'.format(service_name), 'w', encoding='utf-8') as f:
        yaml.dump(tcp_data, f)


