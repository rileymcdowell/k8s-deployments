#!/bin/bash

kubectl patch pv plex-media-pv --patch='{ "spec": { "claimRef": null } }'
kubectl patch pv plex-config-pv --patch='{ "spec": { "claimRef": null } }'
