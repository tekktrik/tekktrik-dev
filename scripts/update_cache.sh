#!/bin/sh
# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

REPOPATH=$(realpath .)
SCRIPTPATH="$REPOPATH/scripts/graphql.py"

python "$SCRIPTPATH" "$REPOPATH"
