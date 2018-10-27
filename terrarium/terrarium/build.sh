#!/bin/bash

Y=$(date '+%Y')
M=$(date '+%m')
D=$(date '+%d')

docker build --tag docker.lan/terrarium:latest --tag docker.lan/terrarium:${Y}.${M}.${D} .

if [ "$?" == "0" ] ; then
    echo "Command success. Pushing image to docker repository."
    docker push docker.lan/terrarium:latest
else
    echo "Build failed. Not pushing to docker repository."
fi
