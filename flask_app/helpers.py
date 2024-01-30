# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

"""Helper functions used by the Flask application.

Author: Alec Delaney
"""

import datetime
import json
from typing import Any, TypedDict

import dateutil.tz
import requests


class JobDict(TypedDict):
    """TypedDict representing job JSON file contents."""

    title: str
    employer: str
    location: str
    startDate: str
    endDate: str | None
    time: str
    duties: list[str]
    skills: list[str]


def generate_settings_json(zipcode: str) -> str:
    """Generate a settings file for the CircuiyPythonukiah."""
    return json.dumps({"zipcode": zipcode})


def get_repo_info(token: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Get repository info from the GraphQL query."""
    url = "https://api.github.com/graphql"

    with open("assets/graphql_query.txt", encoding="utf-8") as queryfile:
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


def sort_jobs_start_date(job: JobDict) -> int:
    """Sort the jobs by start date."""
    month_str, year_str = job["startDate"].split("/")
    return int(year_str) * 100 + int(month_str)


def consolidate_sorted_jobs(jobs: list[JobDict]) -> list[list[JobDict]]:
    """Consolidate jobs in instances like promotions."""
    grouped_jobs_dict: dict[str, list[JobDict]] = {}
    grouped_jobs_list: list[list[JobDict]] = []

    for job in jobs:
        newly_added = False
        employer = job["employer"]

        # If not already in dict, add
        if employer not in grouped_jobs_dict:
            grouped_jobs_dict[employer] = [job]
            newly_added = True

        # Get different of start and end of roles
        start_role = datetime.datetime.strptime(
            grouped_jobs_dict[employer][-1]["startDate"], "%m/%Y"
        )
        if job["endDate"] == "current":
            end_role = datetime.datetime.now(dateutil.tz.UTC)
        else:
            end_role = datetime.datetime.strptime(job["endDate"], "%m/%Y")

        # If job was not just newly added and gap is no more than 31 days apart
        # then add to existing list
        duration_days = 31
        if not newly_added and (start_role - end_role).days <= duration_days:
            grouped_jobs_dict[employer].append(job)

        elif not newly_added:
            grouped_jobs_list.append(grouped_jobs_dict[employer])
            grouped_jobs_dict[employer] = [job]

    for remaining_job in grouped_jobs_dict.values():
        grouped_jobs_list.append(remaining_job)

    return grouped_jobs_list


def sort_grouped_jobs(jobs_list: list[JobDict]) -> int:
    """Sort the grouped lists of jobs."""
    return sort_jobs_start_date(jobs_list[0])
