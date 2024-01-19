# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

"""
Main entry point for the flask application

Author: Alec Delaney
"""

import datetime
import io
import json

import jinja2
from flask import Flask, Response, redirect, render_template, send_file
from flask_bootstrap import Bootstrap5
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_app.forms import MenorahSetupForm
from flask_app.helpers import generate_settings_json, get_repo_info

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


@app.route("/")
def index() -> str:
    """Route for index (landing page)"""
    return render_template("index.html")


@app.route("/set-menorah")
def menorah_settings() -> Response:
    """Route for shortcut to menorah settings page"""
    return redirect("/projects/menorah/settings")


@app.route("/projects/menorah/settings", methods=["GET", "POST"])
@limiter.limit("10/second", key_func=lambda: "menorah-settings")
def project_menorah_settings() -> str:
    """Route for creating menorah settings file"""
    input_form = MenorahSetupForm()
    if input_form.validate_on_submit():
        zipcode = input_form.data["zipcode"]
        with open("assets/settings.json", mode="r", encoding="utf-8") as template_file:
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
    """Route for recent GitHub activity"""
    contributions, repos = get_repo_info(config["GH_TOKEN"])
    end_datetime = datetime.datetime.fromisoformat(contributions["endedAt"])
    start_datetime = datetime.datetime.fromisoformat(contributions["startedAt"])
    diff_datetime: datetime.timedelta = end_datetime - start_datetime
    return render_template(
        "recent.html",
        repos=repos["nodes"],
        num_contributions=contributions["contributionCalendar"]["totalContributions"],
        duration_days=diff_datetime.days,
    )
