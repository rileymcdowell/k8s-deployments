#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

docker run -it \
           --volume "${DIR}/app.py:/app/app.py" \
           -p "80:80/tcp" \
           docker.lan/terrarium \
           "$@"
