#!/bin/sh

# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

set -e

cd /cache

/usr/local/bin/uv run --no-sync python manage.py sync_contributions

printf "export GRAPHQL_TOKEN='%s'\n" "$GRAPHQL_TOKEN" > /cache/.cron_env
chmod 600 /cache/.cron_env

echo "55 * * * * . /cache/.cron_env && cd /cache && /usr/local/bin/uv run --no-sync python manage.py sync_contributions >> /proc/1/fd/1 2>&1" > /etc/crontabs/root

exec crond -f
