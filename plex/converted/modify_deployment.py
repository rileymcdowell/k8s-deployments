#!/usr/bin/env python

import os
import copy
import yaml
import codecs

if os.path.exists('./plex-deployment.yaml'):
    os.rename('./plex-deployment.yaml', './plex-deployment.yaml.bak')

with open('./plex-deployment.yaml.bak') as f:
    data = yaml.load(f)

data['apiVersion'] = 'apps/v1'

data['spec']['selector'] = { 'matchLabels': copy.deepcopy(data['metadata']['labels']) }

# Write the modified deployment out.
with open('./plex-deployment.out.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)


