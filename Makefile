.PHONY: venv init lint test run docker-build docker-run fmt


venv:
	python -m venv .venv
	./.venv/bin/pip install --upgrade pip


init:
	pip install -e .[dev]


lint:
	ruff check src tests


fmt:
	ruff check --fix src tests || true


test:
	pytest


run:
	python -m quest_generator_bot.bot


# Docker
IMAGE?=ghcr.io/tristanstarkl/quest-generator-bot:latest


docker-build:
	docker build -t $(IMAGE) .


docker-run:
	docker run --rm \
	--env-file .env \
	-v $(PWD)/external:/app/external \
	-v $(PWD)/data:/app/data \
	$(IMAGE)