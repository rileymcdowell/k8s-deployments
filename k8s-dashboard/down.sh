#!/bin/bash

kubectl delete -Rf ./converted

kubectl delete secrets \
	--namespace=kube-system \
	kubernetes-dashboard-certs

rm ./converted/*.yaml
rm ./converted/*.yaml.bak
