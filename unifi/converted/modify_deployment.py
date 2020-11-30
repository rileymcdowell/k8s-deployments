#!/usr/bin/env python

"""
The purpose of this script is to modify 
the deployment to mount kubernetes secrets into
a certs directory to enable https.
"""

import os
import copy
import yaml
import codecs

if os.path.exists('./unifi-web-deployment.yaml'):
    os.rename('./unifi-web-deployment.yaml', './unifi-web-deployment.yaml.bak')

with open('./unifi-web-deployment.yaml.bak') as f:
    data = yaml.safe_load(f)

# Switch to apps/v1 api from previous beta api
data['apiVersion'] = 'apps/v1'
data['spec']['selector'] = { 'matchLabels': copy.deepcopy(data['metadata']['labels']) }

# Get the volume mounts and volumes.
if not 'volumeMounts' in data['spec']['template']['spec']['containers'][0]:
    data['spec']['template']['spec']['containers'][0]['volumeMounts'] = []
volume_mounts = data['spec']['template']['spec']['containers'][0]['volumeMounts']
if not 'volumes' in data['spec']['template']['spec']:
    data['spec']['template']['spec']['volumes'] = []
volumes = data['spec']['template']['spec']['volumes']

# Add a new volume for the secrets.
secret_volume = { 'name': 'unifi-web-cert'
                , 'secret': { "secretName": "unifi-web-cert" }
                }
volumes.append(secret_volume)

# Add a new volume mount to the container.
secret_volume_mount = { "name": "unifi-web-cert"
                      , "mountPath": "/unifi/cert"
                      , "readOnly": True
                      }
volume_mounts.append(secret_volume_mount)

# Write the modified deployment out.
with open('./unifi-web-deployment.out.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)


with open('./unifi-mongo-stat-deployment.yaml') as f:
    data = yaml.safe_load(f)

data['apiVersion'] = 'apps/v1'
data['spec']['selector'] = { 'matchLabels': copy.deepcopy(data['metadata']['labels']) }

with open('./unifi-mongo-stat-deployment.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)

with open('./unifi-mongo-config-deployment.yaml') as f:
    data = yaml.safe_load(f)

data['apiVersion'] = 'apps/v1'
data['spec']['selector'] = { 'matchLabels': copy.deepcopy(data['metadata']['labels']) }

with open('./unifi-mongo-config-deployment.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)
