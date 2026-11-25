# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Views for the blog application."""

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import BlogEntry


def blog(request: WSGIRequest):
    """Blog view."""
    blog_entries = BlogEntry.objects.order_by("-date", "-created_at")
    paginator = Paginator(blog_entries, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        template_name="blog.html",
        context={
            "page_obj": page_obj,
        },
    )
