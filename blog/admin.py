# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Admin interface for the blog application."""

from django.contrib import admin

from .models import BlogEntry


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    """Admin view for blog entries."""

    list_display = (
        "title",
        "date",
        "link",
    )
