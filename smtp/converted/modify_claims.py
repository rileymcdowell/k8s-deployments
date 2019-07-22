#!/usr/bin/env python

"""
Adjust the size of the persistent volume claim as needed.

"""

import os
import copy
import yaml

NAME = 'smtp-spool-persistentvolumeclaim.yaml'

claim_raw = './{}'.format(NAME)
claim_raw_bak = claim_raw + '.bak'
claim_out = './{}'.format('.out.'.join(NAME.split('.')))

if os.path.exists(claim_raw):
    os.rename(claim_raw, claim_raw_bak)

with open(claim_raw_bak) as f:
    claim_data = yaml.load(f)

# First configure /etc/pihole
claim_data['spec']['resources']['requests']['storage'] = "250Mi"

with open(claim_out, 'w', encoding='utf-8') as f:
    yaml.dump(claim_data, f, default_flow_style=False)


