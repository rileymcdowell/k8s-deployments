#!/bin/bash

if [ ! -d ./converted ] ; then
    mkdir -p ./converted
fi

kompose convert --out converted

pushd converted
# Modifications here, if needed.
python3 modify_claims.py
python3 modify_service.py
python3 modify_deployment.py
popd

kubectl apply -Rf converted/docker-registry-deployment.out.yaml
