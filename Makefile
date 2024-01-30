# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

.PHONY: localhost
localhost:
	flask --app flask_app run

.PHONY: lint
lint:
	pre-commit run ruff --all-files

.PHONY: format
format:
	pre-commit run ruff-format --all-files

.PHONY: check
check:
	pre-commit run --all-files
