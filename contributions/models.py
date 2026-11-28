# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Models for the contributions application."""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def validate_hex_code(value: str) -> None:
    """Validate hex codes."""
    if not value.startswith("#"):
        raise ValidationError("Value must start with # symbol.")

    try:
        _ = int(value[1:], 16)
    except ValueError as err:
        raise ValidationError("Invalid hex code") from err


class Language(models.Model):
    """Model for programming lanaguages."""

    name = models.CharField(max_length=64)
    background_color = models.CharField(
        max_length=7, default="#87CEFA", validators=(validate_hex_code,)
    )
    black_text = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Convert to string."""
        return self.name

    def clean(self):
        """Clean the data."""
        super().clean()

        self.background_color = self.background_color.upper()


class Repository(models.Model):
    """Model for a repository that has personal contributions."""

    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    url = models.URLField()
    index = models.SmallIntegerField()
    opengraph_image = models.ImageField(upload_to="contributions/")
    last_push = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        """Convert to string."""
        return f"{self.owner}/{self.name}"

    @property
    def language_entries(self) -> list[LanguageEntry]:
        """Information about the languages used in the repository."""
        return list(LanguageEntry.objects.filter(repository=self))


class LanguageEntry(models.Model):
    """Model for language entries for repositories."""

    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    index = models.SmallIntegerField()

    def __str__(self) -> str:
        """Convert to string."""
        return f"{self.repository} [{self.index + 1}]: {self.language}"
