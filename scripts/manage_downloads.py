# SPDX-FileCopyrightText: 2025 Alec Delaney
# SPDX-License-Identifier: MIT

"""Manage the caching of contribution information."""

import datetime
import time

import graphql
import post_graphql

DATETIME_FMT = "%Y%m%d%H"


def get_time_strs() -> tuple[str, str]:
    """Get the download and deletion datetime strings."""
    # Get the current datetime
    tz = datetime.timezone.utc
    current_datetime = datetime.datetime.now(tz)

    # Get the download datetime string based on the delay
    next_download = current_datetime + datetime.timedelta(minutes=5)
    next_download_str = next_download.strftime(DATETIME_FMT)

    # Get the deletion datetime string based on the delay
    next_deletion = current_datetime + datetime.timedelta(minutes=-5)
    next_deletion_str = next_deletion.strftime(DATETIME_FMT)

    return next_download_str, next_deletion_str


last_download_str, last_deletion_str = get_time_strs()

while True:
    # Get the current datetime
    tz = datetime.timezone.utc
    current_datetime = datetime.datetime.now(tz)

    # Get the download datetime string based on the delay
    next_download = current_datetime + datetime.timedelta(minutes=5)
    next_download_str = next_download.strftime(DATETIME_FMT)

    # Get the deletion datetime string based on the delay
    next_deletion = current_datetime + datetime.timedelta(minutes=-5)
    next_deletion_str = next_deletion.strftime(DATETIME_FMT)

    if last_download_str != next_download_str:
        graphql.download(
            "/cache/assets",
            "/cache/gh_cards/",
            delay=10,
        )
        last_download_str = next_download_str

    if last_deletion_str != next_deletion_str:
        post_graphql.delete("/cache/assets/contrib", "/cache/gh_cards/", delay=10)
        last_deletion_str = next_deletion_str

    # Wait one minute
    time.sleep(60)
