#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

/wait-for-it.sh db:5432 -t 5

alembic upgrade head

exec "$@"