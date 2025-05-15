# SPDX-FileCopyrightText: 2025 Alec Delaney
# SPDX-License-Identifier: MIT

# Use a base Python docker image
FROM python:3.12.10-alpine

# Set the working directory to cache
WORKDIR /cache

ARG GRAPHQL_TOKEN
ENV GRAPHQL_TOKEN=${GRAPHQL_TOKEN}

# Install Python app dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Make directories necessary for caching
COPY scripts/ scripts/
COPY assets/ assets/
COPY flask_app/static/img/gh_cards gh_cards/

WORKDIR /cache/scripts

# Start the cache script
CMD ["python", "manage_downloads.py"]
