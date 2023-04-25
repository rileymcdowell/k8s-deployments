#!/bin/bash

kubectl patch pv docker-registry-pv --patch='{ "spec": { "claimRef": null } }'
