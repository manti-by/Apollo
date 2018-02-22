#!/bin/bash
header () {
    echo -e "\e[96m\e[1m$1\e[0m"
}

LOCAL_PATH=$(dirname $(dirname $(pwd)))
REMOTE_REMOTE = '/home/pi/apollo'

header "Deploying source code to the server"
scp -rv $LOCAL_PATH/server/\{*.py,*.js, *.html, *.css\} pi:raspberry@rpi:$REMOTE_REMOTE/server