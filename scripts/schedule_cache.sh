#!/bin/sh
# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

REPOPATH=$(realpath .)
SCRIPTPATH="$REPOPATH/scripts/graphql.py"
COMMAND="55 23 * * * python $SCRIPTPATH $REPOPATH"
JOBNAME=$(echo "$REPOPATH" | xargs basename)

cronberry enter "Cache cards for $JOBNAME" "$COMMAND" --overwrite
