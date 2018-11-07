#!/bin/bash

kubectl delete -Rf ./converted
kubectl delete secrets unifi-web-cert
rm -rf ./converted/*.yaml
rm -rf ./converted/*.yaml.bak


