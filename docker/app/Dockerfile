# SPDX-FileCopyrightText: 2025 Alec Delaney
# SPDX-License-Identifier: MIT

# Use a base Python docker image
FROM ghcr.io/astral-sh/uv:python3.14-alpine

# Set the working directory to app
WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

# Copy site files
COPY tekktrik_dev/ tekktrik_dev/
COPY core/ core/
copy blog/ blog/
COPY contributions/ contributions/
COPY templates/ templates/
COPY manage.py manage.py

# Expose port for gunicorn
EXPOSE 8000

# Start gunicorn and serve website
CMD ["uv", "run", "gunicorn", "--workers=3", "--thread=3", "--bind", "0.0.0.0:8000", "tekktrik_dev.wsgi"]
