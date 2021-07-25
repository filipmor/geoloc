#!/bin/sh

set -o errexit
set -o nounset

. /entrypoint/wait-postgres.sh

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
