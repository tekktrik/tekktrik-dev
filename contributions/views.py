# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Views for the contributions application."""

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from .models import Repository


def recent(request: WSGIRequest):
    """View for recent contributions."""
    repositories = Repository.objects.order_by("-last_push")

    return render(
        request,
        template_name="recent.html",
        context={
            "repos": repositories,
        },
    )
