#!/usr/bin/env python

"""
Adjust the size of persistent volume claims as needed.

"""

import os
import copy
import yaml
import codecs

redis_raw = './terrarium-redis-persistentvolumeclaim.yaml'
redis_raw_bak = redis_raw + '.bak'
redis_out = './terrarium-redis-persistentvolumeclaim-out.yaml'

if os.path.exists(redis_raw):
    os.rename(redis_raw, redis_raw_bak)

with open(redis_raw_bak) as f:
    redis_data = yaml.load(f)

# Configure total storage required.
redis_data['spec']['resources']['requests']['storage'] = "25Mi"

with open(redis_out, 'w', encoding='utf-8') as f:
    yaml.dump(redis_data, f, default_flow_style=False)




