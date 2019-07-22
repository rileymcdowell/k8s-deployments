#!/usr/bin/env python

"""
Adjust the size of persistent volume claims as needed.

"""

import os
import copy
import yaml
import codecs

etc_raw = './etc-pihole-persistentvolumeclaim.yaml'
etc_raw_bak = etc_raw + '.bak'
etc_out = './etc-pihole-persistentvolumeclaim-out.yaml'

if os.path.exists(etc_raw):
    os.rename(etc_raw, etc_raw_bak)

with open(etc_raw_bak) as f:
    etc_data = yaml.load(f)

# First configure /etc/pihole
etc_data['spec']['resources']['requests']['storage'] = "2Gi"

with open(etc_out, 'w', encoding='utf-8') as f:
    yaml.dump(etc_data, f)




