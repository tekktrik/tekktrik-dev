#!/bin/sh
# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

SCRIPTPATH=$(realpath scripts/graphql.py)
JOBNAME=$(realpath . | xargs dirname)
STATICPATH=$(realpath flash_app/static)
COMMAND="python $SCRIPTPATH $STATICPATH"

cronberry enter "Images for $JOBNAME" "$COMMAND" --overwrite
