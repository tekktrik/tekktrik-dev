from flask import Flask, render_template

import json

app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Hello, world!</p>"
