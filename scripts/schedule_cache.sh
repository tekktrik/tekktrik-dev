#!/bin/sh
# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

REPOPATH=$(realpath .)

PYBINPATH="$REPOPATH/.venv/bin"

UPDATESCRIPTPATH="$REPOPATH/scripts/graphql.py"
UPDATECOMMAND="55 * * * * python $UPDATESCRIPTPATH $REPOPATH"
UPDATEJOBNAME=$(echo "$REPOPATH" | xargs basename)

DELETESCRIPTPATH="$REPOPATH/scripts/post_graphql.py"
DELETECOMMAND="5 * * * * python $DELETESCRIPTPATH $REPOPATH"
DELETEJOBNAME=$(echo "$REPOPATH" | xargs basename)

cronberry enter "Cache new cards for $UPDATEJOBNAME" "$UPDATECOMMAND" --path "$PYBINPATH" --overwrite
cronberry enter "Delete old cards for $DELETEJOBNAME" "$DELETECOMMAND" --path "$PYBINPATH" --overwrite
