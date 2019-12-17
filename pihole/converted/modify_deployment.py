#!/usr/bin/env python

"""
Adjust the size of persistent volume claims as needed.

"""

import os
import copy
import yaml
import codecs

deployment_raw = './pihole-deployment.yaml'
deployment_raw_bak = deployment_raw + '.bak'
deployment_out = './pihole-deployment.out.yaml'

if os.path.exists(deployment_raw):
    os.rename(deployment_raw, deployment_raw_bak)

with open(deployment_raw_bak) as f:
    data = yaml.load(f)

data['apiVersion'] = 'apps/v1'

data['spec']['selector'] = { 'matchLabels': copy.deepcopy(data['metadata']['labels']) }

# Set mount for log file to single-file log using subPath.
for mount in data['spec']['template']['spec']['containers'][0]['volumeMounts']:
    if mount['mountPath'] == '/var/log/pihole.log':
        mount['subPath'] = 'pihole.log'

with open(deployment_out, 'w', encoding='utf-8') as f:
    yaml.dump(data, f)




