#!/bin/bash
set -e

FILES=$(ls converted/*.yaml | grep volumeclaim | tr '\n' ',' | sed s'/,$//')
BAK_FILES=$(ls converted/*.yaml.bak | grep volumeclaim | tr '\n' ',' | sed s'/,$//')

kubectl delete -f ${FILES}

rm $(echo ${FILES} | tr ',' '\n')
rm $(echo ${BAK_FILES} | tr ',' '\n')

