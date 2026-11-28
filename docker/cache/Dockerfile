# SPDX-FileCopyrightText: 2025 Alec Delaney
# SPDX-License-Identifier: MIT

# Use a base Python docker image
FROM ghcr.io/astral-sh/uv:python3.14-alpine

# Set the working directory to cache
WORKDIR /cache

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

# Copy site files
COPY tekktrik_dev/ tekktrik_dev/
COPY core/ core/
copy blog/ blog/
COPY contributions/ contributions/
COPY manage.py manage.py

# Copy entry point script
COPY docker/cache/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Start the container
ENTRYPOINT ["/entrypoint.sh"]
