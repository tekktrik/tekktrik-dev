#!/bin/sh
# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

# Script for immediately downloading GitHub repository summary
# card images, useful when errors occur and need to be fixed
# on the server

SCRIPTSPATH="/cron"
UPDATESCRIPTPATH="$SCRIPTSPATH/scripts/graphql.py"

python "$UPDATESCRIPTPATH" "$SCRIPTSPATH" --now
