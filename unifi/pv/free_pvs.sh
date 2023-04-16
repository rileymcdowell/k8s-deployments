#!/bin/bash

kubectl patch pv unifi-mongo-config-pv --patch='{ "spec": { "claimRef": null } }'
kubectl patch pv unifi-mongo-stat-pv --patch='{ "spec": { "claimRef": null } }'
kubectl patch pv unifi-web-config-pv --patch='{ "spec": { "claimRef": null } }'
