#!/usr/bin/env python

"""
Adjust the size of persistent volume claims as needed.

"""

import os
import copy
import yaml
import codecs

claim_raw = './docker-registry-persistentvolumeclaim.yaml'
claim_raw_bak = claim_raw + '.bak'
claim_out = './docker-registry-persistentvolumeclaim-out.yaml'

if os.path.exists(claim_raw):
    os.rename(claim_raw, claim_raw_bak)

with open(claim_raw_bak) as f:
    claim_data = yaml.load(f)

# First configure /etc/pihole
claim_data['spec']['resources']['requests']['storage'] = "5Gi"

with open(claim_out, 'w', encoding='utf-8') as f:
    yaml.dump(claim_data, f)


