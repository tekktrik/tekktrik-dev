# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

"""
Helper functions used by the Flask application

Author: Alec Delaney
"""

import json


def generate_settings_json(zipcode: str):
    """Generate a settings file for the CircuiyPythonukiah"""
    return json.dumps({"zipcode": zipcode})
