# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

"""Main entry point for the flask application.

Author: Alec Delaney
"""

import datetime
import io
import json
import math
import pathlib

import dateutil.parser
import dateutil.tz
import jinja2
from flask import Flask, Response, redirect, render_template, send_file
from flask_bootstrap import Bootstrap5
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_app.forms import MenorahSetupForm
from flask_app.helpers import (
    consolidate_sorted_jobs,
    sort_grouped_jobs,
    sort_jobs_start_date,
)

app = Flask(__name__)

with open("/etc/config.json", encoding="utf-8") as jsonfile:
    config = json.load(jsonfile)

app.config["WTF_CSRF_ENABLED"] = False

bootstrap = Bootstrap5(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50/second"],
    storage_uri="redis://localhost:6379",
    storage_options={"socket_connect_timeout": 30},
    strategy="moving-window",
)


@app.template_filter("timestamptodate")
def timestamptodate(timestamp: int):
    """Jinja filter to convert a timestamp to a date."""
    date = datetime.date.fromtimestamp(timestamp)
    return date.strftime("%b %d %Y")


@app.route("/")
def index() -> str:
    """Route for index (landing page)."""
    return render_template("index.html")


@app.route("/set-menorah")
def menorah_settings() -> Response:
    """Route for shortcut to menorah settings page."""
    return redirect("/projects/menorah/settings")


@app.route("/projects/menorah/settings", methods=["GET", "POST"])
@limiter.limit("10/second", key_func=lambda: "menorah-settings")
def project_menorah_settings() -> str:
    """Route for creating menorah settings file."""
    input_form = MenorahSetupForm()
    if input_form.validate_on_submit():
        zipcode = input_form.data["zipcode"]
        with open("assets/settings.json", encoding="utf-8") as template_file:
            template_text = template_file.read()
        template = jinja2.Template(template_text)
        rendered_temp = template.render(zipcode=zipcode)
        file_bytesio = io.BytesIO()
        file_bytesio.write(rendered_temp.encode("utf-8"))
        file_bytesio.seek(0)
        return send_file(
            file_bytesio, as_attachment=True, download_name="settings.json"
        )
    return render_template("projects/menorah/settings.html", input_form=input_form)


@app.route("/recent", methods=["GET"])
def recent() -> str:
    """Route for recent GitHub activity."""
    datetime_fmt = "%Y%m%d%H"
    current_datetime = datetime.datetime.now(dateutil.tz.gettz())
    current_datetime_str = current_datetime.strftime(datetime_fmt)
    with open(
        f"assets/contrib/recent_{current_datetime_str}.json", encoding="utf-8"
    ) as respfile:
        contents = json.load(respfile)
    contributions, repos = contents["contributionsCollection"], contents["repositories"]
    end_datetime = dateutil.parser.parse(contributions["endedAt"])
    start_datetime = dateutil.parser.parse(contributions["startedAt"])
    diff_datetime: datetime.timedelta = end_datetime - start_datetime
    oldest_push = dateutil.parser.parse(repos["nodes"][-1]["pushedAt"])
    diff_oldest = current_datetime - oldest_push
    return render_template(
        "recent.html",
        repos=repos["nodes"],
        num_contributions=contributions["contributionCalendar"]["totalContributions"],
        duration_days=diff_datetime.days,
        diff_oldest=math.ceil(diff_oldest.days / 365),
        current_datetime=current_datetime_str,
    )


@app.route("/about", methods=["GET"])
def about() -> str:
    """Route for about me page."""
    jobs_path = pathlib.Path("assets/about/jobs")
    jobs = []
    for job_path in jobs_path.glob("*.json"):
        with open(job_path, encoding="utf-8") as jobfile:
            job_obj = json.load(jobfile)
            if job_obj["endDate"] is None:
                job_obj["endDate"] = "current"
            jobs.append(job_obj)
    jobs.sort(key=sort_jobs_start_date, reverse=True)
    jobs_lists = consolidate_sorted_jobs(jobs)
    jobs_lists.sort(key=sort_grouped_jobs, reverse=True)

    education_paths = pathlib.Path("assets/about/education")
    educations = []
    for education_path in education_paths.glob("*.json"):
        with open(education_path, encoding="utf-8") as edufile:
            edu_obj = json.load(edufile)
            if edu_obj["endYear"] is None:
                edu_obj["endYear"] = "current"
            educations.append(edu_obj)
    educations.sort(key=lambda x: x["startYear"], reverse=True)

    return render_template("about.html", jobs_lists=jobs_lists, educations=educations)


@app.route("/other", methods=["GET"])
@app.route("/other/<pagenum>", methods=["GET"])
def other(pagenum: str = "1") -> str:
    """Route for other work page."""
    pagenum = int(pagenum)
    if pagenum <= 0:
        pagenum = 1
    other_path = pathlib.Path("assets/other")
    other_works = []
    for other_filepath in other_path.glob("*.json"):
        with open(other_filepath, encoding="utf-8") as otherfile:
            other_obj = json.load(otherfile)
            other_works.append(other_obj)

    max_pages = len(other_works) // 5 + 1

    start_index = (pagenum - 1) * 5
    end_index = start_index + 5

    if start_index >= len(other_works):
        return other(pagenum - 1)

    other_works.sort(key=lambda x: x["datetime"], reverse=True)

    return render_template(
        "other.html",
        works=other_works[start_index:end_index],
        pagenum=pagenum,
        maxpages=max_pages,
    )
