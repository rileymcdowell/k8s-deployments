#!/usr/bin/env python

"""
Adjust the size of persistent volume claims as needed.

"""

import os
import copy
import yaml
import codecs

video_claim = "unifi-video-persistentvolumeclaim"
video_vids_claim = "unifi-video-vids-persistentvolumeclaim"

for claim, size in [(video_claim, '1Gi'), (video_vids_claim, '8Gi')]:

    raw = './' + claim + '.yaml'
    raw_bak = raw + '.bak'
    out = './' + claim + '-out.yaml'

    if os.path.exists(raw):
        os.rename(raw, raw_bak)

    with open(raw_bak) as f:
        data = yaml.safe_load(f)

    data['spec']['resources']['requests']['storage'] = size

    with open(out, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False)


