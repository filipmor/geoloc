#!/bin/sh

set -o errexit
set -o nounset

. /entrypoint/wait-postgres.sh

python manage.py migrate
