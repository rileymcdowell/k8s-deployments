#!/bin/bash

kubectl delete -Rf converted

rm ./converted/*.yaml
rm ./converted/*.yaml.bak

