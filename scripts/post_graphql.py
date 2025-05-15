# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

"""Delete the images from previous GraphQL query from the static folder."""

import datetime
import os
import pathlib
import sys

import dateutil.tz

# STore the date format
DATETIME_FMT = "%Y%m%d%H"


def delete(contrib_dir: os.PathLike, parent_card_dir: os.PathLike, delay: int) -> None:
    """Delete the cached contribution information."""
    # Convert pathlikes to pathlib.Path
    contrib_dir = pathlib.Path(contrib_dir)
    parent_card_dir = pathlib.Path(parent_card_dir)

    # Get the current datetime
    tz = dateutil.tz.UTC
    current_datetime = datetime.datetime.now(tz)

    # Get the datetime string for 10 minutes ago
    last_datetime = current_datetime - datetime.timedelta(minutes=delay)
    last_datetime_str = last_datetime.strftime(DATETIME_FMT)

    # Get all the necessary paths needed to delete relevant files
    # (stored JSON response file and repository image cards and
    # parent directory)
    old_resp_file = contrib_dir / f"recent_{last_datetime_str}.json"
    old_card_dir = parent_card_dir / last_datetime_str

    # Delete the store JSON response file
    old_resp_file.unlink(missing_ok=True)

    # Delete the repository image cards and parent directory
    for card in old_card_dir.glob("*"):
        card.unlink(missing_ok=True)
    old_card_dir.rmdir()


if __name__ == "__main__":
    # Get the base directory form the command line arguments
    contrib_dir = pathlib.Path(sys.argv[1])
    parent_card_dir = pathlib.Path(sys.argv[2])
    delay = int(sys.argv[3])

    # Delete the old cards
    delete(contrib_dir, parent_card_dir, delay)
