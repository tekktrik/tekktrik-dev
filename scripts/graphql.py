# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

"""Download the images from the GraphQL query to the static folder."""

import json
import pathlib
import sys

import requests

URL = "https://api.github.com/graphql"

with open("/etc/config.json", encoding="utf-8") as jsonfile:
    config = json.load(jsonfile)

with open("assets/graphql_query.txt", mode="r", encoding="utf-8") as queryfile:
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
base_dir = pathlib.Path(sys.argv[1])
resp_dir = base_dir / "assets/contrib/"
card_dir = base_dir / "flask_app/static/img/gh_cards/"
resp_dir.mkdir(exist_ok=True)
card_dir.mkdir(exist_ok=True)

with open(str(resp_dir / "recent.json"), mode="w", encoding="utf-8") as contribfile:
    json.dump(json_resp, contribfile)


for index, node in enumerate(json_resp["repositories"]["nodes"]):
    for _ in range(5):
        img_resp = requests.get(node["openGraphImageUrl"], timeout=5)
        if img_resp.status_code == 200:
            with open(str(card_dir / f"card{index}.png"), mode="wb") as imgfile:
                for data_chunk in img_resp:
                    imgfile.write(data_chunk)
