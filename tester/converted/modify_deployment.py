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

if os.path.exists('./tester-deployment.yaml'):
    os.rename('./tester-deployment.yaml', './tester-deployment.yaml.bak')

with open('./tester-deployment.yaml.bak') as f:
    data = yaml.load(f)

# Convert to new api format
data['apiVersion'] = 'apps/v1'

# Match pods to deployment under new api
data['spec']['selector'] = { 'matchLabels': copy.deepcopy(data['metadata']['labels']) }


# Write the modified deployment out.
with open('./tester-deployment.out.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)


