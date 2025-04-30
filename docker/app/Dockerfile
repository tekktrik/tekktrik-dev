# SPDX-FileCopyrightText: 2025 Alec Delaney
# SPDX-License-Identifier: MIT

# Use a base Python docker image
FROM python:3.12.10-bookworm

# Set the working directory to app
WORKDIR /app

# Copy necessary folders
COPY flask_app/ flask_app/
COPY scripts/ scripts/
COPY assets/ assets/

# Install Python app dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Expose port for gunicorn
EXPOSE 8000

# Start gunicorn and serve website
CMD ["gunicorn", "--workers=3", "-k", "eventlet", "-b", "0.0.0.0:8000", "flask_app:app"]
