# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Models for the blog application."""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class BlogEntry(models.Model):
    """Model for blog entries."""

    title = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to="blog_photos/", blank=True, null=True)
    image_credits = models.TextField(blank=True)
    alt_text = models.TextField(blank=True)
    link = models.URLField(blank=True)
    aria_label = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        """Convert to string."""
        return self.date.strftime("%b. %d, %Y")

    def clean(self):
        """Perform validation on the model."""
        super().clean()

        if not self._state.adding:
            return

        errors = {}

        dependencies = {
            "image": ("image_credits", "alt_text"),
            "link": ("aria_label",),
        }

        for field, dependents in dependencies.items():
            for dependent_field in dependents:
                if getattr(self, field) and not getattr(self, dependent_field):
                    errors[dependent_field] = f"Required when {field} is provided."

        if errors:
            raise ValidationError(errors)
