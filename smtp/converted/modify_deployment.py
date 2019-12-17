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

NAME = 'smtp-deployment.yaml'

CERT_NAME = 'smtp-certs'
CERT_DIR = '/etc/postfix/certs'

SECRET_NAME = 'smtp-sasl-passwd'
SECRET_PATH = '/etc/postfix/sasl/sasl_passwd'

INIT_NAME = 'smtp-init'
INIT_PATH = '/etc/service/postfix/run.initialization'

old_path = './{}'.format(NAME)
bak_path = '{}.bak'.format(old_path)
out_path = './{}'.format('.out.'.join(NAME.split('.')))

if os.path.exists(old_path):
    os.rename(old_path, bak_path)

with open(bak_path) as f:
    data = yaml.load(f)

# Convert to new api
data['apiVersion'] = 'apps/v1'
data['spec']['selector'] = { 'matchLabels': copy.deepcopy(data['metadata']['labels']) }


# Get the volume mounts and volumes.
volumes = data['spec']['template']['spec']['volumes']
volume_mounts = data['spec']['template']['spec']['containers'][0]['volumeMounts']

def add_filemount(name, path, ktype, directory):
    if ktype == 'secret':
        volume = { 'name': name
                 , 'secret': { "secretName": name, 'defaultMode': 0o400}
                 }
        volumes.append(volume)
    elif ktype == 'configMap':
        volume = { 'name': name
                 , 'configMap': { 'name': name, 'defaultMode': 0o700 }
                 }
        volumes.append(volume)
    else:
        raise NotImplementedError(ktype)
    volume_mount = { "name": name 
                   , "mountPath": path
                   , "readOnly": True
                   }
    if not directory:
        volume_mount['subPath'] = os.path.split(path)[-1]
    volume_mounts.append(volume_mount)

# Add the certs
add_filemount(CERT_NAME, CERT_DIR, ktype='secret', directory=True)
# Add a new volume for the smtp username/password.
add_filemount(SECRET_NAME, SECRET_PATH, ktype='secret', directory=False)
# Add a new volume for the postfix configuration
add_filemount(INIT_NAME, INIT_PATH, ktype='configMap', directory=False)

# Write the modified deployment out.
with open(out_path, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False)


