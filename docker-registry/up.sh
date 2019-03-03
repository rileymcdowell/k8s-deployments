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

# Create the certificate kubernetes "generic" secret to mount as files
kubectl create secret generic \
    docker-registry-cert \
    --from-file=./certs/docker.lan.crt \
    --from-file=./certs/docker.lan.key

kubectl apply -Rf converted
