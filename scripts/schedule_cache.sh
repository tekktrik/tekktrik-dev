#!/bin/sh
# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

# Script for managing the cron job instructions for downloading
# GitHub repository summary card images via cronberry

SCRIPTSPATH="/cron"
PYTHONBIN="/usr/local/bin/python"

UPDATESCRIPTPATH="$SCRIPTSPATH/scripts/graphql.py"
UPDATECOMMAND="55 * * * * $PYTHONBIN $UPDATESCRIPTPATH $SCRIPTSPATH"

DELETESCRIPTPATH="$SCRIPTSPATH/scripts/post_graphql.py"
DELETECOMMAND="5 * * * * $PYTHONBIN $DELETESCRIPTPATH $SCRIPTSPATH"

cronberry enter "Cache new cards" "$UPDATECOMMAND" --overwrite
cronberry enter "Delete old cards" "$DELETECOMMAND" --overwrite
