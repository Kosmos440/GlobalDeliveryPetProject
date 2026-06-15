PY_SRCS=api db main.py settings.py
.PHONY: lint fmt lintfix type security cc mi check fix up down
lint:
	poetry run ruff check $(PY_SRCS)
fmt:
	poetry run ruff format $(PY_SRCS)
lintfix:
	poetry run ruff check $(PY_SRCS) --fix
fix: lintfix fmt
type:
	poetry run mypy $(PY_SRCS)
security:
	poetry run bandit -r api db -lll -x venv,.venv,FastVenv,tests,migrations
cc:
	poetry run radon cc -s -a $(PY_SRCS)
mi:
	poetry run radon mi $(PY_SRCS)
check: lint type security cc mi
up:
	docker compose --env-file .env.docker -f docker-compose-local.yaml up -d
down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force