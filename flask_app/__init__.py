# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT


app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Hello, world!</p>"
