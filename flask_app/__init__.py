# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

"""
Main entry point for the flask application

Author: Alec Delaney
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    """Route for index (landing page)"""
    return "<p>Hello, world!</p>"
