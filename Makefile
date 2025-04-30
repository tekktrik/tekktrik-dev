# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

.PHONY: start-prod
start-prod:
	docker compose -f docker/prod-docker-compose.yaml up -d --build

.PHONY: start-test
start-test:
	docker compose -f docker/test-docker-compose.yaml up -d --build

.PHONY: stop-prod
stop-prod:
	docker compose -f docker/prod-docker-compose.yaml down prod-app prod-cron --volumes

.PHONY: stop-test
stop-test:
	docker compose -f docker/test-docker-compose.yaml down test-app test-cron --volumes

.PHONY: lint
lint:
	pre-commit run ruff --all-files

.PHONY: format
format:
	pre-commit run ruff-format --all-files

.PHONY: check
check:
	pre-commit run --all-files
