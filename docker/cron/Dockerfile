# SPDX-FileCopyrightText: 2025 Alec Delaney
# SPDX-License-Identifier: MIT

# Use a base Python docker image
FROM python:3.12.10-bookworm

# Set the working directory to cron
WORKDIR /cron

# Copy necessary folders
COPY scripts/ scripts/
COPY assets/ assets/
COPY .env .env

# Make directories necessary for caching
RUN mkdir contrib
RUN mkdir gh_cards

# Install Python app dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Update the cache immediately
RUN sh scripts/update_cache.sh

# Install and start cron
RUN apt-get install debian-archive-keyring -y
RUN apt-get update
RUN apt-get install cron -y
RUN service cron start

# Install script dependencies
RUN pip install -r scripts/requirements.txt

# Schedule cache updates
RUN sh scripts/schedule_cache.sh

# Run cron in the foreground
CMD ["cron", "-f"]
