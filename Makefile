# SPDX-FileCopyrightText: 2024 Alec Delaney
# SPDX-License-Identifier: MIT

include .env
export

.PHONY: start-prod
start-prod:
	sh scripts/update_cache.sh
	docker compose -f docker/prod-docker-compose.yaml up -d --build
	sh scripts/delete_artifacts.sh

.PHONY: start-test
start-test:
	sh scripts/update_cache.sh
	docker compose -f docker/test-docker-compose.yaml up -d --build
	sh scripts/delete_artifacts.sh

.PHONY: stop-prod
stop-prod:
	docker compose -f docker/prod-docker-compose.yaml down prod-app prod-cache --volumes

.PHONY: stop-test
stop-test:
	docker compose -f docker/test-docker-compose.yaml down test-app test-cache --volumes

.PHONY: lint
lint:
	pre-commit run ruff --all-files

.PHONY: format
format:
	pre-commit run ruff-format --all-files

.PHONY: check
check:
	pre-commit run --all-files
