# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

"""
Helper functions used by the Flask application

Author: Alec Delaney
"""

import json
from typing import Any

import requests


def generate_settings_json(zipcode: str) -> str:
    """Generate a settings file for the CircuiyPythonukiah"""
    return json.dumps({"zipcode": zipcode})


def get_repo_info(token: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Get repository info from the GraphQL query"""
    url = "https://api.github.com/graphql"

    with open("assets/graphql_query.txt", mode="r", encoding="utf-8") as queryfile:
        query_param = {"query": queryfile.read()}

    resp = requests.post(
        url,
        json=query_param,
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=5,
    )

    json_resp = json.loads(resp.content)["data"]["user"]

    return json_resp["contributionsCollection"], json_resp["repositories"]
