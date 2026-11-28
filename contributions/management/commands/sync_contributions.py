# SPDX-FileCopyrightText: 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Command for syncing contributions."""

import datetime as dt
import json
import os
from typing import Any

import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Language, LanguageEntry, Repository

URL = "https://api.github.com/graphql"

QUERY = """
query {
  user (login: "tekktrik") {
    contributionsCollection {
      startedAt
      endedAt
      contributionCalendar {
        totalContributions
      }
    }
    repositories (
      first: 20,
      orderBy: {
        field: PUSHED_AT,
        direction: DESC,
      },
      isArchived: false,
      isLocked: false,
      isFork: false,
      visibility: PUBLIC,
    ) {
      nodes {
        name,
        owner {
          login
        },
        primaryLanguage {
          name
        },
        languages (first: 5) {
          totalCount,
          nodes {
            name
          }
        }
        openGraphImageUrl,
        url,
        pushedAt
      }
    }
  }
}
"""


class Command(BaseCommand):
    """Sync the contributions database."""

    help = "Sync the contributions database."

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> str | None:
        """Execute the command."""
        Repository.objects.all().delete()

        resp = requests.post(
            URL,
            json={"query": QUERY},
            headers={
                "Authorization": f"Bearer {os.getenv('GRAPHQL_TOKEN')}",
            },
            timeout=10,
        )

        content = json.loads(resp.content)
        try:
            json_resp = content["data"]["user"]
        except KeyError as err:
            raise PermissionError(content["message"]) from err

        repositories = json_resp["repositories"]["nodes"]
        for repository_index, repository_info in enumerate(repositories):
            repository = Repository.objects.create(
                name=repository_info["name"],
                owner=repository_info["owner"]["login"],
                url=repository_info["url"],
                index=repository_index,
                opengraph_image_url=repository_info["openGraphImageUrl"],
                last_push=dt.datetime.fromisoformat(repository_info["pushedAt"]),
            )

            languages = [
                Language.objects.get_or_create(
                    name=node["name"],
                )[0]
                for node in repository_info["languages"]["nodes"]
            ]

            for language_index, language in enumerate(languages):
                LanguageEntry.objects.create(
                    language=language,
                    repository=repository,
                    index=language_index,
                )
