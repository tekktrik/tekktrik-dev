# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Admin interface for the contributions application."""

from django.contrib import admin

from .models import Language, LanguageEntry, Repository


class LanguageEntryInline(admin.TabularInline):
    """Inline languages for repositories."""

    model = LanguageEntry
    extra = 0


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """Admin view for languages."""

    list_display = (
        "name",
        "background_color",
        "black_text",
    )


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    """Admin view for repositories."""

    list_display = (
        "name",
        "owner",
        "last_push",
        "created_at",
    )

    list_filter = ("owner",)

    search_fields = (
        "name",
        "owner",
        "languages",
    )

    inlines = (LanguageEntryInline,)


@admin.register(LanguageEntry)
class LanguageEntryAdmin(admin.ModelAdmin):
    """Admin view for language entries."""

    list_display = (
        "language",
        "repository",
        "index",
    )

    list_filter = (
        "language",
        "repository",
    )
