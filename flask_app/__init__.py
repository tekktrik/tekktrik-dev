# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

"""Main entry point for the flask application.

Author: Alec Delaney
"""

import datetime
import json
import math
import pathlib

import bs4
import dateutil.parser
import dateutil.tz

# import jinja2
from flask import (
    Flask,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from flask_bootstrap import Bootstrap5

from flask_app.helpers import (
    consolidate_sorted_jobs,
    sort_grouped_jobs,
    sort_jobs_start_date,
)

# Initialize the Flask app
app = Flask(__name__)

# Disable CSRF for WTForms
app.config["WTF_CSRF_ENABLED"] = False

# Initialize Bootstrap
bootstrap = Bootstrap5(app)


@app.template_filter("timestamptodate")
def timestamptodate(timestamp: int):
    """Jinja filter to convert a timestamp to a date."""
    date = datetime.date.fromtimestamp(timestamp)
    return date.strftime("%b %d %Y")


@app.route("/")
def index() -> str:
    """Route for index (landing page)."""
    return render_template("index.html")


@app.route("/recent", methods=["GET"])
def recent() -> str:
    """Route for recent GitHub activity."""
    # Get the current datetime and hour as a string
    datetime_fmt = "%Y%m%d%H"
    current_datetime = datetime.datetime.now(dateutil.tz.gettz())
    current_datetime_str = current_datetime.strftime(datetime_fmt)

    # Read the contents of the relevant (current) recent activity JSON file
    with open(
        f"assets/contrib/recent_{current_datetime_str}.json", encoding="utf-8"
    ) as respfile:
        contents = json.load(respfile)

    # Get the contribtuons (calendar) collection and specific respository contributions
    contributions, repos = contents["contributionsCollection"], contents["repositories"]

    # Get the start, end, and delta between times within the contributions collection
    end_datetime = dateutil.parser.parse(contributions["endedAt"])
    start_datetime = dateutil.parser.parse(contributions["startedAt"])
    diff_datetime: datetime.timedelta = end_datetime - start_datetime

    # Get the oldest push datetime from the specific repository contributions
    oldest_push = dateutil.parser.parse(repos["nodes"][-1]["pushedAt"])
    diff_oldest = current_datetime - oldest_push

    # Render the HTML template
    rendered = render_template(
        "recent.html",
        repos=repos["nodes"],
        num_contributions=contributions["contributionCalendar"]["totalContributions"],
        duration_days=diff_datetime.days,
        diff_oldest=math.ceil(diff_oldest.days / 365),
        current_datetime=current_datetime_str,
    )

    # Check if the files are there, use the original image URL if there was an error
    soup = bs4.BeautifulSoup(rendered, "html.parser")
    for index, repo in enumerate(repos["nodes"]):
        if not pathlib.Path(
            f"flask_app/static/img/gh_cards/{current_datetime_str}/card{index}.png"
        ).exists():
            img = soup.find("img", {"id": f"gh_card_img{index}"})
            img["src"] = repo["openGraphImageUrl"]
            rendered = soup.prettify()

    # Return the rendered and possibly repaired template
    return rendered


@app.route("/gh_cards/<path:filename>")
def reroute_gh_cards(image_name):
    """Reroute the path for GitHub cards."""
    return send_from_directory("assets/gh_cards", image_name)


@app.route("/about", methods=["GET"])
def about() -> str:
    """Route for about me page."""
    # Load the jobs files and initialize them in a list
    jobs_path = pathlib.Path("assets/app/about/jobs")
    jobs = []
    for job_path in jobs_path.glob("*.json"):
        with open(job_path, encoding="utf-8") as jobfile:
            job_obj = json.load(jobfile)
            # No end date means it's the current (active) job
            if job_obj["endDate"] is None:
                job_obj["endDate"] = "current"
            jobs.append(job_obj)

    # Sort the jobs list based on the custom sorting filter
    jobs.sort(key=sort_jobs_start_date, reverse=True)

    # Consolidate jobs that are grouped (like promotions)
    jobs_lists = consolidate_sorted_jobs(jobs)

    # Sort the grouped jobs based on the custom sorting filter
    jobs_lists.sort(key=sort_grouped_jobs, reverse=True)

    # Load the education files and initialize them in a list
    education_paths = pathlib.Path("assets/app/about/education")
    educations = []
    for education_path in education_paths.glob("*.json"):
        with open(education_path, encoding="utf-8") as edufile:
            edu_obj = json.load(edufile)
            # No end date means it's the current (active) education
            if edu_obj["endYear"] is None:
                edu_obj["endYear"] = "current"
            educations.append(edu_obj)

    # Sort the educations by start year
    educations.sort(key=lambda x: x["startYear"], reverse=True)

    # Render the HTML template
    return render_template("about.html", jobs_lists=jobs_lists, educations=educations)


@app.route("/other", methods=["GET"])
@app.route("/other/<pagenum>", methods=["GET"])
def other(pagenum: str = "1") -> str:
    """Route for other work page."""
    # Load the other activities files and initialize them in a list
    other_path = pathlib.Path("assets/app/other")
    other_works = []
    for other_filepath in other_path.glob("*.json"):
        with open(other_filepath, encoding="utf-8") as otherfile:
            other_obj = json.load(otherfile)
            other_works.append(other_obj)

    # Calculate the maximum number of pages that can be rendered
    # (assuming groups of 5 activities per page), minimum of 1 page
    max_pages = (len(other_works) + 4) // 5
    max_pages = 1 if max_pages < 1 else max_pages

    # Convert the request page number to an integer and redirect
    # if it is outside the possible bounds of allowable pages
    pagenum = int(pagenum)
    if pagenum < 1:
        return redirect(url_for("other", pagenum=1))
    if pagenum > max_pages:
        return redirect(url_for("other", pagenum=max_pages))

    # Calculate the start and end indices for the current page number
    start_index = (pagenum - 1) * 5
    end_index = start_index + 5

    # Sort the list of activities base on the datetime key
    other_works.sort(key=lambda x: x["datetime"], reverse=True)

    # Render the HTML template
    return render_template(
        "other.html",
        works=other_works[start_index:end_index],
        pagenum=pagenum,
        maxpages=max_pages,
    )
