# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

"""Download the images from the GraphQL query to the static folder."""

import datetime
import json
import pathlib
import sys
import time

import dateutil.tz
import requests

# Store the GraphQL API URL and date format for files
URL = "https://api.github.com/graphql"
DATETIME_FMT = "%Y%m%d%H"

# Get the current datetime
current_datetime = datetime.datetime.now(dateutil.tz.gettz())

# If "--now" is given as a a command line argument, use the current time
# Otherwise, this is being used by a cron job that runs right before the
# turn of the hour, so look ahead 10 minutes.  Note that this isn't an
# execution delay.
if "--now" in sys.argv:
    delay = 0
else:
    delay = 10

# Get the datetime string based on the delay
next_datetime = current_datetime + datetime.timedelta(minutes=delay)
next_datetime_str = next_datetime.strftime(DATETIME_FMT)

# Get the base directory form the command line arguments
base_dir = pathlib.Path(sys.argv[1])

# Create the directory to store the responses
resp_dir = base_dir / "assets/contrib/"
resp_dir.mkdir(exist_ok=True)

# Store the name of the new JSON response file
new_resp_file = resp_dir / f"recent_{next_datetime_str}.json"

# Ensure the parent repository card image directory exists
parent_card_dir = base_dir / "flask_app/static/img/gh_cards/"
parent_card_dir.mkdir(exist_ok=True)

# Create a directory for the specific repository image cards for the given datetime
new_card_dir = parent_card_dir / next_datetime_str
new_card_dir.mkdir(exist_ok=True)

# Read the configuration settings file
with open("/etc/config.json", encoding="utf-8") as jsonfile:
    config = json.load(jsonfile)

# Get the GraphQL query from the text file
with open(base_dir / "assets/graphql_query.txt", encoding="utf-8") as queryfile:
    query_param = {"query": queryfile.read()}

# Query the GraphQL API via a POST request
resp = requests.post(
    URL,
    json=query_param,
    headers={
        "Authorization": f"Bearer {config['GH_TOKEN']}",
    },
    timeout=5,
)

# Parse the request for a subset of the returned data (the "user" key)
json_resp = json.loads(resp.content)["data"]["user"]

# Store the subset of data in a JSON file for later use
with open(
    resp_dir / f"recent_{next_datetime_str}.json", mode="w", encoding="utf-8"
) as contribfile:
    json.dump(json_resp, contribfile)

# Iterate through the returned repository nodes
len_nodes = len(json_resp["repositories"]["nodes"])
for index, node in enumerate(json_resp["repositories"]["nodes"]):
    # Attempt three times to store the image card
    for _ in range(3):
        try:
            # Get the repository image card (OpenGraph image)
            img_resp = requests.get(node["openGraphImageUrl"], timeout=10)
            status_okay = 200

            # If request is successful, save the image for caching purposes
            if img_resp.status_code == status_okay:
                with open(str(new_card_dir / f"card{index}.png"), mode="wb") as imgfile:
                    for data_chunk in img_resp:
                        imgfile.write(data_chunk)
                break
        # If a timeout occurs, attempt the request again
        except (TimeoutError, requests.exceptions.ReadTimeout):
            pass  # Try again
        # Add mandatory execution delay to prevent constant timeouts and rate limiting
        finally:
            if index != len_nodes - 1:
                time.sleep(1)
