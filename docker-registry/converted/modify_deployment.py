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

#####################
# First handle the UI
#####################
if os.path.exists('./docker-registry-ui-deployment.yaml'):
    os.rename('./docker-registry-ui-deployment.yaml', './docker-registry-ui-deployment.yaml.bak')

with open('./docker-registry-ui-deployment.yaml.bak') as f:
    data = yaml.load(f)

# Convert to new api style
data['apiVersion'] = 'apps/v1'

# Tell how to match pods to deployment
data['spec']['selector'] = { 'matchLabels': copy.deepcopy(data['metadata']['labels']) }

# Write the modified deployment out.
with open('./docker-registry-ui-deployment.out.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f)

#####################
# Now for the backend.
#####################
if os.path.exists('./docker-registry-deployment.yaml'):
    os.rename('./docker-registry-deployment.yaml', './docker-registry-deployment.yaml.bak')

with open('./docker-registry-deployment.yaml.bak') as f:
    data = yaml.load(f)

# Convert to new api style
data['apiVersion'] = 'apps/v1'

# Tell how to match pods to deployment
data['spec']['selector'] = { 'matchLabels': copy.deepcopy(data['metadata']['labels']) }

# Get the volume mounts and volumes.
volume_mounts = data['spec']['template']['spec']['containers'][0]['volumeMounts']
volumes = data['spec']['template']['spec']['volumes']

# Add a new volume for the secrets.
secret_volume = { 'name': 'docker-registry-cert'
                , 'secret': { "secretName": "docker-registry-cert" }
                }
volumes.append(secret_volume)

# Add a new volume mount to the container.
secret_volume_mount = { "name": "docker-registry-cert"
                      , "mountPath": "/certs"
                      , "readOnly": True
                      }
volume_mounts.append(secret_volume_mount)

# Write the modified deployment out.
with open('./docker-registry-deployment.out.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f)


