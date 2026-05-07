# SPDX-FileCopyrightText: 2025 Alec Delaney
# SPDX-License-Identifier: MIT

# Use a base Python docker image
FROM python:3.12.10-alpine

# Set the working directory to app
WORKDIR /app

# Install Python app dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy necessary folders
COPY scripts/ scripts/
COPY assets/ assets/
COPY flask_app/ flask_app/

# Expose port for gunicorn
EXPOSE 8000

# Start gunicorn and serve website
CMD ["gunicorn", "--workers=3", "--thread=3", "-b", "0.0.0.0:8000", "flask_app:app"]
