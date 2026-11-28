# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

include .env
export

.PHONY: start-prod
start-prod:
	npm install
	docker compose -f docker/prod-docker-compose.yaml build --no-cache
	docker compose -f docker/prod-docker-compose.yaml up -d

.PHONY: start-test
start-test:
	npm install
	docker compose -f docker/test-docker-compose.yaml build --no-cache
	docker compose -f docker/test-docker-compose.yaml up -d

.PHONY: start-debug
start-debug:
	uv run python manage.py sync_contributions
	uv run python manage.py runserver 127.0.0.1:8001

.PHONY: stop-prod
stop-prod:
	docker compose -f docker/prod-docker-compose.yaml down prod-app prod-cache --volumes

.PHONY: stop-test
stop-test:
	docker compose -f docker/test-docker-compose.yaml down test-app test-cache --volumes

.PHONY: lint
lint:
	uv run pre-commit run ruff --all-files

.PHONY: format
format:
	uv run pre-commit run ruff-format --all-files

.PHONY: check
check:
	uv run pre-commit run --all-files
