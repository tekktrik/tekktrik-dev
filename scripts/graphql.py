# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

"""Download the images from the GraphQL query to the static folder."""

import datetime
import json
import os
import pathlib
import sys
import time

import dateutil.tz
import requests

# Store the GraphQL API URL and date format for files
URL = "https://api.github.com/graphql"
DATETIME_FMT = "%Y%m%d%H"


def download(assets_dir: os.PathLike, parent_card_dir: os.PathLike, delay: int) -> None:
    """Download contribution information."""
    # Convert pathlikes to pathlib.Path
    assets_dir = pathlib.Path(assets_dir)
    contrib_dir = assets_dir / "contrib"
    parent_card_dir = pathlib.Path(parent_card_dir)

    # Get the current datetime
    tz = dateutil.tz.UTC
    current_datetime = datetime.datetime.now(tz)

    # Get the datetime string based on the delay
    next_datetime = current_datetime + datetime.timedelta(minutes=delay)
    next_datetime_str = next_datetime.strftime(DATETIME_FMT)

    # Store the name of the new JSON response file
    contrib_dir.mkdir(exist_ok=True)
    new_resp_file = contrib_dir / f"recent_{next_datetime_str}.json"

    # Ensure the parent repository card image directory exists
    parent_card_dir.mkdir(exist_ok=True)

    # Create a directory for the specific repository image cards for the given datetime
    new_card_dir = parent_card_dir / next_datetime_str
    new_card_dir.mkdir(exist_ok=True)

    # Get the GraphQL query from the text file
    with open(assets_dir / "graphql_query.txt", encoding="utf-8") as queryfile:
        query_param = {"query": queryfile.read()}

    # Query the GraphQL API via a POST request
    resp = requests.post(
        URL,
        json=query_param,
        headers={
            "Authorization": f"Bearer {os.getenv('GRAPHQL_TOKEN')}",
        },
        timeout=5,
    )

    # Parse the request for a subset of the returned data (the "user" key)
    json_resp = json.loads(resp.content)["data"]["user"]

    # Store the subset of data in a JSON file for later use
    with open(new_resp_file, mode="w", encoding="utf-8") as contribfile:
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
                    with open(
                        str(new_card_dir / f"card{index}.png"), mode="wb"
                    ) as imgfile:
                        for data_chunk in img_resp:
                            imgfile.write(data_chunk)
                    break
            # If a timeout occurs, attempt the request again
            except (TimeoutError, requests.exceptions.ReadTimeout):
                pass
            # Add mandatory execution delay to prevent constant timeouts and rate limiting
            finally:
                if index != len_nodes - 1:
                    time.sleep(1)


if __name__ == "__main__":
    # Get the directories form the command line arguments
    assets_dir = pathlib.Path(sys.argv[1])
    parent_card_dir = pathlib.Path(sys.argv[2])
    delay = int(sys.argv[3])

    # Download the contribution information
    download(assets_dir, parent_card_dir, delay)
