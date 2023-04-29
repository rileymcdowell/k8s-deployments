#!/bin/bash

kubectl patch pv pihole-dnsmasq-pv --patch='{ "spec": { "claimRef": null } }'
kubectl patch pv pihole-config-pv --patch='{ "spec": { "claimRef": null } }'
