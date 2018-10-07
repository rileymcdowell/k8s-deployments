#!/bin/bash

kubectl delete -Rf ./converted
kubectl delete secrets docker-registry-cert
rm -rf ./converted/*.yaml
rm -rf ./converted/*.yaml.bak

