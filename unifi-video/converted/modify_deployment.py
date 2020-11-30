#!/usr/bin/env python

"""
Need to add special Linux capabilities to the container.
"""

import os
import copy
import yaml
import codecs

if os.path.exists('./unifi-video-deployment.yaml'):
    os.rename('./unifi-video-deployment.yaml', './unifi-video-deployment.yaml.bak')

with open('./unifi-video-deployment.yaml.bak') as f:
    data = yaml.safe_load(f)

# Update to release k8s api
data['apiVersion'] = 'apps/v1'
data['spec']['selector'] = { 'matchLabels': copy.deepcopy(data['metadata']['labels']) }

# Add the CAP_SYS_ADMIN and CAP_DAC_READ_SEARCH capabilities 
# to match the docker run command documented for the image.
container = data['spec']['template']['spec']['containers'][0]
container['securityContext'] = {}
container['securityContext']['capabilities'] = {}
container['securityContext']['capabilities']['add'] = ['CAP_SYS_ADMIN', 'CAP_DAC_READ_SEARCH']

# Add the apparmor profile called "unconfined"
metadata = data['spec']['template']['metadata']
metadata['annotations'] = {}
metadata['annotations']['container.apparmor.security.beta.kubernetes.io/unifi-video'] = 'unconfined'


# Write the modified deployment out.
with open('./unifi-video-deployment.out.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)


