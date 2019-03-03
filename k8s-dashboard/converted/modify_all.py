#!/usr/bin/env python3

"""
The purpose of this script is to assigns a traffic policy and ip address
using the metallb load balancer configuration.

"""

import os
import copy
import yaml
import codecs

config_key = 'k8s-dashboard'

with open('../../deployment-config.yaml') as f:
    config = yaml.load(f)

ip_address = config[config_key]['ip-address']
external_traffic_policy = config[config_key]['external-traffic-policy']

if os.path.exists('./kubernetes-dashboard.yaml'):
    os.rename('./kubernetes-dashboard.yaml', './kubernetes-dashboard.yaml.bak')

with open('./kubernetes-dashboard.yaml.bak') as f:
    raw_data = list(yaml.load_all(f))


def add_load_balancer():
    # Modify the service to specify a load balancer.
    dashboard_service = [x for x in raw_data if x['kind'] == 'Service'][0]
    dashboard_service['metadata']['annotations'] = {}
    dashboard_service['metadata']['annotations']['metallb.universe.tf/allow-shared-ip'] = config_key
    dashboard_service['spec']['type'] = 'LoadBalancer'
    dashboard_service['spec']['loadBalancerIP'] = ip_address
    dashboard_service['spec']['externalTrafficPolicy'] = external_traffic_policy

def remove_cert_secret():
    secret_idx = None
    for idx, elem in enumerate(raw_data):
        if elem['kind'] == 'Secret':
            secret_idx = idx 
            break

    raw_data.pop(secret_idx)

def modify_role():
    role_idx = None
    for idx, elem in enumerate(raw_data):
        if elem['kind'] == 'Role':
            role_idx = idx 
            break

    role = raw_data[role_idx]
    role['kind'] = 'ClusterRole'
    role['metadata']['name'] = 'kubernetes-dashboard-readonly'
    rules = []
    rules.append({ 'apiGroups': ['']
                 , 'resources': ['configmaps', 'secrets']
                 , 'verbs': ['create']
                 })
    rules.append({ 'apiGroups': ['']
                 , 'resources': ['secrets']
                 , 'resourceNames': ['kubernetes-dashboard-key-holder']
                 , 'verbs': ['update', 'delete']
                 })
    rules.append({ 'apiGroups': ['*']
                 , 'resources': [ '*' ]
                 , 'verbs': ['get', 'list', 'watch']
                 })
    role['rules'] = rules

def update_role_binding():
    role_binding = [x for x in raw_data if x['kind'] == 'RoleBinding'][0]
    role_binding['kind'] = 'ClusterRoleBinding'
    role_binding['metadata']['name'] = 'kubernetes-dashboard-readonly'
    role_binding['roleRef']['name'] = 'kubernetes-dashboard-readonly'
    role_binding['roleRef']['kind'] = 'ClusterRole'

def modify_deployment():
    deployment = [x for x in raw_data if x['kind'] == 'Deployment'][0]
    deployment['spec']['template']['spec']['containers'][0]['args'].append('--enable-skip-login')

update_role_binding()
modify_role()
remove_cert_secret()
add_load_balancer()
modify_deployment()

# Write it out with the hange.
with open('./kubernetes-dashboard.out.yaml', 'w', encoding='utf-8') as f:
    yaml.dump_all(raw_data, f, default_flow_style=False)

