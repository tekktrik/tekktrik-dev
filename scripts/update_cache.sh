#!/bin/sh
# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

# Script for immediately downloading GitHub repository summary
# card images, useful when errors occur and need to be fixed
# on the server

CURRENTPATH=$(pwd)
UPDATESCRIPTPATH="$CURRENTPATH/scripts/graphql.py"
ASSETSPATH="$CURRENTPATH/assets"
CONTRIBPATH="$ASSETSPATH/contrib"
GHCARDPATH="$CURRENTPATH/flask_app/static/img/gh_cards"


if [ $(date +%M) -ge 50 ]; then
    python "$UPDATESCRIPTPATH" "$ASSETSPATH" "$GHCARDPATH" 15
fi

python "$UPDATESCRIPTPATH" "$ASSETSPATH" "$GHCARDPATH" 0
