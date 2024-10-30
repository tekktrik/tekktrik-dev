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
    # Store the GraphQL API URL
    url = "https://api.github.com/graphql"

    # Get the query from the saved text file
    with open("assets/graphql_query.txt", encoding="utf-8") as queryfile:
        query_param = {"query": queryfile.read()}

    # Query the API via a POST requrest
    resp = requests.post(
        url,
        json=query_param,
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=5,
    )

    # Return only part of the return data (values within the "user" key)
    json_resp = json.loads(resp.content)["data"]["user"]
    return json_resp["contributionsCollection"], json_resp["repositories"]


def sort_jobs_start_date(job: JobDict) -> int:
    """Sort the jobs by start date."""
    # Split the month and year
    month_str, year_str = job["startDate"].split("/")
    # Use basic formula for data sorting
    return int(year_str) * 100 + int(month_str)


def consolidate_sorted_jobs(jobs: list[JobDict]) -> list[list[JobDict]]:
    """Consolidate jobs in instances like promotions."""
    # Initialize empty dictionary for storing job groupings while iterating
    grouped_jobs_dict: dict[str, list[JobDict]] = {}

    # Initialize emptry list for storing sorted job groupings
    grouped_jobs_list: list[list[JobDict]] = []

    # Iterate through provided jobs
    for job in jobs:
        # Keep track of whether employers are newly added to the list
        newly_added = False

        # Get the employer for the current job being analyzed
        employer = job["employer"]

        # If not already in dict, add it and note it is a new job
        if employer not in grouped_jobs_dict:
            grouped_jobs_dict[employer] = [job]
            newly_added = True

        # Get start date of newer role and end date of older role
        # (contained list is sorted in order of newest to oldest)
        start_new_role = datetime.datetime.strptime(
            grouped_jobs_dict[employer][-1]["startDate"], "%m/%Y"
        )
        if job["endDate"] == "current":
            end_old_role = datetime.datetime.now(dateutil.tz.gettz())
        else:
            end_old_role = datetime.datetime.strptime(job["endDate"], "%m/%Y")

        # If the employer was not newly added and  the gap is no more than 31 days
        # apart, then add it to  the existing list.  This prevents grouping roles
        # that have large breaks in between them (e.g., returning co-ops with no
        # job in between).
        #
        # If the employer has already been added to the dictionary and the time
        # between the jobs is short, append it to the existing grouping and keep
        # using it, as more jobs may be found to add to this grouping.
        duration_days = 31
        if not newly_added and (start_new_role - end_old_role).days <= duration_days:
            grouped_jobs_dict[employer].append(job)

        # Otherwise, if the employer is still in the list but the time between jobs
        # is longer than 31 days, add the existing grouping to the return job list
        # and begin a new dict for iteration, as the current dict is a complete group.
        elif not newly_added:
            grouped_jobs_list.append(grouped_jobs_dict[employer])
            grouped_jobs_dict[employer] = [job]

    # Jobs still remaining in the dict after iteration are complete, and should be
    # added to the return job list
    for remaining_job in grouped_jobs_dict.values():
        grouped_jobs_list.append(remaining_job)

    # Return the grouped jobs list
    return grouped_jobs_list


def sort_grouped_jobs(jobs_list: list[JobDict]) -> int:
    """Sort the grouped lists of jobs (based on first job within group)."""
    return sort_jobs_start_date(jobs_list[-1])
