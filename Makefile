PY_SRCS := app tests
.PHONY: lint fmt lintfix type security cc mi check fix up down
lint:
	uv run ruff check $(PY_SRCS)
fmt:
	uv run ruff format $(PY_SRCS)
lintfix:
	uv run ruff check $(PY_SRCS) --fix
fix: lintfix fmt
type:
	uv run mypy $(PY_SRCS)
security:
	uv run bandit -r $(PY_SRCS) -lll
cc:
	uv run radon cc -s -a $(PY_SRCS)
mi:
	uv run radon mi $(PY_SRCS)
check: lint type security cc mi
up:
	docker compose --env-file .env.docker -f docker-compose-local.yaml up -d
down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force