#!/bin/bash

FILES=$(ls converted/*.yaml | grep -v volumeclaim | tr '\n' ',' | sed s'/,$//')
BAK_FILES=$(ls converted/*.yaml.bak | grep -v volumeclaim | tr '\n' ',' | sed s'/,$//')


kubectl delete -f ${FILES}
kubectl delete secrets docker-registry-cert
rm $(echo ${FILES} | tr ',' '\n')
rm $(echo ${BAK_FILES} | tr ',' '\n')


