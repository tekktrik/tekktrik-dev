#!/bin/sh
# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

REPOPATH=$(realpath .)
JOBNAME=$(echo "$REPOPATH" | xargs basename)
STATICPATH="$REPOPATH/flash_app/static"
COMMAND="50 23 * * * python $SCRIPTPATH $REPOPATH"

cronberry enter "Cache cards for $JOBNAME" "$COMMAND" --overwrite
