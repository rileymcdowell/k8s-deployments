#!/bin/bash

kubectl delete -Rf ./converted
kubectl delete secrets smtp-sasl-passwd smtp-certs
kubectl delete configmaps smtp-init
rm -rf ./converted/*.yaml
rm -rf ./converted/*.yaml.bak


