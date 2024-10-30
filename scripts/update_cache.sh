#!/bin/sh
# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

# Script for immediately downloading GitHub repository summary
# card images, useful when errors occur and need to be fixed
# on the server

REPOPATH=$(realpath .)
PATH="$REPOPATH/.venv/bin:$PATH"
SCRIPTPATH="$REPOPATH/scripts/graphql.py"

python "$SCRIPTPATH" "$REPOPATH" --now
