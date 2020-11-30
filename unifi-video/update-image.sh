#!/bin/bash

if [ ! -d ./converted ] ; then
    mkdir -p ./converted
fi

kompose convert --out converted

pushd converted
python3 modify_service.py
python3 modify_claims.py
python3 modify_deployment.py
popd

# Apply triggers an image update (update definition, scale to zero, scale to one).
kubectl apply -Rf converted/unifi-video-deployment.out.yaml
