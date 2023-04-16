#!/bin/bash

kubectl patch pv jupyter-home-pv --patch='{ "spec": { "claimRef": null } }'
