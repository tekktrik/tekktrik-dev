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

URL = "https://api.github.com/graphql"
DATETIME_FMT = "%Y%m%d%H"

current_datetime = datetime.datetime.now(dateutil.tz.gettz())

if "--now" in sys.argv:
    delay = 0
else:
    delay = 10

next_datetime = current_datetime + datetime.timedelta(minutes=delay)
next_datetime_str = next_datetime.strftime(DATETIME_FMT)

base_dir = pathlib.Path(sys.argv[1])

resp_dir = base_dir / "assets/contrib/"
new_resp_file = resp_dir / ("recent_" + next_datetime_str + ".json")
parent_card_dir = base_dir / "flask_app/static/img/gh_cards/"
new_card_dir = parent_card_dir / next_datetime_str
resp_dir.mkdir(exist_ok=True)
parent_card_dir.mkdir(exist_ok=True)
new_card_dir.mkdir(exist_ok=True)

with open("/etc/config.json", encoding="utf-8") as jsonfile:
    config = json.load(jsonfile)

with open(base_dir / "assets/graphql_query.txt", encoding="utf-8") as queryfile:
    query_param = {"query": queryfile.read()}

resp = requests.post(
    URL,
    json=query_param,
    headers={
        "Authorization": f'Bearer {config["GH_TOKEN"]}',
    },
    timeout=5,
)

json_resp = json.loads(resp.content)["data"]["user"]

with open(
    resp_dir / f"recent_{next_datetime_str}.json", mode="w", encoding="utf-8"
) as contribfile:
    json.dump(json_resp, contribfile)


len_nodes = len(json_resp["repositories"]["nodes"])
for index, node in enumerate(json_resp["repositories"]["nodes"]):
    for _ in range(3):
        try:
            img_resp = requests.get(node["openGraphImageUrl"], timeout=10)
            status_okay = 200
            if img_resp.status_code == status_okay:
                with open(str(new_card_dir / f"card{index}.png"), mode="wb") as imgfile:
                    for data_chunk in img_resp:
                        imgfile.write(data_chunk)
                break
        except (TimeoutError, requests.exceptions.ReadTimeout):
            pass  # Try again
        finally:
            if index != len_nodes - 1:
                time.sleep(1)
