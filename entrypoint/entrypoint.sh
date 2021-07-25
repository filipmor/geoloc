#!/bin/bash

set -o errexit
set -o nounset

case $1 in
    bootstrap)
        exec /entrypoint/bootstrap.sh
        ;;
    start-backend)
        exec /entrypoint/start-backend.sh "${@:2}"
        ;;
    *)
        exec "$@"
        ;;
esac
