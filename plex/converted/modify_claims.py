#!/usr/bin/env python

"""
Adjust the size of persistent volume claims as needed.

"""

import os
import copy
import yaml
import codecs

config_claim = "plex-config-persistentvolumeclaim"
transcode_claim = "plex-transcode-persistentvolumeclaim"
media_claim = "plex-media-persistentvolumeclaim"

for claim, size in [(config_claim, '2Gi'), (transcode_claim, '2Gi'), (media_claim, "2Ti")]:

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


