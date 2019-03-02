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

kubectl create secret generic \
       unifi-web-cert \
       --from-file=./certs/cert.pem  \
       --from-file=./certs/chain.pem  \
       --from-file=./certs/privkey.pem  \
       --from-file=./certs/unifi.pem.csr

kubectl apply -Rf converted
