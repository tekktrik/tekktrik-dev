# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

"""CLI tool for getting the timestamp for a given datetime.

Author: Alec Delaney
"""

import datetime
import re
import sys

import click


@click.command()
@click.argument("dt")
def main(dt: str) -> None:
    """Print the timestamp for the given datetime."""
    # Match the required regex pattern
    result = re.match(
        r"(\d{1,2})/(\d{1,2})/(\d\d|\d\d\d\d)@(\d{1,2}):(\d\d):(\d\d)", dt
    )

    # Exit with error if no matching result
    if not result:
        click.echo("Could not find datetime of format [m]m/[d]d/[yy]yy@[h]h:mm:ss")
        sys.exit(1)

    # Get the year provided as a string (exactly as it was)
    _, _, year_str, _, _, _ = result.groups()

    # Get the found components of the regex
    int_results = [int(value) for value in result.groups()]
    month, day, year, hour, minute, second = int_results

    # Assume the year is within the current century if only two digits were provided
    if len(year_str) == 2:  # noqa: PLR2004
        current_year = datetime.datetime.now().year
        current_century = (current_year // 100) * 100
        year += current_century

    # Get the timestamp for the given date
    converted_datetime = datetime.datetime(year, month, day, hour, minute, second)
    timestamp = converted_datetime.timestamp()

    # Print the timestamp
    click.echo(int(timestamp))


if __name__ == "__main__":
    main()
