# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

"""Delete the images from previous GraphQL query from the static folder.

This is used by a cron job that runs right ater the turn of the hour, so
it looks behind 10 minutes.
"""

import datetime
import pathlib
import sys

import dateutil.tz

# STore the date format
DATETIME_FMT = "%Y%m%d%H"

# Get the current datetime
current_datetime = datetime.datetime.now(dateutil.tz.gettz())

# Get the datetime string for 10 minutes ago
last_datetime = current_datetime - datetime.timedelta(minutes=10)
last_datetime_str = last_datetime.strftime(DATETIME_FMT)

# Get the base directory form the command line arguments
base_dir = pathlib.Path(sys.argv[1])

# Get all the necessary paths needed to delete relevant files
# (stored JSON response file and repository image cards and
# parent directory)
resp_dir = base_dir / "contrib/"
old_resp_file = resp_dir / ("recent_" + last_datetime_str + ".json")
parent_card_dir = base_dir / "gh_cards/"
old_card_dir = parent_card_dir / last_datetime_str

# Delete the store JSON response file
old_resp_file.unlink(missing_ok=True)

# Delete the repository image cards and parent directory
for card in old_card_dir.glob("*"):
    card.unlink(missing_ok=True)
old_card_dir.rmdir()
