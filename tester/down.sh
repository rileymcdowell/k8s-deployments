#!/bin/bash

kubectl delete -f ./yaml

kubectl patch pv tester-temp-pv --patch='{ "spec": { "claimRef": null } }'
