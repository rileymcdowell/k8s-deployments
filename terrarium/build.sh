#!/bin/bash

pushd terrarium
./build.sh
RET=$?
popd
exit ${RET}
