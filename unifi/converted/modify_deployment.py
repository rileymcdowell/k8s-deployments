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
    data = yaml.load(f)

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


