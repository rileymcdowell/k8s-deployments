#!/bin/bash

FILES=$(ls converted/*.yaml | grep -v volumeclaim | tr '\n' ',' | sed s'/,$//')
BAK_FILES=$(ls converted/*.yaml.bak | grep -v volumeclaim | tr '\n' ',' | sed s'/,$//')

kubectl delete -f ${FILES}
kubectl delete secrets smtp-sasl-passwd smtp-certs
kubectl delete configmaps smtp-init

rm $(echo ${FILES} | tr ',' '\n')
rm $(echo ${BAK_FILES} | tr ',' '\n')
