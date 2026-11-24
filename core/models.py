# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Models for the core application."""

import datetime as dt

from django.db import models

# Create your models here.


class Education(models.Model):
    """Model for educational experiences."""

    school = models.CharField(max_length=64)
    degree = models.CharField(max_length=64)
    major = models.CharField(max_length=64)
    focus = models.CharField(max_length=64, blank=True)
    location = models.CharField(max_length=64)
    start_year = models.SmallIntegerField()
    end_year = models.SmallIntegerField()
    gpa = models.FloatField()

    def __str__(self) -> str:
        """Convert to string."""
        return f"{self.degree}, {self.major}"


class Employer(models.Model):
    """Model for employers of job experiences."""

    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        """Convert to string."""
        return self.name


class Employment(models.Model):
    """Model for employment experiences."""

    class EmploymentType(models.TextChoices):
        """Model for employment types."""

        FULL_TIME = "Full-Time", "Full-Time"
        FULL_TIME_COOP = "Full-Time (Co-op)", "Full-Time (Co-op)"
        PART_TIME = "Part-Time", "Part-Time"

    title = models.CharField(max_length=64)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    location = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    employment_type = models.CharField(
        max_length=32,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
    )
    duties = models.TextField()
    skills = models.TextField()

    def __str__(self) -> str:
        """Convert to string."""
        return f"{self.title}, {self.employer}"

    def _attr_list(self, attr: str) -> list[str]:
        """Get the list version of a field."""
        items = getattr(self, attr)
        if not items:
            return []
        return [item.strip() for item in items.splitlines() if item.strip()]

    @staticmethod
    def _simple_formatted_date(date: dt.date) -> str:
        """Get the date in the simplified resume format."""
        return date.strftime("%m/%Y")

    @property
    def simple_start_date(self) -> str:
        """The simplified resume start date."""
        return self._simple_formatted_date(self.start_date)

    @property
    def simple_end_date(self) -> str:
        """The simplified resume end date."""
        if not self.end_date:
            return "current"
        return self._simple_formatted_date(self.end_date)

    @property
    def duties_list(self) -> list[str]:
        """Duties as a list."""
        return self._attr_list("duties")

    @property
    def skills_list(self) -> list[str]:
        """Skills as a list."""
        return self._attr_list("skills")
