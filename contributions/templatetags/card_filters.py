# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Template tags related to contribution card animations."""

from django import template

register = template.Library()


@register.filter
def calc_delay(index_str: str) -> str:
    """Calculate the animation delay."""
    index = int(index_str)
    delay = round(index * 0.2 + 0.2, 1)
    return f"{delay}s"
