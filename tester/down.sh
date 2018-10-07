#!/bin/bash

kubectl delete -Rf ./converted
rm -rf ./converted/*.yaml
rm -rf ./converted/*.yaml.bak
