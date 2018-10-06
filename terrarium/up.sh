#!/bin/bash
set -e

./build.sh

if [ ! -d ./converted ] ; then
    mkdir -p ./converted
fi

kompose convert --out converted

pushd converted
# Call modification scripts here.
python3 modify_claims.py
python3 modify_service.py
popd

kubectl apply -Rf converted
