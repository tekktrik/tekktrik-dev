# SPDX-FileCopyrightText: 2023 Alec Delaney
# SPDX-License-Identifier: MIT

"""WTForms used in the Flask application.

Author: Alec Delaney
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class MenorahSetupForm(FlaskForm):
    """Form for menorah information."""

    zipcode = StringField("Zip Code", validators=[DataRequired()])
    submit = SubmitField("Generate file...")
