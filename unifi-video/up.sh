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

kubectl apply -Rf converted
