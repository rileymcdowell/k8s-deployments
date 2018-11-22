#!/bin/bash
set -e

wget \
    https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml \
    -O ./converted/kubernetes-dashboard.yaml

# Modify to use a load balancer and remove security restrictions
pushd converted
python3 modify_all.py
popd

kubectl create secret generic \
	--namespace=kube-system \
        kubernetes-dashboard-certs \
        --from-file=./certs/dashboard.crt  \
        --from-file=./certs/dashboard.key 


kubectl apply -Rf converted

