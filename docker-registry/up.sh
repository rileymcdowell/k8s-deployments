#!/bin/bash

# Create the certificate kubernetes secret to mount as files
SECRET_NAME=docker-registry-cert
kubectl get secret ${SECRET_NAME} &> /dev/null
if [ "$?" -ne "0" ] ; then
    kubectl create secret generic \
        docker-registry-cert \
        --from-file=./certs/docker.lan.crt \
        --from-file=./certs/docker.lan.key
fi

kubectl apply -Rf yaml
