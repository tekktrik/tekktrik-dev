# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

"""Delete the images from previous GraphQL query from the static folder."""

import datetime
import pathlib
import sys

import dateutil.tz

DATETIME_FMT = "%Y%m%d%H"

current_datetime = datetime.datetime.now(dateutil.tz.gettz())

last_datetime = current_datetime - datetime.timedelta(minutes=10)
last_datetime_str = last_datetime.strftime(DATETIME_FMT)

base_dir = pathlib.Path(sys.argv[1])

resp_dir = base_dir / "assets/contrib/"
old_resp_file = resp_dir / ("recent_" + last_datetime_str + ".json")
parent_card_dir = base_dir / "flask_app/static/img/gh_cards/"
old_card_dir = parent_card_dir / last_datetime_str

old_resp_file.unlink(missing_ok=True)
for card in old_card_dir.glob("*"):
    card.unlink(missing_ok=True)
old_card_dir.rmdir()
