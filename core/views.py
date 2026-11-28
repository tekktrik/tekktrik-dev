# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Views for the core application."""

from itertools import groupby
from operator import attrgetter

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from .models import Education, Employer, Employment


def index(request: WSGIRequest):
    """Index view."""
    return render(
        request,
        template_name="index.html",
    )


def about(request: WSGIRequest):
    """About (resume) view."""
    employments_collected = Employment.objects.order_by("employer")

    employments_grouped = {
        employer: list(jobs)
        for employer, jobs in groupby(employments_collected, key=attrgetter("employer"))
    }

    for group in employments_grouped.values():
        group.sort(key=attrgetter("start_date"), reverse=True)

    employments_ordered = sorted(
        employments_grouped.items(), key=lambda i: i[1][-1].start_date, reverse=True
    )

    employments: tuple[Employer, list[Employment]] = []
    for employer, employment_group in employments_ordered:
        group = []
        for index, role in enumerate(employment_group):
            if not index:
                group.append(role)
                continue
            next_role = employment_group[index - 1]
            delta = next_role.start_date - role.end_date
            max_days = 90
            if delta.days > max_days:
                employments.append((employer, group.copy()))
                group = []
            group.append(role)
        employments.append((employer, group))

    educations = Education.objects.order_by("-start_year")

    return render(
        request,
        template_name="about.html",
        context={
            "employments": employments,
            "educations": educations,
        },
    )
