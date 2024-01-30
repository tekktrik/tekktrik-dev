#!/bin/sh
# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

REPOPATH=$(realpath .)

PYTHONBIN="$REPOPATH/.venv/bin/python"

UPDATESCRIPTPATH="$REPOPATH/scripts/graphql.py"
UPDATECOMMAND="55 * * * * $PYTHONBIN $UPDATESCRIPTPATH $REPOPATH"
UPDATEJOBNAME=$(echo "$REPOPATH" | xargs basename)

DELETESCRIPTPATH="$REPOPATH/scripts/post_graphql.py"
DELETECOMMAND="5 * * * * $PYTHONBIN $DELETESCRIPTPATH $REPOPATH"
DELETEJOBNAME=$(echo "$REPOPATH" | xargs basename)

cronberry enter "Cache new cards for $UPDATEJOBNAME" "$UPDATECOMMAND" --overwrite
cronberry enter "Delete old cards for $DELETEJOBNAME" "$DELETECOMMAND" --overwrite
