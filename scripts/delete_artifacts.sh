#!/bin/sh
# SPDX-FileCopyrightText: 2025 Alec Delaney
# SPDX-License-Identifier: MIT

# Script for deleting update artifacts

CURRENTPATH=$(pwd)

ASSETSPATH="$CURRENTPATH/assets"
CONTRIBPATH="$ASSETSPATH/contrib"
GHCARDPATH="$CURRENTPATH/flask_app/static/img/gh_cards"

rm -rf "$CONTRIBPATH"
rm -rf "$GHCARDPATH"
