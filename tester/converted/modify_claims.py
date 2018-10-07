#!/usr/bin/env python

"""
Adjust the size of persistent volume claims as needed.

"""

import os
import copy
import yaml
import codecs

raw = './test-volume-persistentvolumeclaim.yaml'
raw_bak = raw + '.bak'
out = './test-volume-persistentvolumeclaim-out.yaml'

if os.path.exists(raw):
    os.rename(raw, raw_bak)

with open(raw_bak) as f:
    data = yaml.load(f)

data['spec']['resources']['requests']['storage'] = "25Mi"

with open(out, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)


