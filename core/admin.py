# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Admin interface for the core application."""

from django.contrib import admin

from .models import Education, Employer, Employment


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """Admin view for educational experiences."""

    list_display = (
        "degree",
        "school",
        "major",
    )


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    """Admin view for employers."""

    list_display = ("name",)


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    """Admin view for employment experiences."""

    list_display = (
        "title",
        "employer",
        "start_date",
        "end_date",
    )

    ordering = ("-start_date",)
