#!/usr/bin/env python

"""
Adjust the size of persistent volume claims as needed.

"""

import os
import copy
import yaml
import codecs

mongo_claim = "unifi-mongo-config-persistentvolumeclaim"
mongo_stat_claim = "unifi-mongo-stat-persistentvolumeclaim"
unifi_web_config_claim = "unifi-web-config-persistentvolumeclaim"
for claim, size in [(mongo_claim, '4Gi'), (mongo_stat_claim, '4Gi'), (unifi_web_config_claim, '100Mi')]:

    raw = './' + claim + '.yaml'
    raw_bak = raw + '.bak'
    out = './' + claim + '-out.yaml'

    if os.path.exists(raw):
        os.rename(raw, raw_bak)

    with open(raw_bak) as f:
        data = yaml.load(f)

    data['spec']['resources']['requests']['storage'] = size

    with open(out, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False)


