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
       smtp-certs \
       --from-file=./cert/smtp.lan.pem \
       --from-file=./cert/smtp.lan.key

kubectl create secret generic \
       smtp-sasl-passwd \
       --from-file=./secret/sasl_passwd

kubectl create configmap \
       smtp-init \
       --from-file=./config/run.initialization

kubectl apply -Rf converted
