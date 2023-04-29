#!/bin/bash

kubectl patch pv unifi-video-config-pv --patch='{ "spec": { "claimRef": null } }'
kubectl patch pv unifi-video-vids-pv --patch='{ "spec": { "claimRef": null } }'
